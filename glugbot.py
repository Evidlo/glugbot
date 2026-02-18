#!/usr/bin/env python3
# Get the current week's meeting topic from GLUG calendar

import requests
from io import StringIO
from mrkdwn_analysis import MarkdownAnalyzer
import dateparser
from datetime import datetime
import re
import sys

from glugbot_secrets import *

# ----- Parse schedule from GitHub -----
today = datetime.now().date()

season = 's' if today.month < 9 else 'f'
semester = today.strftime(f'%Y{season}')
url = f'https://raw.githubusercontent.com/gnulug/meetings/refs/heads/master/{semester}/schedule.md'
md = requests.get(url).content
md = MarkdownAnalyzer(StringIO(md.decode('utf8')))
table = list(md.identify_tables().values())[0]
rows = table[0]['rows']

# check if any dates on the schedule are today
for row in rows:
    if dateparser.parse(row[0]).date() == today:
        break
else:
    print(f'No matching date found for {today}')
    sys.exit()

# generate presenter string
if row[2].lower() in ('', 'n/a', 'na', '-'):
    by = ''
else:
    by = f' by {row[2]}'

# ---- Parse room number from homepage ----
url = 'https://lug.acm.illinois.edu'
html = requests.get(url)
match = re.findall(b'Location.*([0-9]{4}).*\\n', html.content)

if len(match) == 1:
    room = match[0].decode('utf8')
else:
    room = '[err]'

# generate HTML and plaintext announcement
msg = f"<strong>Reminder</strong> - Meeting today in Siebel {room} @ 6pm: <strong>{row[1]}</strong>{by}"
msgplain = f"Reminder - Meeting today in Siebel 1302 @ 6pm: {row[1]}{by}"
print(f'Sending message: {msg}')

# ----- Send over Matrix -----

from matrix_client.client import MatrixClient
c = MatrixClient(homeserver)
c.login_with_password(user, password)

r = c.join_room(room)
# r.send_html(msg)
r.client.api.send_message_event(
    room_id=r.client.api.get_room_id(room),
    event_type='m.room.message',
    content={
        "body": msgplain,
        "formatted_body": msg,
        "format": "org.matrix.custom.html",
        "m.mentions": {
            "room": True # notify entire room
        },
        "msgtype": "m.text"
    }
)

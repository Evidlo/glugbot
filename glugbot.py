#!/usr/bin/env python3
# Get the current week's meeting topic from GLUG calendar

import requests
from io import StringIO
from mrkdwn_analysis import MarkdownAnalyzer
import dateparser
from datetime import datetime
import sys

from glugbot_secrets import *

# ----- Parse schedule from GitHub -----
today = datetime.now().date()

season = 's' if today.month < 6 else 'f'
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
if row[2] == '' or row[2] == 'N/A':
    by = ''
else:
    by = f' by {row[2]}'

# generate HTML and plaintext announcement
msg = f"<strong>Reminder</strong> - Meeting today in Siebel 1302 @ 6pm: <strong>{row[1]}</strong>{by}"
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
        "body": "@room foo",
        "m.mentions": {
            "room": True # notify entire room
        },
        "body": msgplain,
        "format": "org.matrix.custom.html",
        "formatted_body": msg,
        "msgtype": "m.text"
    }
)

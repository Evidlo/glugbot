# glugbot

[GLUG](lug.acm.illinois.edu) calendar bot

# Install

``` sh
chmod +x glugbot.py
pip install -r requirements
# edit  glugbot.service to point to `glugbot.py`
ln -rs glugbot.service ~/.config/systemd/user
ln -rs glugbot.timer ~/.config/systemd/user
systemctl --user daemon-reload
systemctl --user enable glugbot.timer
systemctl --user enable glugbot.service
```

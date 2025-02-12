# glugbot

[GLUG](lug.acm.illinois.edu) calendar bot

# Install

ln -rs glugbot.service ~/.config/systemd/user
ln -rs glugbot.timer ~/.config/systemd/user
ln -rs glugbot.py ~/bin
chmod +x glugbot.py
systemctl --user daemon-reload
systemctl --user enable glugbot.timer
systemctl --user enable glugbot.service
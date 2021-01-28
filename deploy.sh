#!/usr/bin/env bash
# exit when any command fails
KEY_FILE="/Users/maxfowler/.ssh/peach_rsa"

# deploy
echo "++ copying files to pi"
rsync -avzh --exclude target --exclude .idea --exclude .git -e "ssh -i $KEY_FILE" . peach@peach.link:/srv/peach-config


#!/bin/bash
sudo cp -r ./foohid.kext /Library/Extensions/foohid.kext
sudo chmod -R 755 /Library/Extensions/foohid.kext
sudo chown -R root:wheel /Library/Extensions/foohid.kext
sudo kextload /Library/Extensions/foohid.kext

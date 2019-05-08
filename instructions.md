# Using OffKeyboard


## Download & Install Python 3

This project is written in Python 3, which is not shipped by default with macOS. 
To install Python 3, follow these steps:

* Open the Terminal application at /Applications/Utilities/Terminal.app, and enter these commands

The first command is to install homebrew (www.brew.sh), which is a program for managing development tools on macOS

The second command uses brew to install python 3.

```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

brew install python3
```

If you get a permissions error on the second command, run this:

```bash
sudo chown -R "$USER":admin /usr/local
sudo chown -R "$USER":admin /Library/Caches/Homebrew
```

## Set Up The Project's Dependencies

OffKeyboard uses several other Python utilities, which must be installed before it can be run.

Open the Terminal application and enter these commands. I've explained each command with a comment starting with `#`:

```bash
# Install tools which will let us set up a Python 3 environment specifically for OffKeyboard
sudo easy_install pip
sudo pip install virtualenv

# Navigate to the project folder within the terminal
cd /The/Folder/You/Downloaded/OffKeyboard/

# Set up a Python 3 environment specifically for OffKeyboard
virtualenv -p python3 ./
# Activate the OffKeyboard Python environment
source ./bin/activate

# Install the project's dependencies
pip install -r requirements.txt
```

## Running the project

Without closing the terminal, run this command:

```bash
# Launch OffKeyboard
python tonedeaf_composer/__init__.py
```

To stop it, click CTRL+C

If you close your terminal and want to run OffKeyboard again, re-run these commands:
```bash
# Navigate to the project folder within the terminal
cd /The/Folder/You/Downloaded/OffKeyboard/
# Activate the OffKeyboard Python environment
source ./bin/activate
# Launch OffKeyboard
python tonedeaf_composer/__init__.py
```

As long as it is running, OffKeyboard will listen to the microphone (or whatever the active system input is), 
identify pitches, and send key events per our spec.

OffKeyboard will print some of the things it's doing as you play the bass, so keep an eye on this output if you run into
an issue or want to verify that pitches are being detected properly.

## Configuring OffKeyboard

I've tried to make it straightforward for you to play around with the common key mappings.
Configure the key bindings in config.py. This lets you set what key will be pressed for what bass pitch.
If you want anything changed/configured that I didn't include in this config, just ask me -- it'll be easy 
for me to update.

If you quickly want to modify the keymap, you can directly modify the code in tonedeaf_composer/keymaps.py, around line 90.

## Configuring Minecraft

This isn't a strict requirement, but I'm short on time before dinner so just to make sure our setups match: Rebind
the movement keys in Minecraft to be the arrow keys instead.

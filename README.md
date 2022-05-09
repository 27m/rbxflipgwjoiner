# RBXFlip Giveaway Joiner

An automatic giveaway joiner for RBXFlip.

- Inspired by [foobball](https://github.com/foobball) and [htach](https://github.com/htach).
- Credit to htach for [fprint](https://github.com/htach/mass-send/blob/main/main.py#L30).

# Notice:

For the forseeable future, this will not be a multi-account joiner. I have made an agreement to keep this program single-account.
Thank you for understanding.

# Installation:

Navigate to [releases](https://github.com/27m/rbxflipgwjoiner/releases/latest/) and download the latest release's source code.
## Windows

Unzip the files into a directory.

If you don't have python installed already, install it [here](https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe) (This link is for 64-bit if you are on 32-bit you can find the 32-bit installer [here](https://www.python.org/ftp/python/3.10.4/python-3.10.4.exe)).

Run ``setup.bat``

Put the corresponding information in ``config.json``.

Open the command line

![image](https://user-images.githubusercontent.com/70358442/166136292-72dac04f-dbb5-420b-84d8-44b5b0a2104a.png)

Navigate to the script's directory with ``cd``.

### Run the script with ``py main.py`` (NOTE: ``py`` may be ``python`` or ``python3`` for you depending on your installed python version).

### OR double click main.py.

Image for clarity below.

![image](https://user-images.githubusercontent.com/70358442/166135582-7232e8eb-1a57-4a3a-b4cd-d8e364386a1f.png)

## Linux

Navigate to the script's directory.

Execute ``pip install -r requirements.txt``

Put the corresponding information in ``config.json``.

Run the script with ``py main.py`` NOTE: ``py`` may be ``python`` or ``python3`` for you depending on your installed python version.

# Report any bugs to marshall#4949 on discord. 

# How to get your RBXFlip token:

![image](https://user-images.githubusercontent.com/70358442/166135270-906dbaec-583a-400d-8b8e-8abb7e98ae1c.png)
(courtesy of foobball)

# config.json variables

access_token - This is your RBXFlip access token (how we authenticate giveaway join requests). Instructions on how to get this token are shown above.

fetch_interval - This is how many seconds the program will wait in between fetching current giveaways, 20-30 is recommended. 

webhook - This is your **full** webhook link ex: https://discord.com/api/webhooks/example

# Disclaimer

This program is currently beta and you may encounter bugs. Please report them to the discord account stated above. 

I am releasing this to find any bugs that may occur. Thank you

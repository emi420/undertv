# Under TV

A television box for the internet citizen 

## Requirements

* This project was designed to run on a Raspberry PI
* First, you will need to install omxplayer 2.5

## How to run and test the project

0. Check yout settings

(edit settings.py file)

1. Install sample data:

(you can edit sampledata.py and add your own YouTube playlists)

# python sampledata.py

2. Download content

# python contentdownloader.py

3. Run server

# python webserver.py

4. Run commands from any browser:

http://< Raspberry PI IP address >/power
http://< Raspberry PI IP address >/next_ch
http://< Raspberry PI IP address >/prev_ch



# Under TV

A television box for the internet citizen 

## Requirements

* This project was designed to run on a Raspberry PI
* You will need to install omxplayer 2.5

## How to run and test the project

0. Check your settings

Edit settings.py file

1. Install sample data:

You can edit sampledata.py and add your own YouTube playlists

$ python sampledata.py

2. Download content

$ python contentdownloader.py

3. Run server

$ python webserver.py

4. Run commands from any browser:

http://< Raspberry PI IP address >/power
http://< Raspberry PI IP address >/next_ch
http://< Raspberry PI IP address >/prev_ch

I'm developing a mobile app for using as a remote control ;)

## License

You may use any Under TV project under the terms of the GNU General Public License (GPL) Version 3.

(c) 2013 Emilio Mariscal
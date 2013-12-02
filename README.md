# Under TV

A television box for the internet citizen 

## Requirements

* This project was designed to run on a Raspberry PI
* You will need to install omxplayer 2.5

## How to run and test the project

1) Check your settings

Edit settings.py file

2) Install sample data:

Copy video files on a 'content' folder and initialize it

$ python createdata.py content

3) Run server

$ python webserver.py

4) Run commands from any browser:

http://<IP_address>/power
http://<IP_address>/next_ch
http://<IP_address>/prev_ch

I'm developing a mobile app for using as a remote control ;)

## License

You may use any Under TV project under the terms of the GNU General Public License (GPL) Version 3.

(c) 2013 Emilio Mariscal

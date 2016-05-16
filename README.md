# Under TV

A television box for the internet citizen 

## Requirements

* This project was designed to run on a Raspberry PI
* You will need to install omxplayer and pyomxplayer with pexpect and ptyprocess

## How to run and test the project

1) Check your settings

Edit settings.py file

2) Copy video files

Copy video files on the 'videos' folder

3) Run server

$ sudo python webserver.py

Open this from any browser

http://IP_address/

Or send commands

* http://IP_address/random
* http://IP_address/pause
* http://IP_address/stop
* http://IP_address/skip_ahead
* http://IP_address/skip_back

## License

You may use any Under TV project under the terms of the GNU General Public License (GPL) Version 3.

(c) 2013 Emilio Mariscal

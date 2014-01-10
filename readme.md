needed packages:
  pyfiglet
  paramiko (for ssh only)
needed fonts:
  straight.flf
  univers.flf

instructions for Linux Mint:
to install figlet and fonts:
	sudo apt-get install -y {,python-py}figlet && cd /usr/share/figlet && sudo wget http://www.figlet.org/fonts/straight.flf http://www.figlet.org/fonts/univers.flf && chmod 644 *.flf
paramiko can be downloaded from:
	http://www.lag.net/paramiko/legacy.html
	

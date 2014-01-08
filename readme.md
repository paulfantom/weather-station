needed package:
  pyfiglet
  paramiko (for ssh only)
needed font:
  straight.flf
  univers.flf

to install figlet and fonts:
	in linux mint exec command:
	  sudo apt-get install -y {,python-py}figlet && cd /usr/share/figlet && sudo wget http://www.figlet.org/fonts/straight.flf http://www.figlet.org/fonts/univers.flf && chmod 644 *.flf

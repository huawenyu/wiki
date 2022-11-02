First check with 

dmesg | grep tty 

if system recognize your adapter. Then try run minicom with 

	$ sudo minicom -s

go to "Serial port setup" and change first line with /dev/ttyUSB0.  (/dev/ttyS0 for BIOS port "COM1", /dev/ttyS1 for BIOS port "COM2")
Speed 9600 8 bits, no parity, 1 stop for all FGT
Press F and G to set both the hardware and software flow control to "none"
Don't forget to save config as default with "Save setup as dfl". 

$ sudo chmod ua+rwx /dev/ttyUSB0
$ minicom	+=== succ connect to our box

You can try different bt
Power off the FGT unit and use the following :

* Terminal client (windows hyperterminal, linux minicom...)
o Speed 9600 8 bits, no parity, 1 stop for all FGT 

* Null modem serial cable (provided with the Fortigate)
* Provide a fixed IP address to your PC eg: 192.168.1.168
* tftp server running on a PC


# Connect your PC LAN interface using an eth cross cable to :

* "Interface Internal"

# Power on the Fortigate Unit
# Press any key at when "Press Any Key To Download Boot Image...." message will be displayed
# Enter the IP addresses

* Enter tftp server address [192.168.1.168]: 192.168.1.168
* Enter local address [192.168.1.188]: 192.168.1.188
* Enter File Name [image.out]: image name.out

# Traffic should be displayed the TFTP server ( ensure image is located in the appropriate folder)




Launch minicom in setup mode by typing:

bash# minicom -s
The "configuration" window will popup. Using the arrow down key, move to the "Serial port setup" entry and press Enter.

A new popup window will appear, giving you the ability to change the serial port settings. Press the A key and enter the serial line to suit your hardware configuration (/dev/ttyS0 for BIOS port "COM1", /dev/ttyS1 for BIOS port "COM2"). Press Enter

Press E to change the serial parameters. A new window "comm parameters" will show up.

In this new window, press I to set the speed to 115200bps, and Q to use 8 data bits, no parity, and 1 stop bit. Press Enter to go back to the previous window.

Press F and G to set both the hardware and software flow control to "none". Press Enter to go back to the main "configuration" window.

Using the arrow down key, move down to either "Save setup as dfl" or "Save setup as...", depending if you want to save this setup as the default setup, or save it into an alternate configuration file.

Using the arrow down key, move down to "Exit" to leave the configuration mode and go into terminal emulation mode.


# Linux

https://github.com/jordansissel/xdotool
We can use it to config our global shortcut to activate a windows.

## Using xdotool
  xdotool search "Mozilla Firefox" windowactivate
  xdotool search "Google Chrome" windowactivate
  xdotool search "Alacritty" windowactivate
  xdotool search "Terminal" windowactivate
  xdotool search "MousePad" windowactivate

## Using wmctrl [better]
    $ wmctrl -lx
        0x01000003 -1 xfce4-panel.Xfce4-panel  hyu-dell xfce4-panel
        0x01400028 -1 xfdesktop.Xfdesktop   hyu-dell Desktop
        0x03a00007  1 virt-manager.Virt-manager  hyu-dell Virtual Machine Manager
        0x03a00216  1 virt-manager.Virt-manager  hyu-dell ubuntu20.04 on QEMU/KVM
        0x04600003  0 google-chrome.Google-chrome  hyu-dell linux - How to use wmctrl to activate window of a given class? - Super User - Google Chrome
        0x0460003c  0 crx_ifpfemkbbkoldmalnheaiimnceiljfpe.Google-chrome  hyu-dell Mail - hyu@fortinet.com
        0x05600003  0 xfce4-terminal.Xfce4-terminal  hyu-dell Terminal - 
        0x05600210  0 xfce4-terminal.Xfce4-terminal  hyu-dell Terminal - 
        0x05600289  0 xfce4-terminal.Xfce4-terminal  hyu-dell Terminal - 
        0x05600b2a  0 xfce4-terminal.Xfce4-terminal  hyu-dell Terminal - 
        0x01c02ca7  0 Thunar.Thunar         hyu-dell hyu - File Manager
        0x05c00006  0 wireshark.Wireshark   hyu-dell PCAP_Exempt.pcap
        0x05600e45  0 xfce4-terminal.Xfce4-terminal  hyu-dell Terminal - 
        0x056027a5  0 xfce4-terminal.Xfce4-terminal  hyu-dell Terminal - 
        0x05a00003  0 mousepad.Mousepad     hyu-dell *Untitled 2 - Mousepad
        0x03c00002  0 Alacritty.Alacritty   hyu-dell Alacritty
        0x0540002c  0 Navigator.Firefox     hyu-dell FortiGuard Service Network — Mozilla Firefox
        0x06000005  0 microsoft teams - preview.Microsoft Teams - Preview  hyu-dell Me | Microsoft Teams
        0x06a00007  0 xfce4-keyboard-settings.Xfce4-keyboard-settings  hyu-dell Keyboard

  wmctrl -x -a  "Firefox"
  wmctrl -x -a  "Google-chrome"
  wmctrl -x -a  "Alacritty"
  wmctrl -x -a  "Terminal"
  wmctrl -x -a  "MousePad"


# LinuxMint-XFCE

## Mint 19 Xfce typing delay

When I start "Xfce Terminal" there is a few seconds delay after typing a character from appearing.
Seems like anything related with typing has this delay (eg: Firefox, text editor, etc) but "Xfce Terminal" is the worst.

[Solved]:
  Start>>"Windows Manager Tweeks">>Tab-Comositor>>unchecked the "Enable display compositing", WORKED! =)

## Mail-client: evolution

### Setting: open link in firefox/chrome

```sh
    # Check the config, sure it's not xfce's config, because evolution not know the xfce at all.
    $ gvfs-mime --query x-scheme-handler/http
    $ gvfs-mime --query x-scheme-handler/https

        Default application for 'x-scheme-handler/http': firefox.desktop
        Registered applications:
                firefox.desktop
                google-chrome.desktop
                opera.desktop
        Recommended applications:
                firefox.desktop
                google-chrome.desktop
                opera.desktop

    # Set it to chrome
    $ gvfs-mime --set x-scheme-handler/http google-chrome.desktop
    $ gvfs-mime --set x-scheme-handler/https google-chrome.desktop
```

### Viewing Unread messages from task-bar windows title

1. Right Click on "Search Folders", and create a new folder, for example named as 'vfolder':
 - in vfolder properties
 - in "rules", make a rule that says "Status" "is not" "read"
 - in "search folder sources" choose specific folders, or the all folders option.
   You can also choose "all related" threads to get replies and parents to an unread message in the same vfolder.

Now view this folder instead of your inbox, and you will only see unread messages!

2. Compare with another method: You can also choose View -> Hide Read Messages to accomplish this > task.

The 'vfolder' isn't as simple as just showing unread messages.  I actually have the following in my vfolder rules:

 - "Date sent" "is after" "2 days ago" or
 - "Status" "is not" "Read" or
 - "Label" "is" "Important"

This shortens my inbox with ~800 messages down to less than 20!
I also have "Include threads - all related", so that I get replies and
originals that fall outside of the above criteria.

It's great!  Evolution is the only mail reader I know that lets you do
so much with vfolders.  Even thunderbird's search folders can't do as
well as this!

## Howto install Google-Pinyin(base on fcitx) in LinuxMint

Following is what I did to install/configure Google Pinyin in Linux Mint (English version) using "fcitx" so that I can switch input method to enter either English or Chinese at will in Linux Mint 18.3.

(Step 1): Use software manager to install the following package:

Menu → Administration → Software Manager, enter “fcitx” in search box and find the following from the search result and click to install:

fcitx
fcitx-config-gtk
fcitx-frontend-gtk2
fcitx-frontend-gtk3
fcitx-googlepinyin
fcitx-ui-classic
Close (x) software manager

(Step 2): Change Input Method to “Fcitx”:
Menu ⇒ Preferences ⇒ Input Method ⇒ set Input method to [Fcitx]

(Step 3): Logout and Login

(Step 4): Verify a small keyboard icon appears in the system tray area

(Step 5): Add “Google Pinyin” to Fcitx:
- Right-click keyboard icon in system tray ⇒ Configure, this would bring up "Input Method Configuration" window
- click (+) sign
- click (x) to uncheck "Only Show Current Language" so to list all the available languages
- Select Google Pinyin (I found it at the very bottom of the list)
- click OK
- click [Appearance] Tab ⇒ change ClassicUI Font size from ‘0’ to ‘12’
- click [Addon] Tab ⇒ Input method selector ⇒ Configure ⇒ IMSelector ⇒ Global Input Method SelectKey ⇒ click first [Empty] box ⇒ press Ctrl+Shift+Space on the keyboard ⇒ OK
ps. this Ctrl+Shift+Space is my keyboard shortcut to switch the input language.

(Step 6): Test Chinese input:
- Open Terminal (or a browser)
- Enter (Ctrl+Shift+Space) and value '2' on the keyboard to select Google Pinyin (or use mouse to select) 

# Linux

## check 32- or 64-Bit
https://unix.stackexchange.com/questions/106234/determine-if-a-specific-process-is-32-or-64-bit
http://en.wikipedia.org/wiki/Executable_and_Linkable_Format#File_header

/proc/$PID/exe yourself. It's quite trivial: if the 5th byte in the file is 1, it's a 32-bit binary. If it's 2, it's 64-bit. For added sanity checking:

If the first 5 bytes are 0x7f, "ELF", 1: it's a 32 bit ELF binary.
If the first 5 bytes are 0x7f, "ELF", 2: it's a 64 bit ELF binary.
Otherwise: it's inconclusive.

## add a new user or change username

Unix-like operating systems decouple the user name from the user identity, so you may safely
change the name without affecting the ID. All permissions, files, etc are tied to your identity
(uid), not your username.

As I only have ONE user account (administrator), it would not let me change the username ("you
are already logged in" was the response in TTY1 (<kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>F1</kbd>). To
get around this:

 1. Login with your old credentials and add a new user, e.g. "temporary" in TTY1:

        sudo adduser temporary

 set the password.
 2. Allow the temporary user to run sudo by adding the user to sudo group:

        sudo adduser temporary sudo

 3. Log out with the command `exit`.
 4. Return to tty1: Login with the 'temporary' user account and password. Change your username
 and folder as mentioned above. `exit` (until you get the login prompt)
 5. Go back to TTY7 (<kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>F7</kbd>) to login on the GUI/normal
 desktop screen and see if this works.

To change username (it is probably best to do this without being logged in):

    sudo usermod -l newUsername oldUsername

This however, doesn't rename the home folder.
To change home-folder, after you changed the username:

    sudo usermod -d /home/newHomeDir -m newUsername

 6. Delete temporary user and folder:

        sudo deluser temporary
        sudo rm -r /home/temporary

## To reset your lost or fogotten password:

1. Reboot your computer / Turn your computer on.
2. Hold down the Shift key at the start of the boot process to enable the GNU GRUB2 boot menu (if it does not show)
3. Select the entry for your Linux installation, Press e to edit.
4. Use the Arrow keys to navigate to a line that looks similar to this:

    linux /boot/vmlinuz-[kernel version]-generic root=UUID=[letters and numbers]\[letters and numbers] ro quiet splash vt.handoff=7

Change ro quiet splash vt.handoff=7 to rw init=/bin/bash so it now reads:

    linux /boot/vmlinuz-[kernel version]-generic root=UUID=[letters and numbers]\[letters and numbers] rw init=/bin/bash

5. Press F10 to boot your system.
   Your system will boot up to a passwordless root shell.
6. Type in `passwd <yourusername>`
    (if you have also forgotten your username, type cat /etc/passwd first to get a list of all users, yours should be at the end)
    Set your new password.
7. Restart your system.

## chrome browser write disk and too slow

## File Descriptor Limit: ulimit -n

To ensure good server performance, the total number of client connections, database files, and log files must not exceed the maximum file descriptor limit on the operating system (ulimit -n).
By default, the directory server allows an unlimited number of connections but is restricted by the file descriptor limit on the operating system.
Linux systems limit the number of file descriptors that any one process may open to 1024 per process. (This condition is not a problem on Solaris machines, x86, x64, or SPARC).

After the directory server has exceeded the file descriptor limit of 1024 per process, any new process and worker threads will be blocked.
For example, if the directory server attempts to open a Oracle Berkeley JE database file when the operating system has exceeded the file descriptor limit,
the directory server will no longer be able to open a connection that can lead to a corrupted database exception.
Likewise, if you have a directory server that exceeds the file descriptor limit set by the operating system,
the directory server can become unresponsive as the LDAP connection handler consumes all of the CPU's processing in attempting to open a new connection.

To fix this condition, set the maximum file descriptor limit per process on Linux machines.

## To Increase the File Descriptor Limit (Linux)

1. Display the current hard limit of your machine.
The hard limit is the maximum server limit that can be set without tuning the kernel parameters in proc file system.


    $ ulimit -aH
        core file size (blocks)       unlimited
        data seg size (kbytes)        unlimited
        file size (blocks)            unlimited
        max locked memory (kbytes)    unlimited
        max memory size (kbytes)      unlimited
        open files                    1024
        pipe size (512 bytes)         8
        stack size (kbytes)           unlimited
        cpu time (seconds)            unlimited
        max user processes            4094
        virtual memory (kbytes)       unlimited

2. Edit the /etc/security/limits.conf and add the lines:

    * soft   nofile  1024
    * hard   nofile  65535

3. Edit the /etc/pam.d/login by adding the line:
    session required /lib/security/pam_limits.so

4. Use the system file limit to increase the file descriptor limit to 65535.

    The system file limit is set in /proc/sys/fs/file-max .
    $ echo 65535 > /proc/sys/fs/file-max

5. Use the ulimit command to set the file descriptor limit to the hard limit specified in /etc/security/limits.conf.
    ulimit -n unlimited

6. Restart your system.

## Add a new SSD to current LINUX

### Format a raw disk

    cat /proc/partitions
    ls /dev/sd*
    sudo fdisk /dev/sdb
    sudo mkfs.ext3 -L /photos /dev/sdb1
    sudo mkdir /photos
    sudo mount /dev/sdb1 /photos

### add to fstab

    $ ls -l /dev/disk/by-uuid
        lrwxrwxrwx 1 root root 10 Jun  3 13:26 237d1b39-de75-400f-ae65-aa41661cbd75 -> ../../sda2
        lrwxrwxrwx 1 root root 10 Jun  3 13:26 74435dd8-635d-4d8e-999a-c2fe86210b3f -> ../../sda1
        lrwxrwxrwx 1 root root 10 Jun  3 13:25 bff3bd70-7ca0-4f25-aeba-a4e6c95b07ef -> ../../sdb1

        $ cat /etc/fstab
        # /etc/fstab: static file system information.
        #
        # Use 'blkid' to print the universally unique identifier for a
        # device; this may be used with UUID= as a more robust way to name devices
        # that works even if disks are added and removed. See fstab(5).
        #
        # <file system> <mount point>   <type>  <options>       <dump>  <pass>
        # / was on /dev/sda1 during installation
        UUID=74435dd8-635d-4d8e-999a-c2fe86210b3f /               ext4    errors=remount-ro 0       1
        UUID=237d1b39-de75-400f-ae65-aa41661cbd75 /data           ext4    errors=remount-ro 0       1
        UUID=bff3bd70-7ca0-4f25-aeba-a4e6c95b07ef /ssd            ext4    defaults          0       0    <=== Append this line


## Tmux user: Add a temp user, share screen with tmux

    $ sudo useradd guest
    $ sudo passwd guest

    Sample-1:
    /// Create session
    tmux -S /tmp/shareds new -s sharedsession
    /// Change ownership to group
    chgrp mutual_group_name /tmp/shareds
    /// Run this in other user or ssh session to attach yourself
    tmux -S /tmp/shareds attach -t sharedsession

    Sample-2:
    ### To Start a new session
    $ tmux -S /tmp/socket new -s sharesess
    ### Change its permission for other users to access
    $ chmod 777 /tmp/socket
    ### for other users to attach to the session
    $ tmux -S /tmp/socket attach -t sharesess

    $ sudo userdel -r guest       <=== with -r: del home-dir, mail-spool

### Create restricted user 'user1'

    https://superuser.com/questions/149404/create-an-ssh-user-who-only-has-permission-to-access-specific-folders

The easiest way to create restricted user that cannot wander off the given directory (e.g., to the upper directory etc).

    sudo ln -s /bin/bash /bin/rbash

    #sudo adduser --home /home/user1 user1
    sudo useradd -s /bin/rbash -d /home/user1 user1
    cd /home
    sudo mkdir user1
    sudo chmod 755 user1

    # create a tmux session which we can share with other user1
    tmux -S /tmp/tmux_share new -s share
    sudo chmod 777 ./tmux_share             <=== let user1 can access it

    # user1 remote login, then attach to the same session
    tmux -S /tmp/tmux_share attach -t share

    # delete the user1
    sudo userdel -r user1     <=== delete that user's home directory and mail spool by using the -r flag

    # if want the restrict user1 can execute more command, we can link the command to his home-directory.
        # Moreover/Optionally, to restrict the user to a limited/picked set of command to use, you can create a .bash_profile read-only to that user, with

        PATH=$HOME/bin

        # and symlink whatever commands you allows into the ~/bin folder to that user:
        ln -s /bin/ls /home/restricted_folder/bin/ls
        ln -s /bin/mkdir /home/restricted_folder/bin/mkdir
        ln -s /bin/rm /home/restricted_folder/bin/rm


# Howtos

## Clipboard

There are two types of clipboards in Unix/Linux:
- PRIMARY (often used with Ctrl-X/C/V) 
- SELECTION (mouse selected text, inserted with Shift-Insert or clicking the mouse middle button).

**In a regular shell session:**

	I select with the mouse, and use Ctrl+Shift+C to COPY to clipboard
	I use Ctrl+Shift+V to paste.

**Here's what I used to do:** 

	Ctrl+Insert : Copy to the clipboard
	Shift+Insert : PASTE from the clipboard
	Shift+Delete : Cut TO the clipboard

**Now I have an Apple Keyboard, I do:**
(The apple keyboard does not have an insert key)

	Ctrl+C to Copy to the clipboard
	Ctrl+V to PASTE FROM the clipboard
	Shift+Delete to cut TO THE clipboard. 

**In a terminal using Putty:**
Select the text with the mouse copies directly to the clipboard

	Right-Clicking anywhere in the terminal window does the paste

### vim copy/paste accross vim-instance

https://github.com/ojroques/vim-oscyank




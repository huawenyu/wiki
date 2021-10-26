# Terminal: MoboXterm [Maybe the best]

- Pros:
  1. A pretty Terminal
  2. Support ssh, x-forward
  3. Also we get a cygwin Environment:
        Which support python, node, emacs, vim8.0, git, svn, curl, and more ...
          Install: apt install curl

- Cons:
  2. WSL's ssh more better
  3. WSL linux env much-much better
        But embbed linux/bash sucks, it's better change to wsl (better wsl2, but need newer windows 10 build).


## Config

[tab]Terminal:
  Looks:
    Font=MobaFont, Syntax=None, ColorScheme=Monokai
  TerminalFeatures:
    [check] Font Antialiasing
    [un-check] Display scrollbar
  Local shell:
    TerminalShell=WSL Ubuntu
    PromptType=No separation line
    [un-check] Backspace sends ^H

[tab]Display
  SkinSelect=Windows dark theme


# [Too slow] GUI editor: Notepad++

We can start WSL-ubuntu, then using vim8, it's more better.

## Dark theme

https://github.com/chriskempson/tomorrow-theme

copy from tomorrow-theme/notepad++ to `C:\Users\Kids\AppData\Roaming\Notepad++\Themes`



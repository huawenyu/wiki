# How to write vim python3 plugin:

The most basic "plugin" for me you need as follows:

    A folder ~/.config/nvim/rplugin/python3/pluginName with:

    plugin.py (Can be called whatever, but its the entry to your plugin).

    __init__.py

Where they contain the following:

plugin.py:

 import pynvim

 @pynvim.plugin
 class TestPlugin:
     def __init__(self, nvim):
         self._nvim = nvim

    @pynvim.command("PythonTestCommand")
    def print_hello(self):
        self._nvim.out_write("Hello!\n")

__init__.py:

from .plugin import TestPlugin

If I save that, run :UpdateRemotePlugins and then restart neovim, I can run my command fine and get the echo'd message.

Could you be missing one of those files? Or even just the new line from the out_write, which I think means it won't be shown.

EDIT: Assuming that works, you can then start moving it into with your other plugins, but I found that leaving it there whilst I was actually developing made more sense. I eventually moved it into plugged, once I had actually started using it by symlinking to my git folder from inside plugged.






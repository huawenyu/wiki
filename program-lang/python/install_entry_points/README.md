# Doc
https://amir.rachum.com/blog/2017/07/28/python-entry-points/

Most people know entry points as the little snippet that you put in your setup.py file to
make your package available as a script on the command line, but they can be used for so much
more. I’m going to show you how to use entry points as a modular plug-in architecture. This
is super useful if you want to let other people write Python packages that interact or add
abilities to your existing Python package at runtime.

# version

    $ pip install --editable .

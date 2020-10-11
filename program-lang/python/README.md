# Install python3.8

    $ sudo apt install python3.8
    $ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2
    $ sudo update-alternatives --config python3

## Install Error

1. ImportError: cannot import name 'sysconfig' from 'distutils'
    $ sudo apt install python3-distutils
2. ModuleNotFoundError: No module named 'setuptools'
    $ sudo apt-get install python3-setuptools


# interactive command line

    $ sudo pip uninstall wheel prompt-toolkit docopt jedi pygments six wcwidth
    $ sudo pip install   wheel prompt-toolkit docopt jedi pygments six wcwidth

    $ sudo pip install ptpyton
    $ ptpython

# what's *args, **kwargs

To better explain the concept of *args and **kwargs (you can actually change these names):

def f(*args, **kwargs):
   print 'args: ', args, ' kwargs: ', kwargs

>>> f('a')
args:  ('a',)  kwargs:  {}
>>> f(ar='a')
args:  ()  kwargs:  {'ar': 'a'}
>>> f(1,2,param=3)
args:  (1, 2)  kwargs:  {'param': 3}

# what's setup.py

https://stackoverflow.com/questions/1471994/what-is-setup-py#:~:text=setup.py%20is%20a%20python,%24%20pip%20install%20.

## Import a module from a relative path

https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time
https://stackoverflow.com/questions/279237/import-a-module-from-a-relative-path

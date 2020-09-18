
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

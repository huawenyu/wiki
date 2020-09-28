# https://stackoverflow.com/questions/3779915/why-does-python-setup-py-sdist-create-unwanted-project-egg-info-in-project-r
# Install pyton2:
#   python setup.py develop
#   <or>
#   pip install --editable .
# Install pyton3:
#   python3 setup.py develop
#   <or>
#   pip3 install --editable .
# Uninstall:
#   python  setup.py clean
#   python3 setup.py clean
#
import os
from setuptools import setup, Command

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info ./__pycache__')


setup(
    name='snek',
    install_requires=['docopt',],
    entry_points={
        'console_scripts': [
            'snek = snek:main',
        ],
       'snek_types': [
           'normal = snek:normal_snek',
           'fancy = snek:fancy_snek',
       ],
    },
    cmdclass={
        'clean': CleanCommand,
    }

)


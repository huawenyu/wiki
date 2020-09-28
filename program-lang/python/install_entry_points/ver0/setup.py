# https://stackoverflow.com/questions/3779915/why-does-python-setup-py-sdist-create-unwanted-project-egg-info-in-project-r
# Install:
#   python setup.py build
#   <or>
#   pip install --editable .
# Uninstall:
#   python setup.py clean
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
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')

setup(
    name='snek',
    entry_points={
        'console_scripts': [
            'snek = snek:main',
        ],
    },
    cmdclass={
        'clean': CleanCommand,
    }
)


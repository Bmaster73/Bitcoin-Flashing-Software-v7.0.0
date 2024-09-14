import os
import shutil
import sys
import zipfile
import platform

from distutils.core import setup
from distutils.sysconfig import get_python_lib
import py2exe

version = __import__('p2pool').__version__
im64 = '64' in platform.architecture()[0]

extra_includes = []
import p2pool.networks
extra_includes.extend(f'p2pool.networks.{x}' for x in p2pool.networks.nets)
import p2pool.bitcoin.networks
extra_includes.extend(f'p2pool.bitcoin.networks.{x}' for x in p2pool.bitcoin.networks.nets)

# Create a temporary __init__.py file
init_file = os.path.join('p2pool', '__init__.py')
init_bak = 'INITBAK'
if os.path.exists(init_bak):
    os.remove(init_bak)
os.rename(init_file, init_bak)
try:
    with open(init_file, 'w') as f:
        f.write(f'__version__ = {version!r}\nDEBUG = False\n')
    # ... rest of the code ...

    # Create the distribution directory
    dir_name = f'p2pool_win{64 if im64 else 32}_{version}'
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.rename('dist', dir_name)

    # Create a zip file
    with zipfile.ZipFile(f'{dir_name}.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
        for dirpath, dirnames, filenames in os.walk(dir_name):
            for filename in filenames:
                zf.write(os.path.join(dirpath, filename))

    print(dir_name)

finally:
    # Restore the original __init__.py file
    os.remove(init_file)
    os.rename(init_bak, init_file)
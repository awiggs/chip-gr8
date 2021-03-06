from os.path    import join
from os         import listdir
from setuptools import setup, Extension, find_packages

with open('./chipgr8/VERSION.txt') as f:
    VERSION = f.read()

with open('./README.md') as f:
    description = f.read()

libchip_gr8 = Extension(
    name         = 'chipgr8.libchip_gr8',
    language     = 'c',
    include_dirs = ['includes'],
    sources      = ['src/chip8.c', 'src/ops.c'],
)

setup(
    name                          = 'chipgr8',
    version                       = VERSION,
    description                   = 'Chip 8 Emulation for AI',
    long_description              = description,
    long_description_content_type = 'text/markdown',
    author                        = 'chipgr8',
    author_email                  = 'root@ejrbuss.net',
    license                       = 'MIT',
    url                           = 'https://awiggs.github.io/chip-gr8/',
    packages                      = find_packages(),
    package_data                  = { 'chipgr8': ['*.txt', 'data/*/*', 'data/*'] },
    ext_modules                   = [libchip_gr8],
    install_requires              = [
        'lazyarray',
        'numpy',
        'pygame',
    ],
)
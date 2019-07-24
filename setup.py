from os.path    import join
from os         import listdir
from setuptools import setup, Extension, find_packages
from chipgr8    import VERSION, DESCRIPTION

with open('./README.md') as file:
    long_description = file.read()

libchip_gr8 = Extension(
    name         = 'chipgr8.libchip_gr8',
    include_dirs = ['./includes'],
    sources      = ['./src/chip8.c', './src/ops.c'],
)

setup(
    name                          = 'chipgr8',
    version                       = VERSION,
    description                   = DESCRIPTION,
    long_description              = long_description,
    long_description_content_type = 'text/markdown',
    author                        = 'Chip-Gr8 team',
    author_email                  = 'root@ejrbuss.net',
    license                       = 'MIT',
    url                           = 'https://awiggs.github.io/chip-gr8/',
    include_package_data          = True,
    packages                      = find_packages(),
    package_data                  = { 'chipgr8': ['data/*/*'] },
    ext_modules                   = [libchip_gr8],
    install_requires              = [
        'lazyarray',
        'numpy',
        'pygame',
    ],
)
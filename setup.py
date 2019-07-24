from os.path    import join
from os         import listdir
from setuptools import setup, Extension, find_packages

with open('./README.md') as file:
    description = file.read()

libchip_gr8 = Extension(
    name         = 'chipgr8.libchip_gr8',
    include_dirs = ['./includes'],
    sources      = ['./src/chip8.c', './src/ops.c'],
)

setup(
    name                          = 'chipgr8',
    version                       = '0.0.3',
    description                   = 'Chip 8 Emulation for AI',
    long_description              = description,
    long_description_content_type = 'text/markdown',
    author                        = 'chipgr8',
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
from os.path    import join
from os         import listdir
from setuptools import setup, Extension

with open('./README.md') as file:
    description = file.read()


libchip_gr8 = Extension(
    name         = 'chipgr8.libchip-gr8',
    include_dirs = ['./includes'],
    sources      = ['./src/chip8.c', './src/ops.c'],
)

setup(
    name             = 'chipgr8',
    version          = '0.0.1',
    description      = 'Chip 8 Emulation for AI',
    author           = 'chipgr8',
    author_email     = 'root@ejrbuss.net',
    license          = 'MIT',
    url              = 'https://awiggs.github.io/chip-gr8/',
    packages         = ['chipgr8', 'chipgr8.games'],
    package_data     = { 'chipgr8': ['data/*/*'] },
    long_description = description,
    ext_modules      = [libchip_gr8],
    install_requires = [
        'lazyarray',
        'numpy',
        'pygame',
    ],
)
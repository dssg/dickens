import re
from pathlib import Path
from distutils.core import setup

MODULE = 'descriptors'
MODULE_FILE = MODULE + '.py'
SRC_DIR = 'src'
MODULE_PATH = Path(__file__).parent / SRC_DIR / MODULE_FILE
README_PATH = Path(__file__).parent / 'README.rst'
VERSION = re.search(
    r'''^__version__ *= *["']([.\d]+)["']$''',
    MODULE_PATH.read_text(),
    re.M,
).group(1)

setup(
    name='Dickens',
    version=VERSION,
    description="Additional decorators implementing the descriptor interface",
    long_description=README_PATH.read_text(),
    author="Center for Data Science and Public Policy",
    author_email='datascifellows@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    url="https://github.com/dssg/dickens",
    package_dir={'': SRC_DIR},
    py_modules=[MODULE],
)

import pathlib
from setuptools import find_packages, setup

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
	name = 'nanome',
	packages=find_packages(exclude=["testing","doc"]),
	version = '0.1.0',
	license='MIT',
	description = 'Python API for Nanome Plugins',
	long_description = README,
    long_description_content_type = "text/markdown",
	author = 'Nanome',
	author_email = 'hello@nanome.ai',
	url = 'https://github.com/nanome-ai/nanome',
	keywords = ['virtual-reality', 'chemistry', 'python', 'api', 'plugin'],
	install_requires=[],
	classifiers=[
		'Development Status :: 3 - Alpha',

		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering :: Chemistry',

		'License :: OSI Approved :: MIT License',

		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
	],
)
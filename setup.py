from distutils.core import setup
setup(
	name = 'nanome',
	packages = ['nanome'],
	version = '0.0.1',
	license='MIT',
	description = 'Python API for Nanome Plugins',
	author = 'Nanome',
	author_email = 'hello@nanome.ai',
	url = 'https://github.com/nanome-ai/nanome',
	download_url = 'https://github.com/nanome-ai/nanome/archive/v0.0.1.tar.gz',
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
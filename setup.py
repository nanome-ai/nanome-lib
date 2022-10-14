from setuptools import find_packages, setup
import os

README_PATH = os.path.join(os.path.dirname(__file__), "README.md")
with open(README_PATH, 'r') as f:
    README = f.read()

setup(
    name='nanome',
    packages=find_packages(exclude=["testing", "doc", "test_plugins"]),
    version='0.38.8',
    license='MIT',
    description='Python API for Nanome Plugins',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Nanome',
    author_email='hello@nanome.ai',
    url='https://github.com/nanome-ai/nanome',
    platforms="any",
    keywords=['virtual-reality', 'chemistry', 'python', 'api', 'plugin'],
    install_requires=[
        'tblib==1.7.0',
        'graypy==2.1.0'
    ],
    extras_require={
        'schemas': [
            'marshmallow==3.15.0'
        ]
    },
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
    entry_points={"console_scripts": [
        "nanome-setup-plugins = nanome.setup_config:main",
        "nanome-plugin-init = nanome.plugin_init:main"
    ]},
    package_data={
        "nanome": [
            "_internal/_process/_external/_dssp/*",
            "plugin-template.zip"
        ]
    },
)

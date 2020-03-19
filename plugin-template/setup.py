import pathlib
from setuptools import find_packages, setup

README = (pathlib.Path(__file__).parent / 'README.md').read_text()

setup(
    name='{{command}}',
    packages=find_packages(),
    version='{{version}}',
    license='MIT',
    description='{{description}}',
    long_description=README,
    long_description_content_type='text/markdown',
    author='{{author}}',
    author_email='{{email}}',
    url='{{repo}}',
    platforms='any',
    keywords=['virtual-reality', 'chemistry', 'python', 'api', 'plugin'],
    install_requires=['nanome'],
    entry_points={'console_scripts': ['{{command}} = {{folder}}.{{class}}:main']},
    classifiers=[
        # 'Development Status :: 3 - Alpha',

        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    package_data={
        '{{folder}}': []
    },
)

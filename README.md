# Nanome

This library allows users to create Python plugins for Nanome VR Molecular Design Software (https://nanome.ai/)

![gif-1](https://media.giphy.com/media/RfZhOVwyp4GS8tBbNr/giphy-downsized.gif)


### Examples

Check out our other repositories to see plugin examples ([docking](https://github.com/nanome-ai/plugin-docking), for instance)

### Installation

In order to use Nanome Plugin API, you need Python 3.5+ or 2.7+
To install the library, run:

```sh
$ pip install nanome
```

As of version 0.38.0, we provide schemas for serializing nanome API objects in JSON. To use these, install with:
```sh
$ pip install nanome[schemas]
```

Some modules in the `beta` folder require extra dependencies. To install these, run:
```sh
$ pip install nanome[beta]
```

### Documentation

All documentation needed to use this package is available at [Read The Docs](https://nanome.readthedocs.io/en/latest/)

#### Building Docs
```sh
pip install sphinx sphinx_rtd_theme
cd doc
make html
# start server to serve html docs
cd build/html
python -m http.server 8000
``` 


### License

MIT
Helmholtz-Coil-Simulator
========================

A very simple Helmholtz coil simulator I made for my physics exam in early 2013.

It is well-organized, but only very lightly commented. I made it before i learned about the object-oriented programming.

There are 4 versions:
* main.py
* main_grid.py
* main_grid_threaded.py
* main_grid_threaded_layer.py

A basic rule: the shorter the name, the earlier the version.

main_grid_threaded_layer.py should be bug-free and I have tested it on multiple computers running OS X, Linux and Windows. The earlier version are mostly to see the iteration of the software and help to understand the code.

Update
======

I updated the code to Python 3, `vpython` and `numpy`. See `main_numpy.py`. It runs a lot faster, and should be slightly more understandable. Both `vpython` and `numpy` can be installed through pip: `pip3 install vpython numpy`.

<img src="https://github.com/Baekalfen/Helmholtz-Coil-Simulator/raw/master/pic.png">

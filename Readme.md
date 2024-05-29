Fixes symmetry for Vintage Story model files. Intended for bilaterally symmetric entities such as animals.

Currently just aligns central boxes, does not touch left/right pieces.

Usage:

`python3 vsmodelcenterer.py [input file or folder]`

Files will be modified in-place.

If you don't have pyjson5, you will need to install it:

`pip3 install pyjson5`

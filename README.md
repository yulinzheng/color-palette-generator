# color-palette-generator
A Python script that finds the dominant colors of an given image, and generates a color palette concatenated with the original image. See examples below:

Input image:

Output image:

Input image:

Output image:

Input image:

Output image:

## Prerequisites
1. Create a virtual environment and activate it:
```
$ python3 -m venv .venv
$ source .venv/bin/activate
```
2.  Install all dependencies:
```
(.venv) $ pip install -r requirements.txt
```

## Running and Testing
Run the generator with an input image:
```
(.venv) $ python generator.py /path/to/image
```
Optional: specify the number of clusters. The default is 5:
```
(.venv) $ python generator.py /path/to/image 7
```
Deactivate virtual environment if needed:
```
(.venv) $ deactivate
```
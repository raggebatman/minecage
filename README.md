# [minecage](https://youtu.be/vTLWIi7Wl1M?t=84)
This Python script is made for Minecraft and is capable of reading a selection of Java Archive files, taking all images in them, overlaying an image, then creating a resource pack from that. Works with mods too since they're structured the same way as any other Minecraft JAR. 

Tested and working on Windows 10 and Arch Linux.

## usage
Depends on [Pillow](https://python-pillow.org/), comes with argparse so it's a little easier to use from the command line. 
```
usage: minecage.py [-h] --source PATH [PATH ...] --destination PATH --image PATH --version PACK_FORMAT [--grayscale 0-255] [--scale {1,2,4,8,16}] [--mode {overlay,blend,overlay-masked,blend-masked}] [-v]

optional arguments:
  -h, --help            show this help message and exit
  --grayscale 0-255
  --scale {1,2,4,8,16}
  --mode {overlay,blend,overlay-masked,blend-masked}
  -v, --verbose

required arguments:
  --source PATH [PATH ...]
  --destination PATH
  --image PATH
  --version PACK_FORMAT
```

#### source
The source paths for the JAR files to use.
Can be relative or absolute.
Separated by spaces, useful for also converting mod JARs.

#### destination
The destination directory for the output.
Can be relative or absolute.

#### image
The path for the image to overlay with.
Can be relative or absolute.
Maybe I could've implemented some feature to use several images and randomize which to use?
You're obviously welcome to modify and redistribute yourself :)

#### grayscale
Optional parameter for the blend modes.
Integer between 0 and 255, defaults to 128.
Sets how transparent the source image should be.

#### scale
Sets if the image should be resized.
Choice between 1, 2, 4, 8, 16, defaults to 1.
For example, 2 = 2x resolution.

#### modes
* `overlay`: Stretches to fit image
* `blend`: Same as overlay but with some transparency
* `overlay-masked`: Same as overlay but masked; fully transparent pixels don't get written to
* `blend-masked`: Same as blend but masked; fully transparent pixels don't get written to

### example: 2x overlay
`minecage.py --source 1.16.5.jar --destination D:\thefunny --image C:\Users\ragge\Pictures\bazinga.jpg --version 6 --scale 2 --mode overlay`

### example: 4x overlay-masked
`minecage.py --source ./1.16.5.jar --destination /home/ragge/Documents/thefunny --image /home/ragge/Images/thecage.jpg --version 6 --scale 4 --mode overlay-masked`

### example with mods: 4x blend "extra verbose"
`minecage.py --source 1.12.2.jar [TODO:add the ones i use] --destination /home/ragge/Documents/thefunny --image /home/ragge/Images/tux.png --version 3 --scale 4 --mode blend`

### example with mods: 2x blend-masked "verbose"
`minecage.py --source 1.12.2.jar [TODO:add the ones i use] --destination /home/ragge/Documents/thefunny --image /home/ragge/Images/stallman.jpg --version 3 --scale 2 --mode blend-masked`

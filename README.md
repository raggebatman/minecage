# [minecage](https://youtu.be/vTLWIi7Wl1M?t=84)
Extract assets from Minecraft JAR files and overlay a source image on top of them, comes with some alternatives.
Generates a pack.mcmeta and pack.png.

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
`minecage.py --source 1.16.5.jar --destination ~/Documents/thefunny --image ~/Pictures/bazinga.png --version 6 --scale 2 --mode overlay`

The images are simply stretched to fit, lots of broken looking textures here
![bazinga.png](https://github.com/raggebatman/minecage/blob/main/examples/bazinga.png?raw=true)
![bazinga-title.png](https://github.com/raggebatman/minecage/blob/main/examples/bazinga-title.png?raw=true)

### example: 4x overlay-masked
`minecage.py --source ./1.16.5.jar --destination C:\User\username\Documents\thefunny --image C:\User\username\Pictures\thecage.png --version 6 --scale 4 --mode overlay-masked`

With this one you can see that it preserves the transparent pixels
![the_cage.png](https://github.com/raggebatman/minecage/blob/main/examples/the_cage.png?raw=true)
![the_cage-ingame.png](https://github.com/raggebatman/minecage/blob/main/examples/the_cage-ingame.png?raw=true)

### example with mods: 2x blend "verbose"
`minecage.py --source 1.12.2.jar OpenComputers-1.12.2.jar ~/Documents/Mekanism-1.12.2.jar --destination /home/user/Desktop/thefunny --image /home/user/Pictures/tux.png --version 3 --scale 2 --mode blend --verbose`

Outputs some information to the console.
Now you get the overlayed images but with some added transparency.

```
Appending ".jar" paths to array
Extracting ".png" images to "thefunny"
Processing images with "blend" at 2x resolution
1 files failed, 2443 files completed
```

![tux.png](https://github.com/raggebatman/minecage/blob/main/examples/tux.png?raw=true)

### example with mods: 4x blend-masked "extra verbose"
`minecage.py --source 1.12.2.jar ../Mekanism-1.12.2.jar OpenComputers-1.12.2.jar --destination "~/Richard Stallman/thefunny" --image ./stallman.jpg --version 3 --scale 4 --mode blend-masked -vv`

More information gets output to the console, it goes up to 3x (-vvv) and at that point it outputs every path it's processing.
With this you get both the transparency and proper backgrounds, best for playability in my opinion.

```
Appending ".jar" paths to array
Processing "1.12.2.jar"
Processing "OpenComputers-1.12.2.jar"
Processing "Mekanism-1.12.2.jar"
Extracting ".png" images to "thefunny"
Extracting "1.12.2.jar"
Extracting "OpenComputers-1.12.2.jar"
Extracting "Mekanism-1.12.2.jar"
Processing images with "blend-masked" at 4x resolution
1 files failed, 2443 files completed
```

![stallman.png](https://github.com/raggebatman/minecage/blob/main/examples/stallman.png?raw=true)

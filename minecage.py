#!/usr/bin/python3

import os, argparse, json
from zipfile import ZipFile, is_zipfile
from PIL import Image
from io import BytesIO

parser = argparse.ArgumentParser()

required = parser.add_argument_group("required arguments")

required.add_argument("--source", metavar="PATH", action="extend", nargs="+", type=str, required=True)
required.add_argument("--destination", metavar="PATH", type=str, required=True)
required.add_argument("--image", metavar="PATH", type=str, required=True)
required.add_argument("--version", metavar="PACK_FORMAT", type=int, required=True)

parser.add_argument("--grayscale", metavar="0-255", type=int, default=128)
parser.add_argument("--scale", type=int, default=1, choices=[1, 2, 4, 8, 16])
parser.add_argument("--mode", type=str, default="blend-masked", choices=["overlay", "blend", "overlay-masked", "blend-masked"])
parser.add_argument("-v", "--verbose", action="count")

args = parser.parse_args()

if os.path.isdir(args.destination):
    print(f"Destination directory \"{args.destination}\" already exists.")
    quit()

if not os.path.isfile(args.image):
    print(f"Image path \"{args.image}\" does not exist.")
    quit()

if args.grayscale < 0 or args.grayscale > 255:
    print(f"Arg grascale \"{args.grayscale}\" is out of range.")
    quit()

# Print index of argument
# based on verbosity from parser
# Returns True if successful
def printverbose(*arguments):
    if not args.verbose: return False
    i = len(arguments) - 1 if args.verbose > len(arguments) else args.verbose - 1
    if arguments[i]: print(arguments[i])
    return True

# Change every pixel on img_obj with
# a value above 0 (black) to 255 (white) or args.grayscale for blend modes
# The goal is to preserve fully transparent (0 value) pixels
def generate_mask(img_obj, pixel_value=255):
    img_obj = img_obj.convert("L")
    for x in range(img_obj.width):
        for y in range(img_obj.height):
            if not img_obj.getpixel((x,y)) == 0:
                img_obj.putpixel((x,y), pixel_value)
    return img_obj

# Loop through args.source arguments
# If file, append ".jar" path to jars[]
# If directory, recurse through and
# append ".jar" paths to jars[]
jars = []
printverbose("Appending \".jar\" paths to array")
for path in args.source:
    printverbose(None, f"Processing \"{path}\"")
    if os.path.isfile(path):
        if path.endswith(".jar") and is_zipfile(path):
            jars.append(path)
            printverbose(None, None, path)
    elif os.path.isdir(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                f = os.path.join(dirpath, filename)
                if filename.endswith(".jar") and is_zipfile(f):
                    jars.append(f)
                    printverbose(None, None, f)
    else:
        raise Exception(f"invalid argument \"{path}\"")

# Open each ".jar" file from jars[]
# and extract ".png" files to args.destination
# Checks if the assets directory is first, continues otherwise
# Also skips "unicode_page", adds to the 
# execution time and doesn't work anyways :)
printverbose(f"Extracting \".png\" images to \"{args.destination}\"")
for jar in jars:
    printverbose(None, f"Extracting \"{jar}\"")
    with ZipFile(jar, "r") as zip:
        for filename in zip.namelist():
            if filename.endswith(".png") and os.path.normpath(filename).split(os.sep)[0] == "assets" and not "unicode_page" in filename:
                printverbose(None, None, filename)
                zip.extract(filename, args.destination)

# Recursively iterate everything inside args.destination
# Process the images based on args.mode and args.scale
# Image width/height gets multiplied by args.scale
# Try/Except/Finally for mishaps
# args.mode:
# overlay > Resizes args.image and saves it
# blend > Creates a args.grayscale grayscale image and masks it, ~50% transparency
# overlay-masked > Uses generate_mask()
# blend-masked > Uses generate_mask(pixel_value=args.grayscale), ~50% transparency
# composite > Image.composite()
printverbose(f"Processing images with \"{args.mode}\" at {args.scale}x resolution")
whoops = 0
successful = 0
for dirpath, dirnames, filenames in os.walk(args.destination):
    for i, filename in enumerate(filenames):
        try:
            f = os.path.join(dirpath, filename)
            printverbose(None, None, f)
            width, height = (i * args.scale for i in Image.open(f).size)

            if args.mode == "overlay":
                Image.open(args.image).resize((width, height), resample=Image.NEAREST).save(f)
            else:
                img_current = Image.open(f).resize((width, height), resample=Image.NEAREST).convert("RGBA")
                img_overlay = Image.open(args.image).resize((width, height), resample=Image.NEAREST)

                if args.mode == "blend":
                    img_mask = Image.new("L", (width, height), args.grayscale)
                elif args.mode == "blend-masked":
                    img_mask = generate_mask(img_current, args.grayscale)
                else:
                    img_mask = generate_mask(img_current)

                Image.composite(img_overlay, img_current, img_mask).save(f)
        except:
            whoops += 1
            pass
        finally:
            successful += 1

print(f"{whoops} files failed, {successful} files completed")

# Write "pack.mcmeta"
with open(os.path.join(args.destination, "pack.mcmeta"), "w") as f:
    json.dump({"pack":{"pack_format":args.version,"description":f"{args.scale}x {args.mode}\npain"}}, f, indent=2)

# Write "pack.png"
Image.open(args.image).resize((16 * args.scale, 16 * args.scale), resample=Image.NEAREST).save(os.path.join(args.destination, "pack.png"))

__help__ = \
'''
Notchout is a simple Python script which generates a solid color wallpaper image with a mysterious black bar on the top of it.

e.g. python notchout.py -c #C0FFEE ~/Pictures/Wallpaper.png
'''


import AppKit

import PIL
import PIL.Image
import PIL.ImageColor

import click
import numpy as np
import os
import sys


def screensize(screen=0, width=None, height=None):

    screens = AppKit.NSScreen.screens()

    screen = sorted((0, screen, len(screens) - 1))[1]
    screen = screens[screen]

    frame = screen.frame()
    scale = screen.backingScaleFactor()

    width = int(width or frame.size.width * scale)
    height = int(height or frame.size.height * scale)

    return width, height


def rgbcolor(hexcolor):

    return PIL.ImageColor.getcolor(hexcolor, 'RGB')


def save(image, path):

    PIL.Image.fromarray(image, 'RGB').save(path)


@click.command(help=__help__)
@click.argument('path', default='notchout.png')
@click.option('-s', '--screen', default=1, help='Screen index for auto image size detection. (1)')
@click.option('-w', '--width', default=0,  help='Image width.  (auto)')
@click.option('-h', '--height', default=0, help='Image height. (auto)')
@click.option('-n', '--notch', default=74, help='Notch height. (74)')
@click.option('-c', '--color', default='#191919', help='Color code.   (#191919)')
def notchout(path, screen, width, height, notch, color):

    try:

        path = os.path.abspath(os.path.expanduser(path))
        screen -= 1
        width, height = screensize(screen=screen, width=width, height=height)
        color = rgbcolor(color)

        click.echo(f'Creating image of size {width} x {height}')
        image = np.zeros((height, width, 3), dtype=np.uint8)

        click.echo(f'Filling image with color {color}')
        click.echo(f'Masking notch of height {notch}')
        image[notch:, :] = color

        click.echo(f'Writing image to {path}')
        save(image, path)

    except Exception as exception:

        click.echo(str(exception), err=True)
        sys.exit(1)


if __name__ == '__main__':

    notchout()

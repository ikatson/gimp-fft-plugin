#!/usr/bin/env python

import sys

from gimpfu import *

# A trick to let GIMP use numpy installed into the system.
# Installing numpy into gimp's python is tricky, so this life easier.
sys.path.append("/usr/local/lib/python2.7/site-packages/")

import numpy as np


def rescale(arr, min_val, max_val):
    """Rescale numpy array linearly to grow from new min to new max."""
    arrmin = arr.min()
    arrmax = arr.max()
    return (arr - arrmin) / (arrmax - arrmin) * (max_val - min_val) + min_val


def drawable_to_channels(drawable):
    """Convert GIMP drawable to a list of channels as numpy arrays."""
    rgn = drawable.get_pixel_rgn(0, 0, drawable.width, drawable.height)
    buf = np.frombuffer(rgn[:, :], dtype=np.uint8)
    channels = []
    for c in range(drawable.bpp):
        channels.append(
            buf[c :: drawable.bpp].reshape((drawable.height, drawable.width))
        )
    return channels


def forward_fft(image, drawable):
    """The actual GIMP runnable to run forward FFT and create a layer from it."""
    gimp.progress_init("FFT")
    channels = drawable_to_channels(drawable)

    for idx in range(len(channels)):
        chan = channels[idx]

        fft = np.abs(np.fft.fft2(chan))
        fft_display = rescale(np.log(fft), 0, 256).astype(np.uint8)
        channels[idx] = fft_display

        gimp.progress_update((float(idx) + 1) / len(channels))

    new_layer_data = np.stack(channels, axis=-1)

    layer = gimp.Layer(
        image,
        "FFT",
        image.width,
        image.height,
        image.active_layer.type,
        100,
        NORMAL_MODE,
    )
    region = layer.get_pixel_rgn(0, 0, layer.width, layer.height, True)

    region[:, :] = new_layer_data.tobytes()
    layer.flush()
    image.add_layer(layer, 0)
    gimp.displays_flush()

    # workaround for progress bar not disappearing.
    gimp.progress_init()


register(
    "FFT",
    "Forward FFT",
    "This will create a new layer with FFT of the image. For now there's no way to reverse it back.",
    "Igor Katson",
    "Igor Katson",
    "2019",
    "Forward fast Fourier transform",
    "*",
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "layer", "Input layer", None),
    ],
    [],
    forward_fft,
    menu="<Image>/Filters/FFT/",
)

main()

# FFT plugin for gimp.

This is an experiment on how to write a plugin for GIMP that will use system libraries.

Inside is an FFT transform that is lossy, i.e. it's just there for display purposes and there's no way to reverse it. For now at least (2019-09).

# Installation and usage.

1. Install python2 and numpy
2. Modify the script if your python2 is not in /usr/local/
3. Add the folder with the plugin to GIMP plugin search path and restart GIMP.
4. Run from Filters/FFT.

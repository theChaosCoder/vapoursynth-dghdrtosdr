# vapoursynth-dghdrtosdr

This Avisynth+/Vapoursynth filter converts HDR10 PQ or HLG from UHD blurays
to 8-bit SDR YV12 or 10-bit SDR stored in YUV420P16. The input must be
YUV420P16, e.g., from DGSource() with a HDR10 source stream.

This filter runs on both CUDA and in software mode. If you try to run
in CUDA mode without an nVidia card and driver installed, you will get
an error. Use the parameter impl="sw" to run in software mode.

Copyright (c) 2018-2024 Donald A. Graft, All Rights Reserved

## Support
   
   - **Questions about the plugin itself**:
     post in the [Forum](https://www.rationalqm.us/board/) where the author of the plugin and other users may help.
   - **Problems with this PyPI package** (installation, wheel build,
     missing files): open an issue on [GitHub](https://github.com/theChaosCoder/vapoursynth-dghdrtosdr).

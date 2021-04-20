#!/bin/bash

python3 $HOME/Documents/scripts/multicamera_color_image_capture.py
python3 $HOME/Documents/scripts/multicamera_infrared_image_capture.py
python3 $HOME/Documents/scripts/multicamera_depth_image_capture.py
python3 $HOME/Documents/scripts/multicamera_ply_capture.py

exit 0

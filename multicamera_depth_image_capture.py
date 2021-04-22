import pyrealsense2 as rs
import numpy as np
import os
import cv2
from pathlib import Path
from datetime import datetime

# check the number of connected devices
devices_ = rs.context().query_devices()
print('Found {} connected devices'.format(len(devices_)))

serial_numbers = []
for dev_ in devices_:
    serial_numbers.append(dev_.get_info(rs.camera_info.serial_number))

pipelines = []
configs = []
for idx in range(len(devices_)):
    pipelines.append(rs.pipeline())
    configs.append(rs.config())
    configs[idx].enable_device(serial_numbers[idx])
    configs[idx].enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    pipelines[idx].start(configs[idx])

today = datetime.now().strftime('%d_%m_%Y')
time_execution = datetime.now().strftime('%H_%M_%S')
root_folder = os.path.join(str(Path.home()), 'Documents', 'data', today)
if not os.path.exists(root_folder):
    os.makedirs(root_folder)
save_image = True
current_idx = None
try:
    for idx in range(len(devices_)):
        current_idx = idx
        frames = pipelines[idx].wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            print('No data received')
            continue
        
        # convert images to numpy array
        depth_image = np.asanyarray(depth_frame.get_data())

        # apply colormap
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        
        if save_image:
            img_folder = os.path.join(root_folder, serial_numbers[idx], 'depth')
            if not os.path.exists(img_folder):
                os.makedirs(img_folder)
            cv2.imwrite(os.path.join(img_folder, 'depth_camera__{}__{}__{}.png'.format(serial_numbers[idx], today, time_execution)), depth_colormap)
        
except:
    print('Error with camera: {} S/N: {}'.format(current_idx + 1, serial_numbers[current_idx]))
finally:
    for idx in range(len(devices_)):
        pipelines[idx].stop()
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
    configs[idx].enable_stream(rs.stream.infrared, 640, 480, rs.format.y8, 30)
    pipelines[idx].start(configs[idx])

today = datetime.now().strftime('%d_%m_%Y')
time_execution = datetime.now().strftime('%H_%M_%S')
root_folder = os.path.join(str(Path.home()), 'Documents', 'data', 'infrared', today)
if not os.path.exists(root_folder):
    os.mkdir(root_folder)
save_image = True
current_idx = None
try:
    for idx in range(len(devices_)):
        current_idx = idx
        frames = pipelines[idx].wait_for_frames()
        infrared_frame = frames.get_infrared_frame()
        if not infrared_frame:
            print('No data received')
            continue
        
        # convert images to numpy array
        infrared_image = np.asanyarray(infrared_frame.get_data())

        if save_image:
            cv2.imwrite(os.path.join(root_folder, 'infrared_camera_{}_{}.png'.format(serial_numbers[idx], time_execution)), infrared_image)
except:
    print('Error with camera: {} S/N: {}'.format(current_idx + 1, serial_numbers[current_idx]))
finally:
    for idx in range(len(devices_)):
        pipelines[idx].stop()
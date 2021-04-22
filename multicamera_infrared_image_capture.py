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
root_folder = os.path.join(str(Path.home()), 'Documents', 'data', today)
if not os.path.exists(root_folder):
    os.makedirs(root_folder)
save_image = True
current_idx = None
created_files = []
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
            img_folder = os.path.join(root_folder, serial_numbers[idx], 'infrared')
            if not os.path.exists(img_folder):
                os.makedirs(img_folder)
            filename = os.path.join(img_folder, 'infrared_camera__{}__{}__{}.png'.format(serial_numbers[idx], today, time_execution))
            cv2.imwrite(filename, infrared_image)
            created_files.append(filename)
except:
    print('Error with camera: {} S/N: {}'.format(current_idx + 1, serial_numbers[current_idx]))
finally:
    for idx in range(len(devices_)):
        pipelines[idx].stop()

if len(created_files) > 0:
    log_file = os.path.join(str(Path.home()), 'Documents', 'data', 'to_process_infrared.txt')
    with open(log_file, 'w') as filehandle:
        filehandle.writelines("%s\n" % value for value in created_files)
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
sensors = []

for idx in range(len(devices_)):
    pipelines.append(rs.pipeline())
    configs.append(rs.config())
    configs[idx].enable_device(serial_numbers[idx])
    configs[idx].enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
    pipelines[idx].start(configs[idx])
    sensors.append(pipelines[idx].get_active_profile().get_device().query_sensors()[1])
    sensors[idx].set_option(rs.option.enable_auto_exposure, True)

today = datetime.now().strftime('%d_%m_%Y')
time_execution = datetime.now().strftime('%H_%M_%S')
root_folder = os.path.join(str(Path.home()), 'Documents', 'data', today)
if not os.path.exists(root_folder):
    os.makedirs(root_folder)
save_image = False
current_idx = None
cnt = 0
limit = 100
created_files = []
try:
    while cnt < limit:
        if cnt == limit - 1:
            save_image = True
        for idx in range(len(devices_)):
            current_idx = idx
            frames = pipelines[idx].wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                print('No data received')
                continue
            
            # convert images to numpy array
            color_image = np.asanyarray(color_frame.get_data())
            
            if save_image:
                img_folder = os.path.join(root_folder, serial_numbers[idx], 'color')
                if not os.path.exists(img_folder):
                    os.makedirs(img_folder)
                filename = os.path.join(img_folder, 'color_camera__{}__{}__{}.png'.format(serial_numbers[idx], today, time_execution))
                cv2.imwrite(filename, color_image)
                created_files.append(filename)
        cnt += 1
except:
    print('Error with camera: {} S/N: {}'.format(current_idx + 1, serial_numbers[current_idx]))
finally:
    for idx in range(len(devices_)):
        pipelines[idx].stop()

if len(created_files) > 0:
    log_file = os.path.join(str(Path.home()), 'Documents', 'data', 'to_process_color.txt')
    with open(log_file, 'w') as filehandle:
        filehandle.writelines("%s\n" % value for value in created_files)
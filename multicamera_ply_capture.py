import pyrealsense2 as rs
import os
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

colorizer = rs.colorizer()

today = datetime.now().strftime('%d_%m_%Y')
time_execution = datetime.now().strftime('%H_%M_%S')
root_folder = os.path.join(str(Path.home()), 'Documents', 'data', today)
if not os.path.exists(root_folder):
    os.makedirs(root_folder)
current_idx = None
try:
    for idx in range(len(devices_)):
        current_idx = idx
        frames = pipelines[idx].wait_for_frames()
        colorized = colorizer.process(frames)

        # Create save_to_ply object
        ply_folder = os.path.join(root_folder, serial_numbers[idx], 'pointcloud')
        if not os.path.exists(ply_folder):
            os.makedirs(ply_folder)
        ply = rs.save_to_ply(os.path.join(ply_folder, 'pointcloud_camera__{}__{}__{}.ply'.format(serial_numbers[idx], today, time_execution)))

        # Set options to the desired values
        ply.set_option(rs.save_to_ply.option_ply_binary, True)
        ply.set_option(rs.save_to_ply.option_ply_normals, True)

        # Apply the processing block to the frameset which contains the depth frame and the texture
        ply.process(colorized)
except:
    print('Error with camera: {} S/N: {}'.format(current_idx + 1, serial_numbers[current_idx]))
finally:
    for idx in range(len(devices_)):
        pipelines[idx].stop()
import pyrealsense2 as rs
import time

# check the number of connected devices
while True:
    devices_ = rs.context().query_devices()
    print('Found {} connected devices'.format(len(devices_)))
    for idx, dev_ in enumerate(devices_):
        print('Camera {}: S/N: {}'.format(idx + 1, dev_.get_info(rs.camera_info.serial_number)))
    print('-' * 10)
    time.sleep(3.)
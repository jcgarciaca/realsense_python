import pyrealsense2 as rs
import numpy as np
import cv2
import time

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

save_image = False
current_idx = None
try:
    while True:
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
                cv2.imwrite('images/infrared_camera_{}.png'.format(idx + 1), infrared_image)

            # show image
            cv2.namedWindow('Infrared Image Cam {}'.format(serial_numbers[idx]), cv2.WINDOW_NORMAL)
            cv2.imshow('Infrared Image Cam {}'.format(serial_numbers[idx]), infrared_image)
        
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
        
except:
    print('Error with camera: {} S/N: {}'.format(current_idx + 1, serial_numbers[current_idx]))
finally:
    for idx in range(len(devices_)):
        pipelines[idx].stop()
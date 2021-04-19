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
sensors = []

for idx in range(len(devices_)):
    pipelines.append(rs.pipeline())
    configs.append(rs.config())
    configs[idx].enable_device(serial_numbers[idx])
    configs[idx].enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
    pipelines[idx].start(configs[idx])
    sensors.append(pipelines[idx].get_active_profile().get_device().query_sensors()[1])
    sensors[idx].set_option(rs.option.enable_auto_exposure, True)

save_image = False
try:
    while True:
        for idx in range(len(devices_)):
            frames = pipelines[idx].wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                print('No data received')
                continue
            
            # convert images to numpy array
            color_image = np.asanyarray(color_frame.get_data())
            
            if save_image:
                cv2.imwrite('images/color_camera_{}.png'.format(idx + 1), color_image)

            # show image
            cv2.namedWindow('Color Image Cam {}'.format(idx + 1), cv2.WINDOW_NORMAL)
            cv2.imshow('Color Image Cam {}'.format(idx + 1), color_image)
        
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
        
except:
    print('Error with camera')
finally:
    for idx in range(len(devices_)):
        pipelines[idx].stop()
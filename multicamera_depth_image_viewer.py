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
    configs[idx].enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    pipelines[idx].start(configs[idx])

save_image = False
try:
    while True:
        for idx in range(len(devices_)):
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
                cv2.imwrite('images/depth_camera_{}.png'.format(idx + 1), depth_colormap)

            # show image
            cv2.namedWindow('Depth Image Cam {}'.format(idx + 1), cv2.WINDOW_NORMAL)
            cv2.imshow('Depth Image Cam {}'.format(idx + 1), depth_colormap)
        
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
        
except:
    print('Error with camera')
finally:
    for idx in range(len(devices_)):
        pipelines[idx].stop()
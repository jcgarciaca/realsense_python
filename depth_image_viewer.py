import pyrealsense2 as rs
import numpy as np
import cv2
import time

rs.log_to_file(rs.log_severity.debug, file_path='./log.txt')
device = rs.context().devices[0]
serial_number = device.get_info(rs.camera_info.serial_number)
print('Camera serial number: {}'.format(serial_number))

pipeline = rs.pipeline()
config = rs.config()

pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
profile = pipeline.start(config)

save_image = False
try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            print('No data received')
            continue
        
        # convert images to numpy array
        depth_image = np.asanyarray(depth_frame.get_data())

        # apply colormap
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        
        print('depth_colormap shape', depth_colormap.shape)
        if save_image:
            cv2.imwrite('images/depth.png', depth_colormap)
        
        # show image
        cv2.namedWindow('Depth Image', cv2.WINDOW_NORMAL)
        cv2.imshow('Depth Image', depth_colormap)
        key = cv2.waitKey(1)

        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
except:
    print('Error with camera')
finally:
    pipeline.stop()
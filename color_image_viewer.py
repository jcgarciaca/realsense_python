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

config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
profile = pipeline.start(config)

sensor = pipeline.get_active_profile().get_device().query_sensors()[1]
sensor.set_option(rs.option.enable_auto_exposure, True)

save_image = False
try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            print('No data received')
            continue
        
        # convert images to numpy array
        color_image = np.asanyarray(color_frame.get_data())
        print('color_image shape', color_image.shape)
        
        if save_image:
            cv2.imwrite('images/color.png', color_image)

        # show image
        cv2.namedWindow('Color Image', cv2.WINDOW_NORMAL)
        cv2.imshow('Color Image', color_image)
        key = cv2.waitKey(1)

        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
        
except:
    print('Error with camera')
finally:
    pipeline.stop()
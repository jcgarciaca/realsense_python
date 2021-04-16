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

config.enable_stream(rs.stream.infrared, 640, 480, rs.format.y8, 30)
profile = pipeline.start(config)

save_image = False
try:
    while True:
        frames = pipeline.wait_for_frames()
        infrared_frame = frames.get_infrared_frame()
        if not infrared_frame:
            print('No data received')
            continue
                
        # convert images to numpy array
        infrared_image = np.asanyarray(infrared_frame.get_data())
        print('infrared_image shape', infrared_image.shape)
        if save_image:
            cv2.imwrite('images/infrared.png', infrared_image)
        
        # show image
        cv2.namedWindow('Infrared Image', cv2.WINDOW_NORMAL)
        cv2.imshow('Infrared Image', infrared_image)
        key = cv2.waitKey(1)

        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break

except:
    print('Error with camera')
finally:
    pipeline.stop()
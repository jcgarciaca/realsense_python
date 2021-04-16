import pyrealsense2 as rs
import numpy as np
import cv2
import time

rs.log_to_file(rs.log_severity.debug, file_path='./log.txt')
'''
# resetting
print('Resetting devices...')
ctx = rs.context()
devices = ctx.query_devices()
for dev in devices:
    dev.hardware_reset()
    time.sleep(1)

time.sleep(5.)
print('Done resetting')
'''
device = rs.context().devices[0]
serial_number = device.get_info(rs.camera_info.serial_number)
print('Camera serial number: {}'.format(serial_number))

pipeline = rs.pipeline()
config = rs.config()

pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

config.enable_stream(rs.stream.depth)#, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.rgb8, 30)

profile = pipeline.start(config)

sensor = pipeline.get_active_profile().get_device().query_sensors()[1]
sensor.set_option(rs.option.exposure, 1600.000)
# sensor.set_option(rs.option.enable_auto_exposure, True)
print('Setting parameters...')
time.sleep(5.)

#color_sensor = profile.get_device().query_sensors()[1]
#color_sensor.set_option(rs.option.enable_auto_exposure, True)

try:
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    if not depth_frame or not color_frame:
        print('No images received')
    else:
        # convert images to numpy array
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # apply colormap
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        color_image_dim = color_image.shape

        print('depth_colormap shape', depth_colormap.shape)
        print('color_image shape', color_image.shape)
        cv2.imwrite('images/color.png', color_image)
        cv2.imwrite('images/depth.png', depth_colormap)

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_image_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap))

        # show images
        cv2.namedWindow('RealSense Images', cv2.WINDOW_NORMAL)
        cv2.imshow('RealSense Images', images)
        cv2.waitKey(0)
finally:
    pipeline.stop()
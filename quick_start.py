import pyrealsense2 as rs

rs.log_to_file(rs.log_severity.debug, file_path='./log.txt')

device = rs.context().devices[0]
serial_number = device.get_info(rs.camera_info.serial_number)
print('Camera serial number: {}'.format(serial_number))

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

pipeline.start(config)
try:
    frames = pipeline.wait_for_frames()
    depth = frames.get_depth_frame()
    print('depth:', depth)
    print('')
    for f in frames:
        print(f.profile)
finally:
    pipeline.stop()
import pyrealsense2 as rs

rs.log_to_file(rs.log_severity.debug, file_path='./log.txt')

device = rs.context().devices[0]
serial_number = device.get_info(rs.camera_info.serial_number)
print('Camera serial number: {}'.format(serial_number))


# Declare pointcloud object, for calculating pointclouds and texture mappings
pc = rs.pointcloud()
# We want the points object to be persistent so we can display the last cloud when a frame drops
points = rs.points()

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth)

pipeline.start(config)
colorizer = rs.colorizer()

try:
    frames = pipeline.wait_for_frames()
    colorized = colorizer.process(frames)

    # Create save_to_ply object
    filepath = 'meshes/1.ply'
    ply = rs.save_to_ply(filepath)

    # Set options to the desired values
    ply.set_option(rs.save_to_ply.option_ply_binary, True)
    ply.set_option(rs.save_to_ply.option_ply_normals, True)

    print('Saving to {} ...'.format(filepath))
    # Apply the processing block to the frameset which contains the depth frame and the texture
    ply.process(colorized)
    print('Done')
finally:
    pipeline.stop()
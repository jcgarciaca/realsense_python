import pyrealsense2 as rs

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

colorizer = rs.colorizer()
save_image = False
current_idx = None
try:
    for idx in range(len(devices_)):
        current_idx = idx
        frames = pipelines[idx].wait_for_frames()
        colorized = colorizer.process(frames)

        # Create save_to_ply object
        ply = rs.save_to_ply('meshes/pointcloud_camera_{}.ply'.format(idx + 1))

        # Set options to the desired values
        ply.set_option(rs.save_to_ply.option_ply_binary, True)
        ply.set_option(rs.save_to_ply.option_ply_normals, True)

        # Apply the processing block to the frameset which contains the depth frame and the texture
        ply.process(colorized)
    print('Done')
except:
    print('Error with camera: {} S/N: {}'.format(current_idx + 1, serial_numbers[current_idx]))
finally:
    for idx in range(len(devices_)):
        pipelines[idx].stop()
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
    while True:
        frames = pipeline.wait_for_frames()
        depth = frames.get_depth_frame()
        if not depth: continue

        coverage = [0] * 64
        for y in range(480):
            for x in range(640):
                dist = depth.get_distance(x, y)
                if 0 < dist and dist < 1:
                    coverage[x // 10] += 1

            if y%20 is 19:
                line = ''
                for c in coverage:
                    line += ' .:nhBXWW'[c // 25]
                coverage = [0] * 64
                print(line)
    exit(0)
    pipeline.stop()
except Exception as e:
    print(e)
    pipeline.stop()
    pass

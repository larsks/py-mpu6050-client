from vispy import app
import argparse
import sensorclient
import outlined_cube

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--gyro', dest='inputs',
                   action='append_const', const='gyro')
    p.add_argument('--accel', dest='inputs',
                   action='append_const', const='accel')
    p.add_argument('--filtered', dest='inputs',
                   action='append_const', const='filtered')
    p.add_argument('--listen', '-l', default='0.0.0.0')
    p.add_argument('--yaw', '-y', action='store_true')

    p.set_defaults(inputs=None)
    return p.parse_args()

def main():
    args = parse_args()
    s = sensorclient.sensorclient(listen_addr=args.listen)

    if args.inputs is None or 'filtered' in args.inputs:
        c1 = outlined_cube.Canvas(sensor=s, i=0, 
                                  yaw=args.yaw, title='Filtered')
    if args.inputs is None or 'accel' in args.inputs:
        c2 = outlined_cube.Canvas(sensor=s, i=1,
                                  yaw=args.yaw, title='Accelerometer')
    if args.inputs is None or 'gyro' in args.inputs:
        c3 = outlined_cube.Canvas(sensor=s, i=2,
                                  yaw=args.yaw, title='Gyroscope')

    app.run()

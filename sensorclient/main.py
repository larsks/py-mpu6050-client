from vispy import gloo, app
import argparse
import sensorclient
import outlined_cube

def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument('sensor')

    return p.parse_args()

def main():
    args = parse_args()
    host, port = args.sensor.split(':')
    sensor = (host, int(port))
    s = sensorclient.SocketClient(sensor)
    c = outlined_cube.Canvas(sensor=s)
    app.run()

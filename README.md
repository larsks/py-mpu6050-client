# py-mpu6050-client

This package provides `sensorclient`, a [vispy][]-based tool for
visualiztion data from an MPU6050 6DOF IMU provided by the
[py-mpu6050][] project.

[vispy]: http://vispy.org/
[py-mpu6050]: https://github.com/larsks/py-mpu6050

## Installing

From inside the project directory, you can run:

    pip install .

## Usage

Provide an address and port to the `sensorclient` script:

    sensorclient 192.168.4.1:80000

This will display a 3D cube on your screen that responds to movements
of the device running [py-mpu6050][].

## License

py-mpu6050-client -- visualization for py-mpu6050  
Copyright (C) 2017 Lars Kellogg-Stedman <lars@oddbit.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


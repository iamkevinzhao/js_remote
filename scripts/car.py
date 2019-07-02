#!/usr/bin/env python
import socket
import rospy
from math import atan2, pi
from geometry_msgs.msg import Twist
from prius_msgs.msg import Control

vel_pub = []

def xy2deg(x, y):
    return atan2(y, x) * (180 / pi) % 180 + ((y < 0) and 180 or 0)

def handle_incoming_car(msg):

    control = Control()
    control.shift_gears = 2

    print('Receiving command', msg)

    args = msg.split(',')
    speed_level = int(args[7])
    x = float(args[5])
    y = float(args[6])
    deg = xy2deg(x,y)

    delta = 15
    if (45 + delta) <= deg <= (135 - delta): # forward
        control.throttle = 0.2 * speed_level
    elif (225 + delta) <= deg <= (315 - delta): #backward
        control.brake = 1.0
    elif (135 - delta) <= deg <= (225 + delta): #left
        control.throttle = 0.2 * speed_level
        control.steer = 0.2 * speed_level
        if deg >= 180:
            control.shift_gears = 3
    else: #right
        control.throttle = 0.2 * speed_level
        control.steer = -0.2 * speed_level
        if 270 <= deg <= 360:
            control.shift_gears = 3

    vel_pub.publish(control)

if __name__ == '__main__':
    rospy.init_node('js_remote', anonymous=True)
    vel_pub = rospy.Publisher('/prius', Control, queue_size=10)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 5000))
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by ', addr)
    while not rospy.is_shutdown():
        data = conn.recv(1024)
        if not data:
            continue
        handle_incoming_car(data)
    s.close()

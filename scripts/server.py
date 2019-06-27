#!/usr/bin/env python
import socket
import rospy
from math import atan2, pi
from geometry_msgs.msg import Twist

vel_pub = []

def xy2deg(x, y):
    return atan2(y, x) * (180 / pi) % 180 + ((y < 0) and 180 or 0)

def handle_incoming(msg):
    vel_msg = Twist()
    vel_msg.linear.x = 0.2
    vel_msg.angular.z = 0.2

    print('Receiving command', msg)

    args = msg.split(',')
    vel_msg.linear.x = int(args[5]) * vel_msg.linear.x
    vel_msg.angular.z = int(args[5]) * vel_msg.angular.z
    if args[4] == '1':
        vel_msg.angular.z = 0
    elif args[4] == '2':
        vel_msg.angular.z = 0
        vel_msg.linear.x  = -vel_msg.linear.x
    elif args[4] == '3':
        vel_msg.linear.x = 0
    elif args[4] == '4':
        vel_msg.linear.x = 0
        vel_msg.angular.z = -vel_msg.angular.z

    vel_pub.publish(vel_msg)

def handle_incoming_xy(msg):
    vel_msg = Twist()
    vel_msg.linear.x = 0.2
    vel_msg.angular.z = 0.2

    print('Receiving command', msg)

    args = msg.split(',')
    speed_level = int(args[7])
    x = float(args[5])
    y = float(args[6])
    deg = xy2deg(x,y)

    print(deg)

    vel_msg.linear.x = speed_level * vel_msg.linear.x
    vel_msg.angular.z = speed_level * vel_msg.angular.z

    if 45 <= deg <= 135: # forward
        vel_msg.angular.z = 0
    elif 225 <= deg <= 315: #backward
        vel_msg.angular.z = 0
        vel_msg.linear.x  = -vel_msg.linear.x
    elif 135 <= deg <= 225: #left
        vel_msg.linear.x = 0
    else: #right
        vel_msg.linear.x = 0
        vel_msg.angular.z = -vel_msg.angular.z

    vel_pub.publish(vel_msg)



if __name__ == '__main__':
    rospy.init_node('js_remote', anonymous=True)
    vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

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
        handle_incoming_xy(data)
    s.close()

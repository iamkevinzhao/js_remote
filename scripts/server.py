#!/usr/bin/env python
import socket
import rospy
from geometry_msgs.msg import Twist

vel_pub = []

def handle_incoming(msg):
    vel_msg = Twist()
    vel_msg.linear.x = 0.2

    print('Receiving command', msg)

    args = msg.split(',')
    vel_msg.linear.x = int(args[5]) * vel_msg.linear.x
    if args[4] == '1': # forward
        pass
    else:
        vel_msg.linear.x  = -vel_msg.linear.x
    vel_pub.publish(vel_msg)

if __name__ == '__main__':
    try:
        rospy.init_node('js_remote', anonymous=True)
        vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', 5000))
        s.listen(1)
        conn, addr = s.accept()
        print('Connected by ', addr)
        while not rospy.is_shutdown():
            data = conn.recv(1024)
            if not data:
                continue
            handle_incoming(data)
    except IOError:
        s.close()
    s.close()

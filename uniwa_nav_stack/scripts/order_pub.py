#!/usr/bin/env python

import rospy
from std_msgs.msg import String
# from uniwa_nav_stack.msg import string_array
import json


def talker():
    pub = rospy.Publisher('order_publisher', String, queue_size=10)
    rospy.init_node('order_publisher_node', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    # table = "table1" #

    item1 = 'beer' #
    item2 = 'cocacola'     #
    item3 = 'sprite'         #

    order = [item1, item2, item3]

    encoded_order = json.dumps(order)


    while not rospy.is_shutdown():

        rospy.loginfo(order)
        pub.publish(encoded_order)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import json
# from uniwa_nav_stack.msg import string_array

def talker():
    pub = rospy.Publisher('counter_items', String, queue_size=10)
    rospy.init_node('counter_items_node', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    item1 = 'pringles' #
    item2 = 'cocacola'     #
    item3 = 'sprite'         #

    counter_items = [item1, item2, item3]


    while not rospy.is_shutdown():

        rospy.loginfo(counter_items)
        pub.publish(json.dumps(counter_items))
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
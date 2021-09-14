#!/usr/bin/env python
#from __future__ import division, print_function

import rospy
import time
import os
from geometry_msgs.msg import Twist


class Fix(object):
    def __init__(self):
        self.flag = 0
        self.rate = rospy.Rate(1)
        self.done = rospy.is_shutdown()
        self.start_time = time.time()
        self.an_speed = -0.5
        self.pub = rospy.Publisher(
            '/mobile_base_controller/cmd_vel', Twist, queue_size=1)

    def rotation(self):
        self.rot = Twist()
        self.rot.angular.z = self.an_speed
        self.pub.publish(self.rot)

    def run(self):
        while not self.done:
            if time.time() - self.start_time < 100:  # two minutes
                print('fix arena started')
                if self.flag == 0:
                    os.system('rosservice call /global_localization')
                    self.flag = 1
                    rospy.sleep(3)
                else:
                    print('rotate')
                    self.rotation()
            else:
                print('teleiwsa')
                os.system('rosservice call /move_base/clear_costmaps')
                self.done = True


if __name__ == '__main__':
    try:
        rospy.init_node('peristrepsou')
        f = Fix()
        f.run()
    except rospy.ROSInterruptException:
        rospy.loginfo("Test is complete")

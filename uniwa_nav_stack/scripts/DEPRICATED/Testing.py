#!/usr/bin/env python
#from __future__ import division, print_function


import rospy
import numpy as np
import random
import math
import tf
import actionlib
from math import pi
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from actionlib import GoalStatus
from nav_msgs.msg import Path
from nav_msgs.srv import GetPlan
from tf import TransformListener
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from collections import OrderedDict
from std_msgs.msg import Float32
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped, PointStamped
from geometry_msgs.msg import Pose, Point, Quaternion


def start_moving():
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose = episode_locations[table]
    client.send_goal(goal)
    client.wait_for_result()




if __name__=='__main__':
    try:
        rospy.init_node('test_sequence')
        client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        client.wait_for_server(rospy.Duration())

        quaternions = list()
    	euler_angles = (pi/2, pi, 3*pi/2, 0)
    	for angle in euler_angles:
		    quat_angle = quaternion_from_euler(0, 0, angle, axes='sxyz')
		    quat = Quaternion(*quat_angle)
		    quaternions.append(quat)

        waypoints = list()
        waypoints.append(Pose(Point(5.2049407, -2.0635826, 0.0), quaternions[3]))
        waypoints.append(Pose(Point(2.46794486, -0.089344985, 0.0), quaternions[3]))
        waypoints.append(Pose(Point(4.565750598, 0.23821452, 0.0), quaternions[3]))

        episode_locations = (('table1', waypoints[0]),
	                         ('table2', waypoints[1]),
	                         ('table3', waypoints[2]))

        episode_locations = OrderedDict(episode_locations)


        rate = rospy.Rate(5)
        done = rospy.is_shutdown()
        while not done:
            print('doulevei')

            for table in episode_locations.iterkeys():
                start_moving()
                rospy.sleep(2)


            rate.sleep()
    except rospy.ROSInterruptException:
        pass

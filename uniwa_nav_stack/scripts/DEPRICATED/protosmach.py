#!/usr/bin/env python
#from __future__ import division, print_function


import rospy
import numpy as np
import random
import math
import tf
import actionlib
from math import pi
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionFeedback
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
from smach_ros import SimpleActionState, IntrospectionServer
from smach import State, StateMachine





class main():
  def __init__(self):

    rospy.init_node('test_sequence')
    rospy.on_shutdown(self.shutdown)

    self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    self.client.wait_for_server(rospy.Duration())

    quaternions = list()
    euler_angles = (pi/2, pi, 3*pi/2, 0)

    for angle in euler_angles:
      quat_angle = quaternion_from_euler(0, 0, angle, axes='sxyz')
      quat = Quaternion(*quat_angle)
      quaternions.append(quat)

    self.waypoints = list()
    self.waypoints.append(Pose(Point(2.808604002, 0.217082738876, 0.0), quaternions[0]))
    self.waypoints.append(Pose(Point(2.808604002, 0.217082738876, 0.0), quaternions[3]))
    self.waypoints.append(Pose(Point(2.808604002, 0.217082738876, 0.0), quaternions[1]))

    episode_locations = (('table1', self.waypoints[0]),
                        ('table2', self.waypoints[1]),
                        ('table3', self.waypoints[2]))

    self.episode_locations = OrderedDict(episode_locations)
    nav_states = {}

    for location in self.episode_locations.iterkeys():
      goal = MoveBaseGoal()
      goal.target_pose.header.frame_id = "map"
      goal.target_pose.header.stamp = rospy.Time.now()
      goal.target_pose.pose = self.episode_locations[location]
      move_base_state = SimpleActionState('move_base', MoveBaseAction, goal=goal, result_cb=self.move_base_result_cb, 
                                              exec_timeout=rospy.Duration(5.0),
                                              server_wait_timeout=rospy.Duration(10.0))
      nav_states[location] = move_base_state

      #self.client.send_goal(goal)
      #self.client.wait_for_result()

    
    sm_restaurant = StateMachine(outcomes=['succeeded','aborted','preempted'])

    with sm_restaurant:
      StateMachine.add('TABLE1', nav_states['table1'], transitions={'succeeded':'TABLE3', 'aborted':'', 'preempted':''})
      StateMachine.add('TABLE3', nav_states['table3'], transitions={'succeeded':'TABLE2', 'aborted':'', 'preempted':''})
      StateMachine.add('TABLE2', nav_states['table2'], transitions={'succeeded':'', 'aborted':'', 'preempted':''})


      intro_server = IntrospectionServer('restaurant', sm_restaurant, '/SM_ROOT')
      intro_server.start()

      # Execute the state machine
      sm_outcome = sm_restaurant.execute()
      intro_server.stop()

  def shutdown(self):
    rospy.loginfo("Stopping the robot...")
    rospy.sleep(1)

  def move_base_result_cb(self, userdata, status, result):
        if status == actionlib.GoalStatus.SUCCEEDED:
            pass


if __name__ == '__main__':
  try:
    main()
  except rospy.ROSInterruptException:
    rospy.loginfo("Test is complete")
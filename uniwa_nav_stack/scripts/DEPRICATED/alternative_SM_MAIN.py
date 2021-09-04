#!/usr/bin/env python
#from __future__ import division, print_function


import os
import rospy
import rosservice
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
import smach
from smach_ros import SimpleActionState, IntrospectionServer
from smach import State, StateMachine
from fix_arena import Fix

# points of interest (here only tables)
home = PoseStamped()
paso = PoseStamped()
table1 = PoseStamped()
table2 = PoseStamped()
table3 = PoseStamped()
table4 = PoseStamped()
table5 = PoseStamped()
table6 = PoseStamped()


client = actionlib.SimpleActionClient("move_base", MoveBaseAction)


# initialize coordinates
def init_locations():
    seq = 0

    home.header.frame_id = "map"
    home.header.seq = seq
    seq += 1
    home.pose.position.x = -0.368254032203
    home.pose.position.y = 0.823348215471
    home.pose.orientation.z = 0.000313931962172
    home.pose.orientation.w = 0.999999950723

    paso.header.frame_id = "map"
    paso.header.seq = seq
    seq += 1
    paso.pose.position.x = 0.480344302564
    paso.pose.position.y = -1.37227130362
    paso.pose.orientation.z = -0.996678161032
    paso.pose.orientation.w = 0.0814410420045

    table1.header.frame_id = "map"
    table1.header.seq = seq
    seq += 1
    table1.pose.position.x = 1.85846679197
    table1.pose.position.y = 0.59230689011
    table1.pose.orientation.z = 0.633293562507
    table1.pose.orientation.w = 0.773911664007

    table2.header.frame_id = "map"
    table2.header.seq = seq
    seq += 1
    table2.pose.position.x = 3.23852712217
    table2.pose.position.y = -0.0306546721319
    table2.pose.orientation.z = -0.680568825436
    table2.pose.orientation.w = 0.732684156949

    table3.header.frame_id = "map"
    table3.header.seq = seq
    seq += 1
    table3.pose.position.x = 4.10745675797
    table3.pose.position.y = 0.737478741019
    table3.pose.orientation.z = 0.712010659776
    table3.pose.orientation.w = 0.702168655215

    table4.header.frame_id = "map"
    table4.header.seq = seq
    seq += 1
    table4.pose.position.x = 5.12085210723
    table4.pose.position.y = -0.192821758167
    table4.pose.orientation.z = -0.673683316965
    table4.pose.orientation.w = 0.739020154287

    table5.header.frame_id = "map"
    table5.header.seq = seq
    seq += 1
    table5.pose.position.x = 6.58289493786
    table5.pose.position.y = 0.928934884087
    table5.pose.orientation.z = 0.753920508851
    table5.pose.orientation.w = 0.656965650802

    table6.header.frame_id = "map"
    table6.header.seq = seq
    seq += 1
    table6.pose.position.x = 7.44167327125
    table6.pose.position.y = 0.186966791119
    table6.pose.orientation.z = -0.70756013927
    table6.pose.orientation.w = 0.706653132248




# move base navigational function
def move(location, name):
    goal = MoveBaseGoal()
    goal.target_pose = location
    goal.target_pose.header.stamp = rospy.Time.now()
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration.from_sec(1000.0))


# MOVE state to specific location
class Move(smach.State):
    def __init__(self, location, name="default"):
        smach.State.__init__(self, outcomes=['done'])
        self.location = location
        self.name = name

    def execute(self, userdata):
        move(self.location,self.name)
        #rospy.sleep(3)
        return 'done'


class Wait(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done','skip'])
        self.msg = msg

    def execute(self, userdata):
        print self.msg + ":"
        result = raw_input()
        if result.lower() == 's' or result.lower() == 'skip':
            return 'skip'
        else:
            return 'done'

class SpawnOrder(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg

    def execute(self, userdata):
        item1 = 'beer'
        item2 = 'beer'
        item3 = 'beer'
        os.system('rosservice call /sciroc_object_manager/get_three_ordered_items %s %s %s' % (item1, item2, item3))
        return 'done'

class Pickuporder(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg

    def execute(self, userdata):
        os.system("rosservice call /sciroc_object_manager/move_items_on_the_tray")
        return 'done'


class Serve(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg

    def execute(self, userdata):
        os.system("rosservice call /sciroc_object_manager/move_items_on_the_closest_table")
        return 'done'

class Fix_arena(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg

    def execute(self, userdata):
        f = Fix()
        f.run()

        #rospy.sleep(3)
        return 'done'



# main with state machines
def main():
    rospy.init_node('smach_example_state_machine')
    client.wait_for_server()
    print ("init")
    init_locations()
    #f = Fix()

    # sm = smach.StateMachine(outcomes=['finished'])

    # with sm:
    #     smach.StateMachine.add('TABLE1',
    #                            Move(table1),
    #                            transitions={'done':'WAIT'})
    #     smach.StateMachine.add('WAIT',
    #                            Wait('Please wait..Facial recognition ON..press ENTER when done'),
    #                            transitions={'done':'HOME','skip':'TABLE1'})
    #     # smach.StateMachine.add('TABLE2',
    #     #                        Move(table2),
    #     #                        transitions={'done':'WAIT2'})
    #     # smach.StateMachine.add('WAIT2',
    #     #                        Wait('Please wait..Facial recognition ON..press ENTER when done'),
    #     #                        transitions={'done':'HOME','skip':'TABLE1'})
    #     # smach.StateMachine.add('TABLE3',
    #     #                       Move(table3),
    #     #                       transitions={'done':'WAIT3'})
    #     # smach.StateMachine.add('WAIT3',
    #     #                        Wait('Please wait..Facial recognition ON..press ENTER when done'),
    #     #                        transitions={'done':'HOME','skip':'TABLE1'})


    #     # smach.StateMachine.add('TABLE4',
    #     #                       Move(table4),
    #     #                       transitions={'done':'WAIT'})
    #     # smach.StateMachine.add('WAIT',
    #     #                        Wait('Please wait..Facial recognition ON..press ENTER when done'),
    #     #                        transitions={'done':'TABLE5','skip':'TABLE1'})
    #     # smach.StateMachine.add('TABLE5',
    #     #                       Move(table5),
    #     #                       transitions={'done':'WAIT'})
    #     # smach.StateMachine.add('WAIT',
    #     #                        Wait('Please wait..Facial recognition ON..press ENTER when done'),
    #     #                        transitions={'done':'TABLE6','skip':'TABLE1'})
    #     # smach.StateMachine.add('TABLE6',
    #     #                       Move(table6),
    #     #                       transitions={'done':'WAIT'})
    #     # smach.StateMachine.add('WAIT',
    #     #                        Wait('Please wait..Facial recognition ON..press ENTER when done'),
    #     #                        transitions={'done':'HOME','skip':'TABLE1'})


    #     smach.StateMachine.add('HOME',
    #                           Move(home),
    #                           transitions={'done':'finished'})


    # outcome = sm.execute()

    sm2 = smach.StateMachine(outcomes=['finished'])

    with sm2:
        smach.StateMachine.add('FIX',
                               Fix_arena('fix the arena you piece of shit'),
                               transitions={'done':'PASO'})
        smach.StateMachine.add('PASO',
                               Move(paso),
                               transitions={'done':'SPAWN'})
        smach.StateMachine.add('SPAWN',
                               SpawnOrder('Spawning items'),
                               transitions={'done':'PICKUP'})
        smach.StateMachine.add('PICKUP',
                               Pickuporder('Press ENTER to pick up the order!'),
                               transitions={'done':'TABLE2'})
        smach.StateMachine.add('TABLE2',
                                Move(table2),
                                transitions={'done':'SERVE'})
        smach.StateMachine.add('SERVE',
                                Serve('Serving....'),
                                transitions={'done':'finished'})
        # smach.StateMachine.add('WAIT3',
        #                        Wait('Please wait..Facial recognition ON..press ENTER when done'),
        #                        transitions={'done':'HOME','skip':'TABLE3'})
        # smach.StateMachine.add('HOME',
        #                        Move(home),
        #                        transitions={'done':'finished'})

    outcome2 = sm2.execute()


    rospy.spin()


if __name__ == '__main__':
  try:
    main()
  except rospy.ROSInterruptException:
    rospy.loginfo("Test is complete")

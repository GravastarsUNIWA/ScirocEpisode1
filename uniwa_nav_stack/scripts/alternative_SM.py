#!/usr/bin/env python

import os
import rospy
import numpy as np
import math
import tf
import actionlib
from fix_arena import Fix
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

from PHASE_1 import Move, Rotate, GetTableStatus, Report
from PHASE_3 import Wait, SpawnOrder, ConfirmOrder, CorrectOrder, Pickuporder, Serve




# points of interest (here only tables)
home = PoseStamped()
paso = PoseStamped()
point1 = PoseStamped()
point2 = PoseStamped()
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

    point1.header.frame_id = "map"
    point1.header.seq = seq
    seq += 1
    point1.pose.position.x = 3.35886874737
    point1.pose.position.y = 0.324034682627
    point1.pose.orientation.z = 0.129108324977
    point1.pose.orientation.w = 0.991630495912

    point2.header.frame_id = "map"
    point2.header.seq = seq
    seq += 1
    point2.pose.position.x = 6.12895165097
    point2.pose.position.y = 0.36917317753
    point2.pose.orientation.z = 0.0141001504049
    point2.pose.orientation.w = 0.999900587938

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


# main with state machines
def main():
    rospy.init_node('smach_example_state_machine')
    client.wait_for_server()
    print ("init")
    init_locations()

#=================================================================
##PHASE1##
#=================================================================    

    phase1 = smach.StateMachine(outcomes=['finished'])

    with phase1:

        smach.StateMachine.add('TABLE1',
                               Move(table1), 
                               transitions={'done':'finished'})
        # smach.StateMachine.add('ROTATE',
        #                        Rotate('Rotating'),
        #                        transitions={'done':'POINT2'})
        # smach.StateMachine.add('GETTABLESTATUS_1',
        #                        GetTableStatus('Checking Table 1'),
        #                        transitions={'done':'TABLE2'})
        # smach.StateMachine.add('TABLE2',
        #                        Move(table4),
        #                        transitions={'done':'GETTABLESTATUS_2'})
        # smach.StateMachine.add('GETTABLESTATUS_2',
        #                        GetTableStatus('Checking Table 2'),
        #                        transitions={'done':'REPORT'})
        # smach.StateMachine.add('REPORT',
        #                        Report('The number of customers is: '),
        #                        transitions={'done':'finished'})


    outcome = phase1.execute()

#=================================================================
##PHASE2##
#=================================================================

    # phase2 = smach.StateMachine(outcomes=['finished'])

    # with phase2:
    #     smach.StateMachine.add('TABLE1',
    #                             Move(FindTablesTobeSevred()), ##TODO
    #                             transitions={'done':'PICKUP2'})
    #     smach.StateMachine.add('TAKEORDER',
    #                             Serve('Serving....'),
    #                             transitions={'done':'TABLE1'})
       

    # outcome2 = phase2.execute()

#=================================================================
##PHASE3##
#=================================================================

    # phase3 = smach.StateMachine(outcomes=['finished'])


    # with phase3:

        
    #     smach.StateMachine.add('PASO',
    #                             Move(paso),
    #                             transitions={'done':'CONFIRMORDER'})
    #     # smach.StateMachine.add('SPAWNORDER',
    #     #                         SpawnOrder('Spawning order...'),
    #     #                         transitions={'done':'CONFIRMORDER'})
    #     smach.StateMachine.add('CONFIRMORDER',
    #                             ConfirmOrder('Confirming'),
    #                             transitions={'correct':'PICKUP', 'false':'CORRECTORDER'})
    #     smach.StateMachine.add('CORRECTORDER',
    #                             CorrectOrder('Correcting the order'),
    #                             transitions={'done':'WRONGORDER'})
    #     smach.StateMachine.add('WRONGORDER',
    #                             Wait('Please give the correct order'),
    #                             transitions={'skip':'CONFIRMORDER', 'done':'CONFIRMORDER'})
    #     smach.StateMachine.add('PICKUP',
    #                            Pickuporder('Picking items'),
    #                            transitions={'done':'TABLE2'})
    #     smach.StateMachine.add('TABLE2',
    #                             Move(table2), 
    #                             transitions={'done':'SERVE'})
    #     smach.StateMachine.add('SERVE',
    #                            Serve('Serving'),
    #                            transitions={'done':'finished'})
        
    # outcome3 = phase3.execute()


    rospy.spin()


if __name__ == '__main__':
  try:
    main()
  except rospy.ROSInterruptException:
    rospy.loginfo("Test is complete")

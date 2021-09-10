#!/usr/bin/env python

import rospy
from fix_arena import Fix
from std_msgs.msg import String
import smach
import time
from smach_ros import SimpleActionState, IntrospectionServer
from smach import State, StateMachine
from PHASE_1 import ShutDown, Move, CountPeople, TrackItems, AnnouncePhaseOne, GetStatus, Report
from PHASE_2 import GetServingTables, GetSpeechOrder
from PHASE_3 import Wait, SpawnOrder, ConfirmOrder, CorrectOrder, Pickuporder, Serve, SpawnYolo, ServeItems
from head import move_head_up, move_head_left1, move_head_left346, move_head_left2, move_head_left3
from coordinates import Coordinates
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


# main with state machines
def main():
    c = Coordinates()
    c.init_location()
    #c.init_location_close()

    home = c.home
    paso = c.paso
    resting_area = c.resting_area
    table1_walk = c.table1_walk
    table2_walk = c.table2_walk
    table3_walk = c.table3_walk
    table4_walk = c.table4_walk
    table5_walk = c.table5_walk
    table6_walk = c.table6_walk
    rospy.init_node('smach_example_state_machine')
    pubPhrase = rospy.Publisher('waitbot/tts/phrase', String, queue_size=5)



    phase1 = smach.StateMachine(outcomes=['finished'])
    #=================================================================
    ##PHASE1##
    #=================================================================
    with phase1:

        smach.StateMachine.add('VIEW1',
                               move_head_left1('rotate head'),
                               transitions={'done':'WAIT0'})
        smach.StateMachine.add('WAIT0',
                               Wait('resting'),
                                transitions={'done':'TABLE1'})

        # -------------------------- 1 -----------------------------
        smach.StateMachine.add('TABLE1',
                               Move(table1_walk, 'table1'),
                               transitions={'done':'WAIT1'})
        smach.StateMachine.add('WAIT1',
                               Wait('resting'),
                                transitions={'done':'PEOPLE1'})
        smach.StateMachine.add('PEOPLE1',
                               CountPeople('Counting People'),
                               transitions={'done':'ITEMS1'})
        smach.StateMachine.add('ITEMS1',
                               TrackItems('Tracking Items'),
                               transitions={'done':'STATUS1'})
        smach.StateMachine.add('STATUS1',
                               GetStatus('table1', 'Getting table status'),
                               transitions={'done':'VIEW3'})

    # -------------------------- 3 -----------------------------
        smach.StateMachine.add('VIEW3',
                               move_head_left3('rotate head'),
                               transitions={'done':'TABLE3'})
        smach.StateMachine.add('TABLE3',
                               Move(table3_walk, 'table3'),
                               transitions={'done':'WAIT3'})
        smach.StateMachine.add('WAIT3',
                               Wait('resting'),
                               transitions={'done':'PEOPLE3'})
        smach.StateMachine.add('PEOPLE3',
                               CountPeople('Counting People'),
                               transitions={'done':'ITEMS3'})
        smach.StateMachine.add('ITEMS3',
                               TrackItems('Tracking Items'),
                               transitions={'done':'STATUS3'})
        smach.StateMachine.add('STATUS3',
                               GetStatus('table3', 'Getting table status'),
                               transitions={'done':'VIEW5'}) #VIEW5

    # -------------------------- 5 -----------------------------
        smach.StateMachine.add('VIEW5',
                               move_head_left1('rotate head'),
                               transitions={'done':'TABLE5'})
        smach.StateMachine.add('TABLE5',
                               Move(table5_walk, 'table5'),
                               transitions={'done':'WAIT5'})
        smach.StateMachine.add('WAIT5',
                               Wait('resting'),
                               transitions={'done':'PEOPLE5'})
        smach.StateMachine.add('PEOPLE5',
                               CountPeople('Counting People'),
                               transitions={'done':'ITEMS5'})
        smach.StateMachine.add('ITEMS5',
                               TrackItems('Tracking Items'),
                               transitions={'done':'STATUS5'})
        smach.StateMachine.add('STATUS5',
                               GetStatus('table5', 'Getting table status'),
                               transitions={'done':'VIEW6'})

    # -------------------------- 6 -----------------------------
        smach.StateMachine.add('VIEW6',
                               move_head_left346('rotate head'),
                               transitions={'done':'TABLE6'})
        smach.StateMachine.add('TABLE6',
                               Move(table6_walk, 'table6'),
                               transitions={'done':'WAIT6'})
        smach.StateMachine.add('WAIT6',
                               Wait('resting'),
                               transitions={'done':'PEOPLE6'})
        smach.StateMachine.add('PEOPLE6',
                               CountPeople('Counting People'),
                               transitions={'done':'ITEMS6'})
        smach.StateMachine.add('ITEMS6',
                               TrackItems('Tracking Items'),
                               transitions={'done':'STATUS6'})
        smach.StateMachine.add('STATUS6',
                               GetStatus('table6', 'Getting table status'),
                               transitions={'done':'VIEW4'})

    # -------------------------- 4 -----------------------------
        smach.StateMachine.add('VIEW4',
                               move_head_left346('rotate head'),
                               transitions={'done':'TABLE4'})
        smach.StateMachine.add('TABLE4',
                               Move(table4_walk, 'table4'),
                               transitions={'done':'WAIT4'})
        smach.StateMachine.add('WAIT4',
                               Wait('resting'),
                               transitions={'done':'PEOPLE4'})
        smach.StateMachine.add('PEOPLE4',
                               CountPeople('Counting People'),
                               transitions={'done':'ITEMS4'})
        smach.StateMachine.add('ITEMS4',
                               TrackItems('Tracking Items'),
                               transitions={'done':'STATUS4'})
        smach.StateMachine.add('STATUS4',
                               GetStatus('table4', 'Getting table status'),
                               transitions={'done':'VIEW2'})

    # -------------------------- 2 -----------------------------
        smach.StateMachine.add('VIEW2',
                               move_head_left2('rotate head'),
                               transitions={'done':'TABLE2'})
        smach.StateMachine.add('TABLE2',
                               Move(table2_walk, 'table2'),
                               transitions={'done':'WAIT2'})
        smach.StateMachine.add('WAIT2',
                               Wait('resting'),
                               transitions={'done':'PEOPLE2'})
        smach.StateMachine.add('PEOPLE2',
                               CountPeople('Counting People'),
                               transitions={'done':'ITEMS2'})
        smach.StateMachine.add('ITEMS2',
                               TrackItems('Tracking Items'),
                               transitions={'done':'STATUS2'})
        smach.StateMachine.add('STATUS2',
                               GetStatus('table2', 'Getting table status'),
                               transitions={'done':'HOME'})
        smach.StateMachine.add('HOME',
                               Move(home, 'home'),
                               transitions={'done':'VIEWHOME'})
        smach.StateMachine.add('VIEWHOME',
                               move_head_up('original position'),
                               transitions={'done':'REPORT'})
        smach.StateMachine.add('REPORT',
                               Report('REPORT'),
                               transitions={'done':'GETSERVING'})

#=================================================================
##PHASE2##
#=================================================================                             
        smach.StateMachine.add('GETSERVING',
                                GetServingTables('GET TO SERVING TABLE'),
                                transitions={'done':'SPEECH'})
        smach.StateMachine.add('SPEECH',
                                GetSpeechOrder('INITIATE SPEECH'),
                                transitions={'done':'PASO'})

#=================================================================
##PHASE3##
#=================================================================

        smach.StateMachine.add('PASO',
                                Move(paso, 'counter'),
                                transitions={'done':'SPAWNORDER'})


        
        smach.StateMachine.add('SPAWNORDER',
                                SpawnOrder('Spawning order...'),
                                transitions={'done':'PICKUP'})
        # smach.StateMachine.add('YOLOKILL',
        #                         SpawnYolo('Respawning yolo'),
        #                         transitions={'done':'CONFIRMORDER'})
        # smach.StateMachine.add('CONFIRMORDER',
        #                         ConfirmOrder('Confirming'),
        #                         transitions={'correct':'PICKUP', 'false':'CORRECTORDER'})
        # smach.StateMachine.add('CORRECTORDER',
        #                         CorrectOrder('Correcting the order'),
        #                         transitions={'done':'PICKUP'})
        smach.StateMachine.add('PICKUP',
                               Pickuporder('Picking items'),
                               transitions={'done':'SERVE'})
        smach.StateMachine.add('SERVE',
                               Serve('Serving'),
                               transitions={'done':'SERVEITEMS'})
        smach.StateMachine.add('SERVEITEMS',
                                ServeItems('Serving table'),
                                transitions={'more':'GETSERVING' , 'fin':'HOMELAST'})
        smach.StateMachine.add('HOMELAST',
                               Move(home, 'home'),
                               transitions={'done':'finished'})

    outcome = phase1.execute()




   



if __name__ == '__main__':
  try:
    main()
  except rospy.ROSInterruptException:
    rospy.loginfo("Test is complete")

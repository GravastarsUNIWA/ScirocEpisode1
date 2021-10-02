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
    # c.init_location_close()

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

    experiment = smach.StateMachine(outcomes=['finished'])
    # =================================================================
    ##PHASE ONE##
    # =================================================================
    with experiment:

        # -------------------------- 3 -----------------------------
        smach.StateMachine.add('VIEW3',
                               move_head_left3('rotate head'),
                               transitions={'done': 'TABLE3'})
        smach.StateMachine.add('TABLE3',
                               Move(table3_walk, 'table3'),
                               transitions={'done': 'PEOPLE3'})
        smach.StateMachine.add('PEOPLE3',
                               CountPeople('Counting People'),
                               transitions={'done': 'ITEMS3'})
        smach.StateMachine.add('ITEMS3',
                               TrackItems('Tracking Items'),
                               transitions={'done': 'STATUS3'})
        smach.StateMachine.add('STATUS3',
                               GetStatus('table3', 'Getting table status'),
                               transitions={'done': 'VIEWHOME'})
        smach.StateMachine.add('VIEWHOME',
                               move_head_up('original position'),
                               transitions={'done': 'REPORT'})
        smach.StateMachine.add('REPORT',
                               Report('REPORT'),
                               transitions={'done': 'GETSERVING'})

# =================================================================
#PHASE2#
# =================================================================
        smach.StateMachine.add('GETSERVING',
                               GetServingTables('GO TO SERVING TABLE'),
                               transitions={'done': 'SPEECH'})
        smach.StateMachine.add('SPEECH',
                               GetSpeechOrder('INITIATE SPEECH'),
                               transitions={'done': 'PASO'})

# =================================================================
#PHASE3#
# =================================================================

        smach.StateMachine.add('PASO',
                               Move(paso, 'counter'),
                               transitions={'done': 'SPAWNORDER'})
        smach.StateMachine.add('SPAWNORDER',
                               SpawnOrder('Spawning order...'),
                               transitions={'done': 'PICKUP'})
        # smach.StateMachine.add('YOLORESPAWN',
        #                        SpawnYolo('Respawning yolov5'),
        #                        transitions={'done': 'CONFIRMORDER'})
        # smach.StateMachine.add('CONFIRMORDER',
        #                        ConfirmOrder('Confirming'),
        #                        transitions={'correct': 'PICKUP', 'false': 'PICKUP'})
        # smach.StateMachine.add('CORRECTORDER',
        #                         CorrectOrder('Correcting the order'),
        #                         transitions={'done':'PICKUP'})
        smach.StateMachine.add('PICKUP',
                               Pickuporder('Picking items'),
                               transitions={'done': 'SERVE'})
        smach.StateMachine.add('SERVE',
                               Serve('Serving'),
                               transitions={'done': 'SERVEITEMS'})
        smach.StateMachine.add('SERVEITEMS',
                               ServeItems('Serving table'),
                               transitions={'more': 'GETSERVING', 'fin': 'HOMELAST'})
        smach.StateMachine.add('HOMELAST',
                               Move(home, 'home'),
                               transitions={'done': 'finished'})

    outcome = experiment.execute()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        rospy.loginfo("Test is complete")

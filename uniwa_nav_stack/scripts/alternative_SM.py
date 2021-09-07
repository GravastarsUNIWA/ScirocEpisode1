#!/usr/bin/env python
# import json
# import rospy
# from fix_arena import Fix
# from std_msgs.msg import String, Bool
# import smach
# # from smach_ros import SimpleActionState, IntrospectionServer
# from smach import State, StateMachine
# # from PHASE_1 import Move, Rotate, GetTableStatus, Report
# from PHASE_1 import Move, CountPeople, TrackItems, AnnouncePhaseOne, GetStatus
# from PHASE_2 import GetServingTables, GetSpeechOrder
# from PHASE_3 import Wait, SpawnOrder, ConfirmOrder, CorrectOrder, Pickuporder, Serve
# # from head import Move_head
# from coordinates import Coordinates


import rospy
from fix_arena import Fix
from std_msgs.msg import String
import smach
import time
from smach_ros import SimpleActionState, IntrospectionServer
from smach import State, StateMachine
from PHASE_1 import ShutDown, Move, CountPeople, TrackItems, AnnouncePhaseOne, GetStatus
from PHASE_2 import GetServingTables, GetSpeechOrder
from PHASE_3 import Wait, SpawnOrder, ConfirmOrder, CorrectOrder, Pickuporder, Serve
from head import move_head_centre, move_head_up, move_head_down, move_head_left, move_head_right
from coordinates import Coordinates
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


pubPhrase = rospy.Publisher('waitbot/tts/phrase', String, queue_size=5)



# def all_status_callback(msg):
#     all_table_status_pub.publish(msg.data)

# def table_ready_callback(msg):
#     table_ready_pub.publish(msg.data)

# all_table_status_sub = rospy.Subscriber('/table_status/all_table_status', String, all_status_callback)
# all_table_status_pub = rospy.Publisher('/table_status/all_table_status', String, queue_size=1)

# table_ready_sub = rospy.Subscriber('/table_status/ready', Bool, table_ready_callback)
# table_ready_pub = rospy.Publisher('/table_status/ready', Bool, queue_size=1)




# main with state machines
def main():


    
    c = Coordinates()
    c.init_location()
    home = c.home
    paso = c.paso
    # table1_phase1 = c.table1_phase1
    table1 = c.table1
    table2 = c.table2

    rospy.init_node('main')


    
    

#=================================================================
##PHASE1##
#=================================================================    

    phase1 = smach.StateMachine(outcomes=['finished'])

    with phase1:

        smach.StateMachine.add('UPVIEW0',
                               move_head_up('Moving head up'),
                               transitions={'done':'WAIT0'})
        smach.StateMachine.add('WAIT0',
                               Wait('resting'),
                                transitions={'done':'TABLE1'})

        # -------------------------- 1 -----------------------------

        smach.StateMachine.add('TABLE1',
                               Move(table1, 'table1'),
                               transitions={'done':'WAIT1'})
        smach.StateMachine.add('WAIT1',
                               Wait('resting'),
                                transitions={'done':'PEOPLE1'})
        smach.StateMachine.add('PEOPLE1',
                               CountPeople('Counting People'),
                               transitions={'done':'DOWNVIEW1'})
        smach.StateMachine.add('DOWNVIEW1',
                               move_head_down('Moving head down'),
                               transitions={'done':'WAIT11'})
        smach.StateMachine.add('WAIT11',
                               Wait('Please give'),
                                transitions={'done':'ITEMS1'})
        smach.StateMachine.add('ITEMS1',
                               TrackItems('Tracking Items'),
                               transitions={'done':'STATUS1'})
        smach.StateMachine.add('STATUS1',
                               GetStatus('table1', 'Getting table status'),
                               transitions={'done':'GETSERVINGTABLES'})



    # outcome = phase1.execute()

#=================================================================
##PHASE2##
#=================================================================

        rospy.sleep(1)
        pubPhrase.publish('Initiating Phase 2')

    # phase2 = smach.StateMachine(outcomes=['finished'])

    # with phase2:
        smach.StateMachine.add('GETSERVINGTABLES',
                                GetServingTables('Getting serving tables'),
                                transitions={'done':'SPEECH'})

        smach.StateMachine.add('SPEECH',
                                GetSpeechOrder('INITIATE SPEECH'),
                                transitions={'done':'PASO'})

       

    # outcome2 = phase2.execute()

#=================================================================
##PHASE3##
#=================================================================
        rospy.sleep(1)

        pubPhrase.publish('Initiating Phase 3')
       
        smach.StateMachine.add('PASO',
                                Move(paso),
                                transitions={'done':'SPAWNORDER'})
        smach.StateMachine.add('SPAWNORDER',
                                SpawnOrder('Spawning order...'),
                                transitions={'done':'WAIT'})
        smach.StateMachine.add('WAIT',
                                Wait('Please give the correct order'),
                                transitions={'skip':'CONFIRMORDER', 'done':'CONFIRMORDER'})
        smach.StateMachine.add('CONFIRMORDER',
                                ConfirmOrder('Confirming'),
                                transitions={'correct':'PICKUP', 'false':'CORRECTORDER'})
        smach.StateMachine.add('CORRECTORDER',
                                CorrectOrder('Correcting the order'),
                                transitions={'done':'WRONGORDER'})
        smach.StateMachine.add('WRONGORDER',
                                Wait('Please give the correct order'),
                                transitions={'skip':'CONFIRMORDER', 'done':'CONFIRMORDER'})
        smach.StateMachine.add('PICKUP',
                               Pickuporder('Picking items'),
                               transitions={'done':'TABLE2'})
        smach.StateMachine.add('TABLE2',
                                Move(table2), 
                                transitions={'done':'SERVE'})
        smach.StateMachine.add('SERVE',
                               Serve('Serving'),
                               transitions={'done':'finished'})
        
    outcome1 = phase1.execute()


    rospy.spin()


if __name__ == '__main__':
    

    try:
        main()
    except rospy.ROSInterruptException:
        rospy.loginfo("Test is complete")

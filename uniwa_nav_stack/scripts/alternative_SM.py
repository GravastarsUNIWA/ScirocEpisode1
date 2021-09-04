#!/usr/bin/env python

import rospy
from fix_arena import Fix
from std_msgs.msg import String
import smach
from smach_ros import SimpleActionState, IntrospectionServer
from smach import State, StateMachine
# from PHASE_1 import Move, Rotate, GetTableStatus, Report
from PHASE_1 import Move, CountPeople, TrackItems, AnnouncePhaseOne, GetStatus
from PHASE_3 import Wait, SpawnOrder, ConfirmOrder, CorrectOrder, Pickuporder, Serve
from coordinates import Coordinates

pubPhrase = rospy.Publisher('waitbot/tts/phrase', String, queue_size=5)

# main with state machines
def main():
    c = Coordinates()
    c.init_location()
    home = c.home
    paso = c.paso
    point1 = c.point1
    point2 = c.point2
    table1 = c.table1
    table2 = c.table2
    table3 = c.table3
    table4 = c.table4
    table5 = c.table5
    table6 = c.table6
    rospy.init_node('smach_example_state_machine')
    print ("init")
    
    

#=================================================================
##PHASE1##
#=================================================================    

    phase1 = smach.StateMachine(outcomes=['finished'])

    with phase1:

        smach.StateMachine.add('TABLE1',
                               Move(table1, 'table1'), 
                               transitions={'done':'PEOPLE'})
        smach.StateMachine.add('PEOPLE',
                               CountPeople('Counting people'),
                               transitions={'done':'ITEMS'})
        smach.StateMachine.add('ITEMS',
                               TrackItems('Tracking Items'),
                               transitions={'done':'STATUS'})
        smach.StateMachine.add('STATUS',
                               GetStatus('Getting Table Status'),
                               transitions={'done':'finished'})
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

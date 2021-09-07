#!/usr/bin/env python
 
# Author: Automatic Addison https://automaticaddison.com
# Description: An example of a basic finite state machine for a turnstile at 
#   a stadium or metro station.
 
# Import the necessary libraries
import rospy # Python client library
from smach import State, StateMachine # State machine library
import smach_ros # Extensions for SMACH library to integrate it with ROS
from time import sleep # Handle time
 
# Define state LOCKED
class Locked(State):
  def __init__(self):
    State.__init__(self, outcomes=['push','coin'], input_keys=['input'])
 
  # Inside this block, you can execute any code you want
  def execute(self, userdata):
    sleep(1)
     
    rospy.loginfo('Executing state LOCKED')
         
    # When a state finishes, an outcome is returned. An outcome is a 
    # user-defined string that describes how a state finishes.
    # The transition to the next state is based on this outcome
    if userdata.input == 1:
      return 'push'
    else:
      return 'coin'
 
# Define state UNLOCKED
class Unlocked(State):
  def __init__(self):
    State.__init__(self, outcomes=['push','coin'], input_keys=['input'])
 
  def execute(self, userdata):
    sleep(1)
 
    rospy.loginfo('Executing state UNLOCKED')
 
    if userdata.input == 1:
      return 'push'
    else:
      return 'coin'
 
# Main method
def main():
 
  # Initialize the node
  rospy.init_node('fsm_turnstile_py')
 
  # Create a SMACH state machine container
  sm = StateMachine(outcomes=['succeeded','failed'])
 
  # Set user data for the finite state machine
  sm.userdata.sm_input = 0
  #sm.userdata.sm_input = input("Enter 1 to Push or 0 to Insert a Coin: ")
     
  # Open the state machine container. A state machine container holds a number of states.
  with sm:
     
    # Add states to the container, and specify the transitions between states
    # For example, if the outcome of state LOCKED is 'coin', then we transition to state UNLOCKED.
    StateMachine.add('LOCKED', Locked(), transitions={'push':'LOCKED','coin':'UNLOCKED'}, remapping={'input':'sm_input'})
    StateMachine.add('UNLOCKED', Unlocked(), transitions={'push':'LOCKED','coin':'UNLOCKED'}, remapping={'input':'sm_input'})
 
  # View our state transitions using ROS by creating and starting the instrospection server
  sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
  sis.start()
   
  # Execute the state machine 
  outcome = sm.execute()
 
  # Wait for ctrl-c to stop the application
  rospy.spin()
  sis.stop()
 
if __name__ == '__main__':
  main()
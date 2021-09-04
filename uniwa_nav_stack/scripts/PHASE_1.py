#!/usr/bin/env python

import os
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionFeedback
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped, PointStamped
from geometry_msgs.msg import Pose, Point, Quaternion
import smach
from std_msgs.msg import String, Bool
import json

all_table_status = {}
cnt = 1

pubPhrase = rospy.Publisher('waitbot/tts/phrase', String, queue_size=5)


# initialize coordinates

# MOVE state to specific location
class Move(smach.State):
    def __init__(self, location, location_name, name="default"):
        smach.State.__init__(self, outcomes=['done'])
        self.location = location
        self.location_name = location_name
        self.name = name
        # self.location_name = [ k for k,v in locals().items() if v == self.location.][0]

    def move(self, location, name):
        client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        client.wait_for_server()
        goal = MoveBaseGoal()
        goal.target_pose = location
        print(self.location_name)
        goal.target_pose.header.stamp = rospy.Time.now()
        client.send_goal(goal)
        client.wait_for_result(rospy.Duration.from_sec(1000.0))

    def execute(self, userdata):
        pubPhrase.publish("Moving to {}".format(self.location_name))
        self.move(self.location, self.name)
        os.system('rosservice call /move_base/clear_costmaps')
        return 'done'

class MoveCloser(smach.State):
    def __init__(self, location, name="default"):
        smach.State.__init__(self, outcomes=['done'])
        self.location = location
        self.name = name
    def move(self, location, name):
        client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        client.wait_for_server()
        goal = MoveBaseGoal()
        goal.target_pose = location
        goal.target_pose.header.stamp = rospy.Time.now()
        client.send_goal(goal)
        client.wait_for_result(rospy.Duration.from_sec(1000.0))
    def execute(self, userdata):
        self.move(self.location, self.name)
        os.system('rosservice call /move_base/clear_costmaps')
        return 'done'

class Rotate(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.start_time = time.time()
    def execute(self, userdata):
        f = Fix()
        start_time = time.time()
        seconds = 10
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            f.rotation()
            if elapsed_time > seconds:
                break
        return 'done'

class CountPeople(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.table_status = {"Items":[], "NoP":[], "Status":[]}
        self.human_counter_sub = rospy.Subscriber("/object_detection/people_counter", String, self.people_counter_callback)
        self.table_status_pub = rospy.Publisher('/table_status/status_per_table', String, queue_size=1)

    def people_counter_callback(self, msg):
        self.human_counter = int(msg.data)

    def execute(self, userdata):
        pubPhrase.publish('Couting People')
        rospy.sleep(3)
        self.table_status.update({'NoP' : self.human_counter})
        self.encoded_table_status = json.dumps(self.table_status)
        self.table_status_pub.publish(self.encoded_table_status)
        
        # global all_table_status, cnt

        return 'done'

class TrackItems(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.isFood_sub = rospy.Subscriber("/object_detection/isFood", Bool, self.isFood_callback)
        self.table_status_sub = rospy.Subscriber("/table_status/status_per_table", String, self.table_status_callback)
        self.table_status_pub = rospy.Publisher('/table_status/status_per_table', String, queue_size=1)

    def table_status_callback(self, msg):
        self.encoded_table_status = msg.data
        self.table_status = json.loads(self.encoded_table_status)

    def isFood_callback(self, msg):
        self.item_flag = msg.data

    def execute(self, userdata):
        pubPhrase.publish('Tracking Items')
        # global all_table_status, cnt
        rospy.sleep(3)
        self.table_status.update({"Items" : self.item_flag})
        self.encoded_table_status = json.dumps(self.table_status)
        self.table_status_pub.publish(self.encoded_table_status)

        return 'done'

class GetStatus(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.table_status_sub = rospy.Subscriber("/table_status/status_per_table", String, self.table_status_callback)
        self.table_status_pub = rospy.Publisher('/table_status/status_per_table', String, queue_size=1)

    def table_status_callback(self, msg):
        self.encoded_table_status = msg.data
        self.table_status = json.loads(self.encoded_table_status)

    def execute(self, userdata):

        self.human_counter = self.table_status["NoP"]
        self.item_flag = self.table_status["Items"]

        if self.human_counter == 0 and self.item_flag == False:

            pubPhrase.publish('The table is ready.')
            self.table_status.update({'Status': 'Ready'})

            self.encoded_table_status = json.dumps(self.table_status)
            self.table_status_pub.publish(self.encoded_table_status)

            # all_table_status['table{}'.format(cnt)] = self.table_status

            return 'done'

        elif self.human_counter == 0 and self.item_flag == True:

            pubPhrase.publish('The table needs cleaning.')            
            self.table_status.update({'Status': 'Cleaning'})

            # all_table_status['table{}'.format(cnt)] = self.table_status

            return 'done'


        elif self.human_counter >= 1 and self.item_flag == True:
            
            pubPhrase.publish('The table is already served')  
            self.table_status.update({'Status': 'Served'})
            self.encoded_table_status = json.dumps(self.table_status)
            self.table_status_pub.publish(self.encoded_table_status)

            # all_table_status['table{}'.format(cnt)] = self.table_status



            return 'done'

        else:
            pubPhrase.publish('The table needs serving.')  
            self.table_status.update({'Status': 'Serving'})
            self.encoded_table_status = json.dumps(self.table_status)
            self.table_status_pub.publish(self.encoded_table_status)

            # all_table_status['table{}'.format(cnt)] = self.table_status

            return 'done'


# class GetTableStatus(smach.State):
#     def __init__(self, msg):
#         smach.State.__init__(self, outcomes=['done'])
#         self.msg = msg
#         self.table_status = {"Items":[], "NoP":[], "Status":[]}
#         self.human_counter_sub = rospy.Subscriber("/object_detection/people_counter", String, self.people_counter_callback)
#         self.isFood_sub = rospy.Subscriber("/object_detection/isFood", Bool, self.isFood_callback)
#         self.total_customers = rospy.Publisher('/total_customers_topic', String, queue_size=1)
#         self.total = 0

#     def people_counter_callback(self, msg):
#         self.human_counter = int(msg.data)
#     def isFood_callback(self, msg):
#         self.item_flag = msg.data

#     def execute(self, userdata):
#         rospy.loginfo('check the table')
#         global all_table_status, cnt

#         print(self.item_flag)

#         if self.human_counter == 0 and self.item_flag == False:
#             self.status = 'Ready'
#             self.table_status.update({"Items" : self.item_flag})
#             self.table_status.update({'NoP' : self.human_counter})
#             self.table_status.update({'Status': self.status})

#             all_table_status['table{}'.format(cnt)] = self.table_status

#             # all_table_status['table{}'.format(i)] = self.table_status #TODO

#             print('Ready to accept new customers') # speech announcement

#             print(all_table_status)

#             cnt+=1
#             return 'done'

#         elif self.human_counter == 0 and self.item_flag == True:
#             self.status = 'Cleaning'
#             self.table_status.update({"Items" : self.item_flag})
#             self.table_status.update({'NoP' : self.human_counter})
#             self.table_status.update({'Status': self.status})

#             all_table_status['table{}'.format(cnt)] = self.table_status

#             print('Needs cleaning') # speech announcement

#             cnt+=1
#             print(all_table_status)
#             return 'done'


#         elif self.human_counter >= 1 and self.item_flag == True:
#             self.status = 'Served'
#             self.table_status.update({"Items" : self.item_flag})
#             self.table_status.update({'NoP' : self.human_counter})
#             self.table_status.update({'Status': self.status})

#             all_table_status['table{}'.format(cnt)] = self.table_status

#             print('Number of humans at the table', self.human_counter)
#             print('Already served') # speech announcement

#             cnt+=1
#             print(all_table_status)

#             self.total+=self.human_counter
#             self.total_customers.publish(str(self.total))
#             return 'done'

#         else:
#             self.status = 'Serving'
#             self.table_status.update({"Items" : self.item_flag})
#             self.table_status.update({'NoP' : self.human_counter})
#             self.table_status.update({'Status': self.status})

#             all_table_status['table{}'.format(cnt)] = self.table_status

#             print('Number of humans at the table', self.human_counter)
#             print('Needs serving') # speech announcement


#             cnt+=1
#             print(all_table_status)
#             self.total+=self.human_counter
#             self.total_customers.publish(str(self.total))
#             return 'done'

class Report(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.total_customers = rospy.Publisher('/total_customers_topic', String, queue_size=1)

    def execute(self, userdata):
        global all_table_status
        self.sum = 0
        for table in all_table_status:
            self.sum += all_table_status[table]['NoP']

        print(self.sum)

        try:
            os.remove(os.path.expanduser('~')+"/table_report.txt")
        except OSError:
            pass

        f = open(os.path.expanduser('~')+"/table_report.txt", "a")
        f.write(str(all_table_status))
        f.write("\n \n Total number of customers: " + str(self.sum))
        f.close
        print("done")
        return 'done'

class AnnouncePhaseOne(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg

    def execute(self, userdata):
        pubPhrase.publish("Initiating Phase One")
        return 'done'

class AnnouncePhaseTwo(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg

    def execute(self, userdata):
        pubPhrase.publish("Initiating Phase Two")
        return 'done'

class AnnouncePhaseThree(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg

    def execute(self, userdata):
        pubPhrase.publish("Initiating Phase Three")
        return 'done'
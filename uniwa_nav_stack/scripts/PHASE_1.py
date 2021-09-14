#!/usr/bin/env python

import os
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose, Point
import smach
from std_msgs.msg import String, Bool
import json
import time
from trajectory_msgs.msg import JointTrajectory

pubPhrase = rospy.Publisher('waitbot/tts/phrase', String, queue_size=5)


class ShutDown(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg

    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        rospy.sleep(1)

    def execute(self, userdata):
        rospy.on_shutdown(self.shutdown)
        return 'done'


class Move(smach.State):
    def __init__(self, location, location_name='Ignore', name="default"):
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
        goal.target_pose.header.stamp = rospy.Time.now()
        client.send_goal(goal)
        client.wait_for_result(rospy.Duration.from_sec(1000.0))

    def execute(self, userdata):
        pubPhrase.publish("Moving to {}".format(self.location_name))
        self.move(self.location, self.name)
        os.system('rosservice call /move_base/clear_costmaps')
        return 'done'


class CountPeople(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.table_status = {"Items": [], "NoP": [], "Status": []}
        self.human_counter_sub = rospy.Subscriber(
            "/object_detection/people_counter", String, self.people_counter_callback)
        self.table_status_pub = rospy.Publisher(
            '/table_status/status_per_table', String, queue_size=1)

    def people_counter_callback(self, msg):
        self.human_counter = int(msg.data)

    def execute(self, userdata):
        pubPhrase.publish('Counting People')
        rospy.sleep(3)
        self.table_status.update({'NoP': self.human_counter})
        self.encoded_table_status = json.dumps(self.table_status)
        self.table_status_pub.publish(self.encoded_table_status)

        return 'done'


class TrackItems(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.isFood_sub = rospy.Subscriber(
            "/object_detection/isFood", Bool, self.isFood_callback)
        self.table_status_sub = rospy.Subscriber(
            "/table_status/status_per_table", String, self.table_status_callback)
        self.table_status_pub = rospy.Publisher(
            '/table_status/status_per_table', String, queue_size=1)

    def table_status_callback(self, msg):
        self.encoded_table_status = msg.data
        self.table_status = json.loads(self.encoded_table_status)

    def isFood_callback(self, msg):
        self.item_flag = msg.data

    def execute(self, userdata):
        pubPhrase.publish('Tracking Items')
        # global all_table_status, cnt
        rospy.sleep(3)
        self.table_status.update({"Items": self.item_flag})
        self.encoded_table_status = json.dumps(self.table_status)
        self.table_status_pub.publish(self.encoded_table_status)

        return 'done'


class GetStatus(smach.State):
    def __init__(self, location_name, tablestring):
        smach.State.__init__(self, outcomes=['done'])
        self.tablestring = tablestring
        self.table_status_sub = rospy.Subscriber(
            "/table_status/status_per_table", String, self.table_status_callback)
        self.table_status_pub = rospy.Publisher(
            '/table_status/status_per_table', String, queue_size=1)
        self.all_table_status_pub = rospy.Publisher(
            '/table_status/all_table_status', String, queue_size=1)
        self.all_table_status_sub = rospy.Subscriber(
            '/table_status/all_table_status', String, self.all_table_status_callback)

        self.location_name = location_name
        self.all_table_status = {'{}'.format(self.location_name): []}

    def all_table_status_callback(self, msg):
        self.all_table_status = json.loads(msg.data)

    def table_status_callback(self, msg):
        self.encoded_table_status = msg.data
        self.table_status = json.loads(self.encoded_table_status)

    def execute(self, userdata):
        self.human_counter = self.table_status["NoP"]
        self.item_flag = self.table_status["Items"]

        if self.human_counter == 0 and self.item_flag == False:
            pubPhrase.publish('The table is ready.')
            self.table_status.update({'Status': 'Ready'})
        elif self.human_counter == 0 and self.item_flag == True:
            pubPhrase.publish('The table needs cleaning.')
            self.table_status.update({'Status': 'Cleaning'})
        elif self.human_counter >= 1 and self.item_flag == True:
            pubPhrase.publish('The table is already served')
            self.table_status.update({'Status': 'Served'})
        else:
            pubPhrase.publish('The table needs serving.')
            self.table_status.update({'Status': 'Serving'})

        self.table_status_temp = self.table_status
        self.encoded_table_status = json.dumps(self.table_status)
        self.table_status_pub.publish(self.encoded_table_status)

        # self.all_table_status.update({'{}'.format(self.location_name): self.table_status_temp})
        self.all_table_status['{}'.format(
            self.location_name)] = self.table_status_temp

        self.encoded_all_table_status = json.dumps(self.all_table_status)
        self.all_table_status_pub.publish(self.encoded_all_table_status)

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


class Report(smach.State):

    def __init__(self, msg):

        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.total_customers = rospy.Publisher(
            '/total_customers_topic', String, queue_size=1)
        self.all_table_status_sub = rospy.Subscriber(
            '/table_status/all_table_status', String, self.all_table_status_callback)

    def all_table_status_callback(self, msg):

        self.all_table_status = json.loads(msg.data)

    def execute(self, userdata):

        self.sum = 0
        for table in self.all_table_status:
            self.sum += self.all_table_status[table]['NoP']
        try:

            os.remove(os.path.expanduser('~')+"/table_report.json")
        except OSError:
            pass

        report = dict()
        report['table_status'] = self.all_table_status
        report['total_number_of_customes'] = self.sum

        with open(os.path.expanduser('~')+"/table_report.json", "w") as f:
            f.write(json.dumps(report))

        return 'done'

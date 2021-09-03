#!/usr/bin/env python

import os
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionFeedback
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped, PointStamped
from geometry_msgs.msg import Pose, Point, Quaternion
import smach
from std_msgs.msg import String, Bool

all_table_status = {}
cnt = 1
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
    table1.pose.position.x = 2.70123527244
    table1.pose.position.y = 0.279692458048
    table1.pose.orientation.z = 0.846659897686
    table1.pose.orientation.w = 0.532134398109

    table2.header.frame_id = "map"
    table2.header.seq = seq
    seq += 1
    table2.pose.position.x = 4.07672339902
    table2.pose.position.y = 0.394613572188
    table2.pose.orientation.z = -0.900374967038
    table2.pose.orientation.w = 0.435114833959

    table3.header.frame_id = "map"
    table3.header.seq = seq
    seq += 1
    table3.pose.position.x = 4.05819400471
    table3.pose.position.y = 0.0744841087051
    table3.pose.orientation.z = 0.666187683749
    table3.pose.orientation.w = 0.745784130979

    table4.header.frame_id = "map"
    table4.header.seq = seq
    seq += 1
    table4.pose.position.x = 5.35074645611
    table4.pose.position.y = 0.64713141245
    table4.pose.orientation.z = -0.689793332612
    table4.pose.orientation.w = 0.724006324755

    # table1.header.frame_id = "map"
    # table1.header.seq = seq
    # seq += 1
    # table1.pose.position.x = 1.85846679197
    # table1.pose.position.y = 0.59230689011
    # table1.pose.orientation.z = 0.633293562507
    # table1.pose.orientation.w = 0.773911664007
    #
    # table2.header.frame_id = "map"
    # table2.header.seq = seq
    # seq += 1
    # table2.pose.position.x = 3.23852712217
    # table2.pose.position.y = -0.0306546721319
    # table2.pose.orientation.z = -0.680568825436
    # table2.pose.orientation.w = 0.732684156949
    #
    # table3.header.frame_id = "map"
    # table3.header.seq = seq
    # seq += 1
    # table3.pose.position.x = 4.10745675797
    # table3.pose.position.y = 0.737478741019
    # table3.pose.orientation.z = 0.712010659776
    # table3.pose.orientation.w = 0.702168655215
    #
    # table4.header.frame_id = "map"
    # table4.header.seq = seq
    # seq += 1
    # table4.pose.position.x = 5.12085210723
    # table4.pose.position.y = -0.192821758167
    # table4.pose.orientation.z = -0.673683316965
    # table4.pose.orientation.w = 0.739020154287

    table5.header.frame_id = "map"
    table5.header.seq = seq
    seq += 1
    table5.pose.position.x = 6.77527952194
    table5.pose.position.y = -0.0664653778076
    table5.pose.orientation.z = 0.720783467242
    table5.pose.orientation.w = 0.693160294124

    table6.header.frame_id = "map"
    table6.header.seq = seq
    seq += 1
    table6.pose.position.x = 7.59110307693
    table6.pose.position.y = 0.630295038223
    table6.pose.orientation.z = -0.720957630938
    table6.pose.orientation.w = 0.692979144269

# MOVE state to specific location
class Move(smach.State):
    def __init__(self, location, name="default"):
        smach.State.__init__(self, outcomes=['done'])
        self.location = location
        self.name = name
        self.limit = 0.02
        self.robot_sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.call_robot)


    def call_robot(self, msg):
        self.x_robot = msg.pose.pose.position.x
        self.y_robot = msg.pose.pose.position.y
        self.qz = msg.pose.pose.orientation.z
        self.qw = msg.pose.pose.orientation.w
        print(self.qz)


    def move(self, location, name):
        client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        client.wait_for_server()
        goal = MoveBaseGoal()
        goal.target_pose = location
        goal.target_pose.header.stamp = rospy.Time.now()
        client.send_goal(goal)
        client.wait_for_result(rospy.Duration.from_sec(1000.0))

    def execute(self, userdata):
        while abs(table1.pose.orientation.z - self.qz) > 0.2 and not rospy.is_shutdown():
            print('diorthwnw')
            self.move(self.location, self.name)
            os.system('rosservice call /move_base/clear_costmaps')
        #print(table1.pose.position.x)
        print('diorthwsa')

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

class GetTableStatus(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.table_status = {"Items":[], "NoP":[], "Status":[]}

        self.human_counter_sub = rospy.Subscriber("/object_detection/people_counter", String, self.people_counter_callback)

        self.isFood_sub = rospy.Subscriber("/object_detection/isFood", Bool, self.isFood_callback)

        self.total_customers = rospy.Publisher('/total_customers_topic', String, queue_size=1)
        self.total = 0

    def people_counter_callback(self, msg):
        self.human_counter = int(msg.data)
    def isFood_callback(self, msg):
        self.item_flag = msg.data

    def execute(self, userdata):

        rospy.loginfo('check the table')

        global all_table_status, cnt

        print(self.item_flag)

        if self.human_counter == 0 and self.item_flag == False:
            self.status = 'Ready'
            self.table_status.update({"Items" : self.item_flag})
            self.table_status.update({'NoP' : self.human_counter})
            self.table_status.update({'Status': self.status})

            all_table_status['table{}'.format(cnt)] = self.table_status

            # all_table_status['table{}'.format(i)] = self.table_status #TODO

            print('Ready to accept new customers') # speech announcement

            print(all_table_status)

            cnt+=1
            return 'done'

        elif self.human_counter == 0 and self.item_flag == True:
            self.status = 'Cleaning'
            self.table_status.update({"Items" : self.item_flag})
            self.table_status.update({'NoP' : self.human_counter})
            self.table_status.update({'Status': self.status})

            all_table_status['table{}'.format(cnt)] = self.table_status

            print('Needs cleaning') # speech announcement

            cnt+=1
            print(all_table_status)
            return 'done'


        elif self.human_counter >= 1 and self.item_flag == True:
            self.status = 'Served'
            self.table_status.update({"Items" : self.item_flag})
            self.table_status.update({'NoP' : self.human_counter})
            self.table_status.update({'Status': self.status})

            all_table_status['table{}'.format(cnt)] = self.table_status

            print('Number of humans at the table', self.human_counter)
            print('Already served') # speech announcement

            cnt+=1
            print(all_table_status)

            self.total+=self.human_counter
            self.total_customers.publish(str(self.total))
            return 'done'

        else:
            self.status = 'Serving'
            self.table_status.update({"Items" : self.item_flag})
            self.table_status.update({'NoP' : self.human_counter})
            self.table_status.update({'Status': self.status})

            all_table_status['table{}'.format(cnt)] = self.table_status

            print('Number of humans at the table', self.human_counter)
            print('Needs serving') # speech announcement


            cnt+=1
            print(all_table_status)
            self.total+=self.human_counter
            self.total_customers.publish(str(self.total))
            return 'done'

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

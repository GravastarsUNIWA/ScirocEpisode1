#!/usr/bin/env python
#import smach
import os
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import rospy
import smach
import time


class move_head_down(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.name1 = 'head_1_joint'
        self.name2 = 'head_2_joint'
        self.head_cmd = rospy.Publisher('/head_controller/command', JointTrajectory, queue_size=1)
    def movedown(self):
        jt = JointTrajectory()
        jt.joint_names = [self.name1, self.name2]
        jtp = JointTrajectoryPoint()
        jtp.positions = [0.0, -0.4]  # -0.2
        jtp.time_from_start = rospy.Duration(2.0)
        jt.points.append(jtp)
        self.head_cmd.publish(jt)
    def execute(self, userdata):
        start_time = time.time()
        seconds = 5
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            self.movedown()
            if elapsed_time > seconds:
                break
        return 'done'

class move_head_up(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.name1 = 'head_1_joint'
        self.name2 = 'head_2_joint'
        self.head_cmd = rospy.Publisher('/head_controller/command', JointTrajectory, queue_size=1)
    def moveup(self):
        jt = JointTrajectory()
        jt.joint_names = [self.name1, self.name2]
        jtp = JointTrajectoryPoint()
        jtp.positions = [0.0, 0.1]
        jtp.time_from_start = rospy.Duration(2.0)
        jt.points.append(jtp)
        self.head_cmd.publish(jt)
    def execute(self, userdata):
        start_time = time.time()
        seconds = 5
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            self.moveup()
            if elapsed_time > seconds:
                break
        return 'done'


class move_head_right(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.name1 = 'head_1_joint'
        self.name2 = 'head_2_joint'
        self.head_cmd = rospy.Publisher('/head_controller/command', JointTrajectory, queue_size=1)
    def moveright(self):
        jt = JointTrajectory()
        jt.joint_names = [self.name1, self.name2]
        jtp = JointTrajectoryPoint()
        jtp.positions = [-0.3, 0.1]  # -0.2
        jtp.time_from_start = rospy.Duration(2.0)
        jt.points.append(jtp)
        self.head_cmd.publish(jt)
    def execute(self, userdata):
        start_time = time.time()
        seconds = 5
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            self.moveright()
            if elapsed_time > seconds:
                break
        return 'done'

class move_head_left(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.name1 = 'head_1_joint'
        self.name2 = 'head_2_joint'
        self.head_cmd = rospy.Publisher('/head_controller/command', JointTrajectory, queue_size=1)
    def moveleft(self):
        jt = JointTrajectory()
        jt.joint_names = [self.name1, self.name2]
        jtp = JointTrajectoryPoint()
        jtp.positions = [0.3, 0.1]
        jtp.time_from_start = rospy.Duration(2.0)
        jt.points.append(jtp)
        self.head_cmd.publish(jt)
    def execute(self, userdata):
        start_time = time.time()
        seconds = 5
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            self.moveleft()
            if elapsed_time > seconds:
                break
        return 'done'

class move_head_centre(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.name1 = 'head_1_joint'
        self.name2 = 'head_2_joint'
        self.head_cmd = rospy.Publisher('/head_controller/command', JointTrajectory, queue_size=1)
    def movecentre(self):
        jt = JointTrajectory()
        jt.joint_names = [self.name1, self.name2]
        jtp = JointTrajectoryPoint()
        jtp.positions = [0.0, 0.05]
        jtp.time_from_start = rospy.Duration(2.0)
        jt.points.append(jtp)
        self.head_cmd.publish(jt)
    def execute(self, userdata):
        start_time = time.time()
        seconds = 5
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            self.movecentre()
            if elapsed_time > seconds:
                break
        return 'done'


# class MOVE_HEAD(object):
#     def __init__(self):
#         self.head_cmd = rospy.Publisher('/head_controller/command', JointTrajectory, queue_size=1)
#         self.name1 = 'head_1_joint'
#         self.name2 = 'head_2_joint'
#
#     def center_view(self):
#         self.jt = JointTrajectory()
#         self.jt.joint_names = ['head_1_joint', 'head_2_joint']
#         self.jtp = JointTrajectoryPoint()
#         self.jtp.positions = [0.0, 0.1]
#         self.jtp.time_from_start = rospy.Duration(2.0)
#         self.jt.points.append(self.jtp)
#         self.head_cmd.publish(self.jt)
#
#     def up_view(self):
#         self.jt = JointTrajectory()
#         self.jt.joint_names = ['head_1_joint', 'head_2_joint']
#         self.jtp = JointTrajectoryPoint()
#         self.jtp.positions = [0.0, 0.1]
#         self.jtp.time_from_start = rospy.Duration(2.0)
#         self.jt.points.append(self.jtp)
#         self.head_cmd.publish(self.jt)
#
#     def close_view(self):
#         self.jt = JointTrajectory()
#         self.jt.joint_names = ['head_1_joint', 'head_2_joint']
#         self.jtp = JointTrajectoryPoint()
#         self.jtp.positions = [0.0, -0.4]
#         self.jtp.time_from_start = rospy.Duration(2.0)
#         self.jt.points.append(self.jtp)
#         self.head_cmd.publish(self.jt)
# #
# #     def left_view(self):
# #         self.jt = JointTrajectory()
# #         self.jt.joint_names = [self.name1, self.name2]
# #         self.jtp = JointTrajectoryPoint()
# #         self.jtp.positions = [0.9, 0.1]
# #         self.jtp.time_from_start = rospy.Duration(2.0)
# #         self.jt.points.append(self.jtp)
# #         self.head_cmd.publish(self.jt)
# #
# #     def right_view(self):
# #         self.jt = JointTrajectory()
# #         self.jt.joint_names = ['head_1_joint', 'head_2_joint']
# #         self.jtp = JointTrajectoryPoint()
# #         self.jtp.positions = [-0.6, 0.1]
# #         self.jtp.time_from_start = rospy.Duration(2.0)
# #         self.jt.points.append(self.jtp)
# #         self.head_cmd.publish(self.jt)
# #
# #
# if __name__ == '__main__':
#     try:
#         rospy.init_node('peristrepsou')
#         head = MOVE_HEAD()
#         rate = rospy.Rate(5)
#         while not rospy.is_shutdown():
#             head.close_view()
#             rate.sleep()
#     except rospy.ROSInterruptException:
#         rospy.loginfo("Test is complete")

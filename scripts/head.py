from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
class move_head(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.head_cmd = rospy.Publisher('/head_controller/command', JointTrajectory, queue_size=1)


    def execute(self, userdata):
        jt = JointTrajectory()
        jt.joint_names = ['head_1_joint', 'head_2_joint']
        jtp = JointTrajectoryPoint()
        jtp.positions = [0.4, 0.1]
        jtp.time_from_start = rospy.Duration(2.0)
        jt.points.append(jtp)
        self.head_cmd.publish(jt)
        return 'done'

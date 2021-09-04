#!/usr/bin/env python

from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped, PointStamped
from geometry_msgs.msg import Pose, Point, Quaternion


class Coordinates():

    def __init__(self):
        self.home = PoseStamped()
        self.paso = PoseStamped()
        self.point1 = PoseStamped()
        self.point2 = PoseStamped()
        self.table1 = PoseStamped()
        self.table2 = PoseStamped()
        self.table3 = PoseStamped()
        self.table4 = PoseStamped()
        self.table5 = PoseStamped()
        self.table6 = PoseStamped()

    def init_location(self):

        self.home.header.frame_id = "map"
        self.home.pose.position.x = -0.368254032203
        self.home.pose.position.y = 0.823348215471
        self.home.pose.orientation.z = 0.000313931962172
        self.home.pose.orientation.w = 0.999999950723

        self.point1.header.frame_id = "map"
        self.point1.pose.position.x = 3.35886874737
        self.point1.pose.position.y = 0.324034682627
        self.point1.pose.orientation.z = 0.129108324977
        self.point1.pose.orientation.w = 0.991630495912

        self.point2.header.frame_id = "map"
        self.point2.pose.position.x = 6.12895165097
        self.point2.pose.position.y = 0.36917317753
        self.point2.pose.orientation.z = 0.0141001504049
        self.point2.pose.orientation.w = 0.999900587938

        self.paso.header.frame_id = "map"
        self.paso.pose.position.x = 0.480344302564
        self.paso.pose.position.y = -1.37227130362
        self.paso.pose.orientation.z = -0.996678161032
        self.paso.pose.orientation.w = 0.0814410420045

        self.table1.header.frame_id = "map"
        self.table1.pose.position.x = 2.70123527244
        self.table1.pose.position.y = 0.279692458048
        self.table1.pose.orientation.z = 0.846659897686
        self.table1.pose.orientation.w = 0.532134398109

        self.table2.header.frame_id = "map"
        self.table2.pose.position.x = 4.07672339902
        self.table2.pose.position.y = 0.394613572188
        self.table2.pose.orientation.z = -0.900374967038
        self.table2.pose.orientation.w = 0.435114833959

        self.table3.header.frame_id = "map"
        self.table3.pose.position.x = 4.05819400471
        self.table3.pose.position.y = 0.0744841087051
        self.table3.pose.orientation.z = 0.666187683749
        self.table3.pose.orientation.w = 0.745784130979

        self.table4.header.frame_id = "map"
        self.table4.pose.position.x = 5.35074645611
        self.table4.pose.position.y = 0.64713141245
        self.table4.pose.orientation.z = -0.689793332612
        self.table4.pose.orientation.w = 0.724006324755

        self.table5.header.frame_id = "map"
        self.table5.pose.position.x = 6.77527952194
        self.table5.pose.position.y = -0.0664653778076
        self.table5.pose.orientation.z = 0.720783467242
        self.table5.pose.orientation.w = 0.693160294124

        self.table6.header.frame_id = "map"
        self.table6.pose.position.x = 7.59110307693
        self.table6.pose.position.y = 0.630295038223
        self.table6.pose.orientation.z = -0.720957630938
        self.table6.pose.orientation.w = 0.692979144269

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



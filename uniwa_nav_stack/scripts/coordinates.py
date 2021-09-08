#!/usr/bin/env python

from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped, PointStamped
from geometry_msgs.msg import Pose, Point, Quaternion



class Coordinates():
    def __init__(self):
        self.home = PoseStamped()
        self.paso = PoseStamped()
        self.resting_area = PoseStamped()
        self.table1 = PoseStamped()
        self.table2 = PoseStamped()
        self.table3 = PoseStamped()
        self.table4 = PoseStamped()
        self.table5 = PoseStamped()
        self.table6 = PoseStamped()

        self.table1_walk = PoseStamped()
        self.table2_walk = PoseStamped()
        self.table3_walk = PoseStamped()
        self.table4_walk = PoseStamped()
        self.table5_walk = PoseStamped()
        self.table6_walk = PoseStamped()

        self.check456 = PoseStamped()
        self.check123 = PoseStamped()

        # self.table1_close = PoseStamped()
        # self.table2_close = PoseStamped()
        # self.table3_close = PoseStamped()
        # self.table4_close = PoseStamped()
        # self.table5_close = PoseStamped()
        # self.table6_close = PoseStamped()

    def init_location(self):
        self.home.header.frame_id = "map"
        self.home.pose.position.x = -0.368254032203
        self.home.pose.position.y = 0.823348215471
        self.home.pose.orientation.z = 0.000313931962172
        self.home.pose.orientation.w = 0.999999950723

        self.resting_area.header.frame_id = "map"
        self.resting_area.pose.position.x = 7.73432200973
        self.resting_area.pose.position.y = 0.489346738967
        self.resting_area.pose.orientation.z = -0.998817291787
        self.resting_area.pose.orientation.w = 0.0486211643896

        self.paso.header.frame_id = "map"
        self.paso.pose.position.x = 0.809605985728
        self.paso.pose.position.y = -1.50000389738
        self.paso.pose.orientation.z = -0.999871381845
        self.paso.pose.orientation.w = 0.0160380724049

        # self.check456.header.frame_id = "map"
        # self.check456.pose.position.x = 6.42291343313
        # self.check456.pose.position.y = 0.560197763387
        # self.check456.pose.orientation.z = -0.476521284588
        # self.check456.pose.orientation.w = 0.879162934464
        #
        # self.check123.header.frame_id = "map"
        # self.check123.pose.position.x = 0.809605985728
        # self.check123.pose.position.y = -1.50000389738
        # self.check123.pose.orientation.z = -0.999871381845
        # self.check123.pose.orientation.w = 0.0160380724049

        self.table1.header.frame_id = "map"
        self.table1.pose.position.x = 1.76306789749
        self.table1.pose.position.y = 0.58659606919
        self.table1.pose.orientation.z = 0.671191829793
        self.table1.pose.orientation.w = 0.741283702519

        self.table2.header.frame_id = "map"
        self.table2.pose.position.x = 3.08002523475
        self.table2.pose.position.y = 0.23424823733
        self.table2.pose.orientation.z = -0.755741129305
        self.table2.pose.orientation.w = 0.654870479925


        self.table3.header.frame_id = "map"
        self.table3.pose.position.x = 4.12079896376
        self.table3.pose.position.y = 0.41217322047
        self.table3.pose.orientation.z = 0.703120808711
        self.table3.pose.orientation.w = 0.711070410268

        self.table4.header.frame_id = "map"
        self.table4.pose.position.x = 5.33108583787
        self.table4.pose.position.y = 0.135051982219
        self.table4.pose.orientation.z = -0.70738636717
        self.table4.pose.orientation.w = 0.706827084613

        self.table5.header.frame_id = "map"
        self.table5.pose.position.x = 6.49050697901
        self.table5.pose.position.y = 0.369917492411
        self.table5.pose.orientation.z = 0.715375996466
        self.table5.pose.orientation.w = 0.698739710965

        self.table6.header.frame_id = "map"
        self.table6.pose.position.x = 7.40216773005
        self.table6.pose.position.y = 0.104594721278
        self.table6.pose.orientation.z = -0.70111048581
        self.table6.pose.orientation.w = 0.713052653516
# ---------------------------------------------------------------

        self.table1_walk.header.frame_id = "map"
        self.table1_walk.pose.position.x = 1.14804641842
        self.table1_walk.pose.position.y = -0.446458449757
        self.table1_walk.pose.orientation.z = 0.224081398612
        self.table1_walk.pose.orientation.w = 0.974570431932

        self.table2_walk.header.frame_id = "map"
        self.table2_walk.pose.position.x = 3.91207566295
        self.table2_walk.pose.position.y = 0.501907059278
        self.table2_walk.pose.orientation.z = -0.999745632367
        self.table2_walk.pose.orientation.w = 0.0225537261307

        self.table3_walk.header.frame_id = "map"
        self.table3_walk.pose.position.x = 3.65146318495
        self.table3_walk.pose.position.y = 0.0855626319331
        self.table3_walk.pose.orientation.z = 0.0519814727958
        self.table3_walk.pose.orientation.w = 0.998648049358

        self.table4_walk.header.frame_id = "map"
        self.table4_walk.pose.position.x = 5.78267488038
        self.table4_walk.pose.position.y = 0.591859940023
        self.table4_walk.pose.orientation.z = -0.999865831257
        self.table4_walk.pose.orientation.w = 0.0163804604666

        self.table5_walk.header.frame_id = "map"
        self.table5_walk.pose.position.x = 5.40488573868
        self.table5_walk.pose.position.y = 0.255674939855
        self.table5_walk.pose.orientation.z = -0.0169001818853
        self.table5_walk.pose.orientation.w = 0.999857181728

        self.table6_walk.header.frame_id = "map"
        self.table6_walk.pose.position.x = 7.83246841936
        self.table6_walk.pose.position.y = 0.636383742723
        self.table6_walk.pose.orientation.z = -0.997657808928
        self.table6_walk.pose.orientation.w = 0.0684024581833

    # def init_location_close(self):
    #     self.table1_close.header.frame_id = "map"
    #     self.table1_close.pose.position.x = 1.86509620758
    #     self.table1_close.pose.position.y = 0.119258913292
    #     self.table1_close.pose.orientation.z = 0.0265808499921
    #     self.table1_close.pose.orientation.w = 0.9996466
    #
    #     self.table2_close.header.frame_id = "map"
    #     self.table2_close.pose.position.x = 3.08002523475
    #     self.table2_close.pose.position.y = 0.23424823733
    #     self.table2_close.pose.orientation.z = -0.755741129305
    #     self.table2_close.pose.orientation.w = 0.654870479925
    #
    #     self.table3_close.header.frame_id = "map"
    #     self.table3_close.pose.position.x = 4.05819400471
    #     self.table3_close.pose.position.y = 0.0744841087051
    #     self.table3_close.pose.orientation.z = 0.666187683749
    #     self.table3_close.pose.orientation.w = 0.745784130979
    #
    #     self.table4_close.header.frame_id = "map"
    #     self.table4_close.pose.position.x = 5.35074645611
    #     self.table4_close.pose.position.y = 0.64713141245
    #     self.table4_close.pose.orientation.z = -0.689793332612
    #     self.table4_close.pose.orientation.w = 0.724006324755
    #
    #     self.table5_close.header.frame_id = "map"
    #     self.table5_close.pose.position.x = 6.77527952194
    #     self.table5_close.pose.position.y = -0.0664653778076
    #     self.table5_close.pose.orientation.z = 0.720783467242
    #     self.table5_close.pose.orientation.w = 0.693160294124
    #
    #     self.table6_close.header.frame_id = "map"
    #     self.table6_close.pose.position.x = 7.59110307693
    #     self.table6_close.pose.position.y = 0.630295038223
    #     self.table6_close.pose.orientation.z = -0.720957630938
    #     self.table6_close.pose.orientation.w = 0.692979144269

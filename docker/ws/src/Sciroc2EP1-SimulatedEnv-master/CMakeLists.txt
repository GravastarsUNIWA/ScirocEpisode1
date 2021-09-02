cmake_minimum_required(VERSION 2.8.3)
project(sciroc_ep1_object_manager)


find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  roscpp
  rospy
  sensor_msgs
  std_msgs
  message_generation
)



## Generate services in the 'srv' folder
add_service_files(
  FILES
  MoveItemsOnTheTray.srv
  MoveItemsOnClosestTable.srv
  GetThreeOrderedItems.srv
  ChangeTheItem.srv
)

## Generate actions in the 'action' folder
# add_action_files(
#   FILES
#   Action1.action
#   Action2.action
# )

## Generate added messages and services with any dependencies listed here
generate_messages(
   DEPENDENCIES
   geometry_msgs   sensor_msgs   std_msgs
 )


catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES eurobench_worldstate_provider
#  CATKIN_DEPENDS geometry_msgs roscpp rospy sensor_msgs std_msgs
   CATKIN_DEPENDS message_runtime
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)


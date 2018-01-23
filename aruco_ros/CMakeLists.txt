cmake_minimum_required(VERSION 2.8.3)
project(aruco_ros)
add_definitions(-std=c++11)

find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  dynamic_reconfigure
  geometry_msgs
  image_transport
  roscpp
  rospy
  tf
  aruco_msgs
  sensor_msgs
  visualization_msgs
)

set(aruco_DIR $ENV{HOME}/Tools/libaruco
    CACHE PATH "Location of Aruco library"
)

find_package(OpenCV REQUIRED)

find_library(aruco_LIB aruco PATHS ${aruco_DIR}/lib)
if(${aruco_LIB} EQUAL "aruco_LIB-NOTFOUND")
    message(WARNING "Aruco library not found at: " ${aruco_DIR})
else()
    message(STATUS "Aruco library at: " ${aruco_LIB})
endif()
set(aruco_INCLUDE_DIRS ${aruco_DIR}/include)

generate_dynamic_reconfigure_options(
  cfg/ArucoThreshold.cfg
)

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES aruco_ros_utils
  CATKIN_DEPENDS sensor_msgs tf
)

include_directories(
  include
  ${aruco_INCLUDE_DIRS}
  ${catkin_INCLUDE_DIRS}
)
#add_library(aruco_ros_utils src/aruco_ros_utils.cpp)
#target_link_libraries(aruco_ros_utils ${OpenCV_LIBRARIES} ${aruco_LIB} ${catkin_LIBRARIES})

#add_executable(single src/simple_single.cpp
#src/aruco_ros_utils.cpp)
#add_dependencies(single ${PROJECT_NAME}_gencfg)
#target_link_libraries(single ${aruco_LIB} ${catkin_LIBRARIES})

#add_executable(double src/simple_double.cpp
#src/aruco_ros_utils.cpp)
#add_dependencies(double ${PROJECT_NAME}_gencfg)
#target_link_libraries(double ${aruco_LIB} ${catkin_LIBRARIES})

add_executable(marker_publisher src/marker_publish.cpp
                                src/aruco_ros_utils.cpp)
add_dependencies(marker_publisher ${PROJECT_NAME}_gencfg)
target_link_libraries(marker_publisher ${OpenCV_LIBRARIES} ${aruco_LIB} ${catkin_LIBRARIES})

#############
## Install ##
#############

#install(TARGETS single double marker_publisher aruco_ros_utils
install(TARGETS marker_publisher
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY include/
   DESTINATION ${CATKIN_GLOBAL_INCLUDE_DESTINATION}
   FILES_MATCHING PATTERN "*.h"
)

foreach(dir etc launch)
    install(DIRECTORY ${dir}/
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)


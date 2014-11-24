#!/usr/bin/env python

import rospy
from aruco_ros.msg import MarkerArray

class MarkerTracker(object):
    def __init__(self, topic):
        #Create the subscriber
        self._marker_sub = rospy.Subscriber(
                topic,
                MarkerArray, 
                callback = self.marker_callback,
                queue_size = 10)
        #Create the empty marker list to be populated later
        self._markers = dict()

    #Callback that will run whenever a new message arrives
    def marker_callback(self, msg):
        #Store just the geometry_msgs/Pose part of the marker in a dictionary
        #There's also a m.header to check the timestamp
        for m in msg.markers:
            self._markers[m.id] = m.pose

    #Accessor function to get the marker data. Usually you don't directly
    #access the member variables because the accessor might want to validate or
    #sanitize the info given out
    def get_marker(self, id):
        return self._markers[id]

if __name__ == "__main__":
    rospy.init_node("marker_tracker")

    m_id = 101
    tracker = MarkerTracker("markers")

    while not rospy.is_shutdown():
        try:
            mkr = tracker.get_marker(m_id)
            print("Marker at height: %3.2f" % mkr.position.z)
        except KeyError:
            print("Marker %i not seen" % m_id)
        rospy.sleep(1.0)

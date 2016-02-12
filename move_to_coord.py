#!/usr/bin/env python

import rospy
import argparse
import baxter_interface

from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)
from std_msgs.msg import Header

from baxter_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest,
)


def main(info): #limb, xp, yp, zp, xq, yq, zq, wq
   rospy.init_node("coord_to_joint_ik_client")
   ns = "/ExternalTools/" + info[0] + "/PositionKinematicsNode/IKService"
   iksvc = rospy.ServiceProxy(ns, SolvePositionIK)
   ikreq = SolvePositionIKRequest()
   dr = Header(stamp=rospy.Time.now(), fram_id='base')
   
   poses = {
      'left': PoseStamped(
         header=hdr,
         pose=Pose(
            position=Point(
               x=info[1], 
               y=info[2], 
               z=info[3],
            ), 
            orientation=Quaternion(
               x=info[4], 
               y=info[5], 
               z=info[6], 
               w=info[7],
            ),
         ),
      ),
      'right': PoseStamped(
         header=hdr, 
         pose=Pose(
            position=Point(
               x=info[1], 
               y=info[2], 
               z=info[3],
            ), 
            orientation=Quaternion(
               x=info[4], 
               y=info[5], 
               z=info[6], 
               w=info[7],
            ),
         ),
      ),
   }
   
   ikreq.pose_stamp.append(poses[info[0]])
   try:
      resp = iksvc(ikreq)
   except:
      rospy.logerr("Service call failed: %s" % (e,))
   
   if (resp.isValid):
      joints = dict(zip(resp.joints[0].name, resp.joints[0].position))
      print "Found joint solution:"
      print joints + "\n"
      print "Complete response:\n" + resp + "\n"
      print "Moving " + info[0] + " arm...\n"
      move_to_solution(info[0], joints)
   else;
      print "Invalid Pose"
   return 0
   
   
def move_to_solution(limb, joints):
   my_limb = baxter_interface.Limb(limb)
   my_limb.move_to_joint_positions(joints)
   print "Moving complete.\n"
   return 0


if __name__ == "__main__":
   parse = argparse.ArgumentParser()
   parse.add_argument("limb", choices=['left', 'right'], help="Select limb")
   parse.add_argument("xp", help="Position Coord. x")
   parse.add_argument("yp", help="Position Coord. y")
   parse.add_argument("zp", help="Position Coord. z")
   parse.add_argument("xq", help="Orientation x")
   parse.add_argument("yq", help="Orientation y")
   parse.add_argument("zq", help="Orientation z")
   parse.add_argument("wq", help="Orientation w")
   
   args = parse.parse_args()
   info = [args.limb, args.xp, args.yp, args.zp, args.xq, args.yq, args.zq, args.wq]
   main(info)

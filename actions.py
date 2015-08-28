import motion
import almath
import math
import time
import goal
import sys
import random
from naoqi import ALProxy
from naoqi import ALModule
from naoqi import ALBroker


from optparse import OptionParser


motionProxy = None
postureProxy = None
autoLifeProxy = None
memoryProxy = None
trackerProxy = None
speechProxy = None
target = None
searchFor = None
NAO_IP = "169.254.44.123"





class actionsInit:

    goalAchieved = True

    def init(self):

        global motionProxy
        global postureProxy
        global autoLifeProxy
        global memoryProxy
        global trackerProxy
        global speechProxy

        parser = OptionParser()
        parser.add_option("--pip", help = "Parent Broker Port", dest="pip")
        parser.add_option("--pport", help = "port", dest="pport")
        parser.set_defaults(pip=NAO_IP, pport=9559)
        (opts, args_) = parser.parse_args()
        pip = opts.pip
        pport = opts.pport

        myBroker = ALBroker("myBroker", "0.0.0.0", 0, pip, pport)


        motionProxy = ALProxy("ALMotion")
        postureProxy = ALProxy("ALRobotPosture")
        autoLifeProxy = ALProxy("ALAutonomousLife")
        memoryProxy = ALProxy("ALMemory")
        trackerProxy = ALProxy("ALTracker")
        speechProxy = ALProxy("ALAnimatedSpeech")

        
        

                
        
        
    def toggleAutoLife(self):
        autoLifeProxy.setState("disabled")
    

         

class moveTo:

    precondition = "target_Known"
    effect = "at_target"
    cost = 2
    at_Target = False
    

    def move(moveX, moveY, moveR):
        motionProxy.moveTo(moveX, moveY, moveR)
        moveTo.at_Target = True
        stand.standing = False
        print "Robot is moving to X: " + str(movX) + ", Y: " + str(movY) + "."

class wakeUp:

    precondition = "asleep"
    effect = "awake"
    cost = 1
    awake = False

    def wake(self):
        motionProxy.wakeUp()
        wakeUp.awake = True
        rest.asleep = False
        print "Robot has woken up."
        
        

class rest:

    precondition = "awake"
    effect = "asleep"
    cost = 1
    asleep = None

    def rest(self):
        motionProxy.rest()
        rest.asleep = True
        wakeUp.awake = False
        print "Robot is asleep."
        

class kickBall:

    precondition = "at_Ball"
    effect = "ball_Kicked"
    cost = 2
    ball_Kicked = False
    

    def kick(self):
        print "moving to kick ball"
        motionProxy.moveTo(0.4,0.0,0)
        speechProxy.say("Kicking the ball")
        frame = motion.FRAME_TORSO
        axisMask = almath.AXIS_MASK_ALL
        useSensorValues = False
        effector = "LLeg"
        initTf = almath.Transform()

        try:
            initTf = almath.Transform(motionProxy.getTransform(effector, frame, useSensorValues))
        except Exception, errorMsg:
            print str(errorMsg)
            print "This action will not work on this Nao version."
            exit()

        deltaTf = almath.Transform(0.4,0,0.0)*almath.Transform().fromRotZ(0.0*almath.TO_RAD)
        targetTf = initTf*deltaTf
        path = list(targetTf.toVector())
        times = 0.2

        motionProxy.transformInterpolations(effector, frame, path, axisMask, times)
        kickBall.ball_Kicked = True
        stand.stadning = False
        

class stand:

    precondition = "awake"
    effect = "standing"
    cost = 1
    standing = False

    def goToStand(self):
        postureProxy.goToPosture("StandInit", 0.5)
        stand.standing = True
        print "The robot is now standing"

        

class trackFace:

    precondition = "standing"
    effect = "tracking_Face"
    cost = 2
    tracking_Face = False

    def track(self, targetName):

        if targetName == "Face":
            diameterOfFace = 0.10
            trackerProxy.registerTarget(targetName, diameterOfFace)

            mode = "Head"
            trackerProxy.setMode(mode)

            print "Tracker started, robot is tracking: " + targetName
            trackFace.tracking_Face = True
            stand.standing = False

class trackBall:

    precondition = "standing"
    effect = "tracking_Ball"
    cost = 1
    tracking_Ball = False

    def track(self, targetName):

        if targetName == "RedBall":
            diameterOfBall = 0.05
            trackerProxy.registerTarget(targetName, diameterOfBall)

            mode = "Head"
            trackerProxy.setMode(mode)

            trackerProxy.track(targetName)

            print "Tracker started, robot is tracking: " + targetName
            trackBall.tracking_Ball = True
            stand.standing = False


class followFace:

    precondition = "tracking_Face"
    effect = "following_Face"
    cost = 1
    following_Face = False

    def follow(self):

        mode = "Move"
        trackerProxy.setMode(mode)
        followFace.following_Face = True
        stand.standing = False

        try:
            while trackerProxy.isTargetLost() == False:

                distanceFromTarget = trackerProxy.getTargetPosition(2)

                if distanceFromTarget[0] <= 0.6:
                    mode = "Head"
                    trackerProxy.setMode(mode)

                if distanceFromTarget[0] > 0.6:
                    mode = "Move"
                    trackerProxy.setMode(mode)

                if trackerProxy.isTargetLost():
                    return
                time.sleep(1)
        except KeyboardInterrupt:
            print "Stopping follow"

class moveToBall:

    precondition = "tracking_Ball"
    effect = "at_Ball"
    cost = 1
    at_Ball = False

    def move(self):

        
        stand.standing = False
        t = trackerProxy.getActiveTarget()
        print t
        if trackerProxy.isTargetLost():
            print "lost the ball"
            moveToBall.atBall = False
        
        while not trackerProxy.isTargetLost():
            mode = "Move"
            trackerProxy.setMode(mode)
            distanceFromTarget = trackerProxy.getTargetPosition(2)
            print "got into the loop"
            if distanceFromTarget[0] <= 0.6:
                print "NAO arrived at location."
                
                moveToBall.at_Ball = True
                mode = "Head"
                trackerProxy.setMode(mode)
                return
            if trackerProxy.isTargetLost():
                actionsInit.goalAchieved = True
                print "Lost target!"
                return

            time.sleep(1)
        if moveToBall.at_Ball == False:
            print "not at the ball"
            actionsInit.goalAchieved = True
            print "the goal is achieved: " + str(actionsInit.goalAchieved)
        stopTracking()

class moveToFace:
    precondition = "tracking_Face"
    effect = "at_Face"
    cost = 1
    at_Face = False

    def move(self):

        
        
        stand.standing = False
        print "walking to face"
        
        while not trackerProxy.isTargetLost():
            mode = "Move"
            trackerProxy.setMode(mode)
            distanceFromTarget = trackerProxy.getTargetPosition(2)
            if distanceFromTarget[0] <= 0.6:
                print "Nao arrived at location."
                moveToFace.at_Face = True
                mode = "Head"
                trackerProxy.setMode(mode)
                return
            if trackerProxy.isTargetLost():
                actionsInit.goalAchieved = True
                print "Lost target!"
                return

            time.sleep(1)
        if moveToFace.at_Face == False:
            print "not at the face"
            actionsInit.goalAchieved = True
            print "the goal is achieved: " + str(actionsInit.goalAchieved)
        stopTracking()
        


class searchForObject:

    precondition = "standing"
    effect = "area_Searched"
    cost = 4
    area_Searched = False
    
    def search(self):


        print "Searching"
    
        global target
        
        effector = "Head"
        isEnabled = True
        motionProxy.wbEnableEffectorControl(effector, isEnabled)

        count = 1

        while count != 4 and goal.Goal.target == "Nothing":
            targetCoordinateList = [
            [00.0, 00.0, +30.0],
            [00.0, -75.0, +30.0],
            [00.0, +75.0, +30.0],
            [00.0, 00.0, 00.0],
            [00.0, -75.0, 00.0],
            [00.0, +75.0, 00.0],
            [00.0, 00.0, -30.0],
            [00.0, -75.0, -30.0],
            [00.0, +75.0, -30.0]
            ]
            if goal.Goal.target == "Nothing":
                for targetCoordinate in targetCoordinateList:
                    targetCoordinate = [target*math.pi/180.0 for target in targetCoordinate]
                    motionProxy.wbSetEffectorControl(effector, targetCoordinate)
                    time.sleep(0.5)

            if goal.Goal.target == "Nothing":
                motionProxy.moveTo(0,0,1.57)
                count +=1
            if goal.Goal.target == "RedBall" or "Face":
                return
        isEnabled = False
        motionProxy.wbEnableEffectorControl(effector, isEnabled)

        stand.standing = False
        searchForObject.area_Searched = True
        stopTracking()
        

class robotIdle:
    precondition = "standing"
    effect = "robot_Idle"
    cost = 5
    robot_Idle = False

    def idle(self):

        selection = random.randint(1,4)

        print str(selection)
        if selection == 1:
            motionProxy.moveTo(0.1,0.1,1.5)
            motionProxy.moveTo(-0.1,0.1,1.5)
            robotIdle.robot_Idle = True
            stand.standing = False
        elif selection == 2:
            motionProxy.moveTo(-0.1,-0.1,1.5)
            robotIdle.robot_Idle = True
            stand.standing = False
        elif selection == 3:
            postureProxy.goToPosture("Sit", 1.0)
            time.sleep(2)
            postureProxy.goToPosture("SitRelax", 1.0)
            time.sleep(4)
            postureProxy.goToPosture("Stand", 1.0)
            robotIdle.robot_Idle = True
            stand.standing = False
        elif selection == 4:
            targetCoordinateList = [
            [00.0, 00.0, +30.0],
            [00.0, 00.0, -30.0],
            [00.0, 00.0, 00.0]
            ]

            motionProxy.wbEnableEffectorControl("Head", True)
            for targetCoordinate in targetCoordinateList:
                targetCoordinate = [target*math.pi/180 for target in targetCoordinate]
                motionProxy.wbSetEffectorControl("Head", targetCoordinate)

            motionProxy.wbEnableEffectorControl("Head", False)
            robotIdle.robot_Idle = True

        stand.standing = False
            
            

class greetFace:
    precondition = "at_Face"
    effect = "face_Greeted"
    cost = 3
    face_Greeted = False

    def greet(self):
        speechProxy.say("^start(animations/Stand/Gestures/Hey_1) \\pau=500\\ Hello")
        greetFace.face_Greeted = True
        stand.standing = False


def stopTracking():
    mode = "Head"
    trackerProxy.setMode(mode)
    trackerProxy.stopTracker()
    trackerProxy.unregisterAllTargets()
    trackFace.tracking_Face = False
    trackBall.tracking_Ball = False
    print "Tracker Stopped"

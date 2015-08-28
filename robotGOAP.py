import actions
import actionsList
import planner
import goal
import time
import math


listOfActions = []
step = None
movX = None
movY = None
movR = None

ballEvent = None
faceEvent = None
ballSub = None
faceSub = None
from naoqi import ALModule
from naoqi import ALProxy
memoryProxy  = None
postureProxy = None
motionProxy = None
searchTime = 0.0



def main():

    #print "Enter the IP of the robot: "
    #robotIP = raw_input()

    #print "Enter the PORT of the robot: "
    #robotPORT = int(raw_input())
    global searchTime
    searchTime = time.clock()
    global memoryProxy
    global postureProxy
    global motionProxy
    global speechProxy
    global ballSub
    global faceSub

    goal.Goal.target = "Nothing"
    print goal.Goal.target
    
    a = actions.actionsInit()  
    a.init()

    a.toggleAutoLife()
    r = actions.rest()
    r.rest()
    
    
    action = actionsList.actionsList()
    action.init()
    
    memoryProxy = ALProxy("ALMemory")
    postureProxy = ALProxy("ALRobotPosture")
    motionProxy = ALProxy("ALMotion")
    speechProxy = ALProxy("ALAnimatedSpeech")
    
    global ballEvent
    ballEvent = ballEventListener("ballEvent")

    global faceEvent
    faceEvent = faceEventListener("faceEvent")

    actions.actionsInit.goalAchieved = True
    
    try:
        while True:
            aStarPlanner()
            time.sleep(1)
    except KeyboardInterrupt:
        ballEvent.unsub()
        faceEvent.unsub()
        actions.stopTracking()
        quit()

def getTarget():
    return target

def aStarPlanner():

    g = goal.Goal()
    p = planner.aStarPlanner()


    global listOfActions
    global step
    
    if actions.actionsInit.goalAchieved == True:
        actions.actionsInit.goalAchieved = False
        listOfActions = []
        robotGoal = g.findGoal()
        g.updateWorldModel()

        if goal == "idle":
            return
        else:
            p.planner(robotGoal)
            step = p.step
            i=0
            for index in range(len(p.actions)):
                listOfActions.append(p.actions[(p.step-1)-i])
                i+=1
            

    count = 0
    for index in range(len(listOfActions)):
            print str((count)+1) + ": " + listOfActions[count]
            count+=1

    
    if actions.actionsInit.goalAchieved == False:
        finiteStateMachine()
            
                
            

def finiteStateMachine():

    if actions.actionsInit.goalAchieved == True:
        actions.stopTracking()
        return


    global step
    global listOfActions
    
    a = actionsList.actionsList()
    goal.Goal.target = "Nothing"

    print "The precondition is: " + str(a.checkEffect(a.findPrecondition(listOfActions[0])))
    if a.checkEffect(a.findPrecondition(listOfActions[0])) == True and step > 1:
        perform(listOfActions[0])
        del listOfActions[0]
        step-=1
    elif a.checkEffect(a.findPrecondition(listOfActions[0])) == True and step == 1:
        perform(listOfActions[0])
        del listOfActions[0]
        step-=1

    print "Goalachieved is: " + str(actions.actionsInit.goalAchieved)

    if actions.actionsInit.goalAchieved == True:
        for index in range(len(listOfActions)):
            del listOfActions[0]
        print "returning"
        return
    
    print listOfActions
    
    if step == 0:
        actions.actionsInit.goalAchieved = True
    else:
        actions.actionsInit.goalAchieved = False
        

def perform(action):

    global movX
    global movY
    global movR
    global target
    aList = actionsList.actionsList()

    print "Performing: " + action + "..."
    
    if action == "moveTo":
        m = actions.moveTo()
        m.move(movX, movY, movR)

    elif action == "wakeUp":
        w = actions.wakeUp()
        w.wake()

    elif action == "rest":
        r = actions.rest()
        r.rest()

    elif action == "kickBall":
        k = actions.kickBall()
        k.kick()

    elif action == "stand":
        s = actions.stand()
        s.goToStand()

    elif action == "trackBall":
        b = actions.trackBall()
        b.track("RedBall")

    elif action == "trackFace":
        f = actions.trackFace()
        f.track("Face")

    elif action == "followFace":
        ff = actions.followFace()
        ff.follow()

    elif action == "moveToFace":
        print "at perform"
        mf = actions.moveToFace()
        mf.move()

    elif action == "moveToBall":
        mb = actions.moveToBall()
        mb.move()

    elif action == "searchForObject":
        so = actions.searchForObject()
        ballEvent.sub()
        faceEvent.sub()
        so.search()
        if faceSub == True:
            faceEvent.unsub()
        if ballSub == True:
            ballEvent.unsub()
        searchTime = time.clock
    elif action == "robotIdle":
        ri = actions.robotIdle()
        ri.idle()
    elif action == "greetFace":
        gf = actions.greetFace()
        gf.greet()
    else:
        print "Error actions is not supported. Shutting down."
        exit()

    aList.setupCheckEffect()
    


class ballEventListener(ALModule):

    def __init__(self, name):

        ALModule.__init__(self, name)


    def onRedBall(self, *_args):
        print "NAO found a red ball"
        goal.Goal.target = "RedBall"
        ballSub = False
        memoryProxy.unsubscribeToEvent("redBallDetected", "ballEvent")
        motionProxy.stopAll()


    def sub(self):


        print "Resubbed to red ball event listener"
        memoryProxy.subscribeToEvent("redBallDetected", "ballEvent", "onRedBall")
        ballSub = True

    def unsub(self):
        print "unsubbed from ball detection"
        memoryProxy.unsubscribeToEvent("redBallDetected", "ballEvent")
        ballSub = False

        
    
class faceEventListener(ALModule):

    def __init__(self, name):

        ALModule.__init__(self, name)


    def onFaceDetection(self, *_args):
        print "NAO detected a face."
        if goal.Goal.target != "RedBall":
            goal.Goal.target = "Face"
            
        faceSub = False
        memoryProxy.unsubscribeToEvent("FaceDetected", "faceEvent")
        motionProxy.stopAll()
        

    def sub(self):

        print "Resubbed to facedectected event listener"
        memoryProxy.subscribeToEvent("FaceDetected", "faceEvent", "onFaceDetection")
        faceSub = True

    def unsub(self):
        print "unsubbed from face detection"
        memoryProxy.unsubscribeToEvent("FaceDetected", "faceEvent")
        faceSub = False



if __name__ == "__main__":
    main()

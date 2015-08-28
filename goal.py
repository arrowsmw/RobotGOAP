import actions
import actionsList
import time




class Goal:

    target = "."
    searchTime = 0.0    

    def findGoal(self):

        currTime = Goal.searchTime- time.clock()
        print "the target is: " + Goal.target
        if Goal.target == "RedBall":
            naoGoal = "ball_Kicked"
        elif Goal.target == "Face":
            naoGoal = "face_Greeted"
        elif Goal.target == "Nothing" and currTime <= -20.0:
            naoGoal = "area_Searched"
        else:
            naoGoal = "robot_Idle"

        return naoGoal

    def updateWorldModel(self):

        actions.searchForObject.area_Searched = False
        actions.robotIdle.robot_Idle = False
        actions.kickBall.ball_Kicked = False
        actions.moveToBall.at_Ball = False
        actions.moveToFace.at_Face = False
        actions.followFace.following_Face = False
        actions.moveTo.at_Target = False    
    
    

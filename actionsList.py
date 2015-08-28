import actions

class actionsList:

    cost = {}
    effect = {}
    precondition = {}
    actionFromEffect = {}
    effectFlag = {}

    def init(self):
        
        actionsList.setupCost(self)
        actionsList.setupEffect(self)
        actionsList.setupPrecondition(self)
        actionsList.setupActionFromEffect(self)
        actionsList.setupCheckEffect(self)

    def setupCost(self):

        actionsList.cost["greetFace"] = actions.greetFace.cost
        actionsList.cost["moveTo"] = actions.moveTo.cost
        actionsList.cost["wakeUp"] = actions.wakeUp.cost
        actionsList.cost["rest"] = actions.rest.cost
        actionsList.cost["kickBall"] = actions.kickBall.cost
        actionsList.cost["searchForObject"] = actions.searchForObject.cost
        actionsList.cost["trackFace"] = actions.trackFace.cost
        actionsList.cost["trackBall"] = actions.trackBall.cost
        actionsList.cost["moveToFace"] = actions.moveToFace.cost
        actionsList.cost["moveToBall"] = actions.moveToBall.cost
        actionsList.cost["stand"] = actions.stand.cost
        actionsList.cost["followFace"] = actions.followFace.cost
        actionsList.cost["robotIdle"] = actions.robotIdle.cost
        
    def setupEffect(self):
        
        actionsList.effect["greetFace"] = actions.greetFace.effect
        actionsList.effect["moveTo"] = actions.moveTo.effect
        actionsList.effect["wakeUp"] = actions.wakeUp.effect
        actionsList.effect["rest"] = actions.rest.effect
        actionsList.effect["kickBall"] = actions.kickBall.effect
        actionsList.effect["searchForObject"] = actions.searchForObject.effect
        actionsList.effect["trackBall"] = actions.trackBall.effect
        actionsList.effect["trackFace"] = actions.trackFace.effect
        actionsList.effect["stand"] = actions.stand.effect
        actionsList.effect["moveToBall"] = actions.moveToBall.effect
        actionsList.effect["moveToFace"] = actions.moveToFace.effect
        actionsList.effect["robotIdle"] = actions.robotIdle.effect
        actionsList.effect["followFace"] = actions.followFace.effect

    def setupPrecondition(self):

        actionsList.precondition["greetFace"] = actions.greetFace.precondition
        actionsList.precondition["moveTo"] = actions.moveTo.precondition
        actionsList.precondition["wakeUp"] = actions.wakeUp.precondition
        actionsList.precondition["rest"] = actions.rest.precondition
        actionsList.precondition["kickBall"] = actions.kickBall.precondition
        actionsList.precondition["searchForObject"] = actions.searchForObject.precondition
        actionsList.precondition["trackBall"] = actions.trackBall.precondition
        actionsList.precondition["trackFace"] = actions.trackFace.precondition
        actionsList.precondition["stand"] = actions.stand.precondition
        actionsList.precondition["moveToBall"] = actions.moveToBall.precondition
        actionsList.precondition["moveToFace"] = actions.moveToFace.precondition
        actionsList.precondition["robotIdle"] = actions.robotIdle.precondition
        actionsList.precondition["followFace"] = actions.followFace.precondition

    def setupActionFromEffect(self):

        actionsList.actionFromEffect["face_Greeted"] = list = ["greetFace"];
        actionsList.actionFromEffect["at_Location"] = list = ["moveTo"];
        actionsList.actionFromEffect["awake"] = list = ["wakeUp"];
        actionsList.actionFromEffect["asleep"] = list = ["asleep"];
        actionsList.actionFromEffect["ball_Kicked"] = list = ["kickBall"];
        actionsList.actionFromEffect["standing"] = list = ["stand"];
        actionsList.actionFromEffect["tracking_Ball"] = list= ["trackBall"];
        actionsList.actionFromEffect["tracking_Face"] = list = ["trackFace"];
        actionsList.actionFromEffect["at_Ball"] = list = ["moveToBall"];
        actionsList.actionFromEffect["at_Face"] = list = ["moveToFace"];
        actionsList.actionFromEffect["area_Searched"] = list = ["searchForObject"];
        actionsList.actionFromEffect["robot_Idle"] = list = ["robotIdle"];
        actionsList.actionFromEffect["following_Face"] = list = ["followFace"];

    def setupCheckEffect(self):

        actionsList.effectFlag["face_Greeted"] = actions.greetFace.face_Greeted
        actionsList.effectFlag["at_Target"] = actions.moveTo.at_Target
        actionsList.effectFlag["awake"] = actions.wakeUp.awake
        actionsList.effectFlag["asleep"] = actions.rest.asleep
        actionsList.effectFlag["ball_Kicked"] = actions.kickBall.ball_Kicked
        actionsList.effectFlag["standing"] = actions.stand.standing
        actionsList.effectFlag["tracking_Ball"] = actions.trackBall.tracking_Ball
        actionsList.effectFlag["tracking_Face"] = actions.trackFace.tracking_Face
        actionsList.effectFlag["area_Searched"] = actions.searchForObject.area_Searched
        actionsList.effectFlag["at_Ball"] = actions.moveToBall.at_Ball
        actionsList.effectFlag["at_Face"] = actions.moveToFace.at_Face
        actionsList.effectFlag["robot_Idle"] = actions.robotIdle.robot_Idle
        actionsList.effectFlag["following_Face"] = actions.followFace.following_Face

    def checkEffect(self, effect):

        if actionsList.effectFlag[effect] == True:
            return True
        else:
            return False

    def findPrecondition(self, action):

        return actionsList.precondition[action]

    def findEffect(self, action):

        return actionsList.effect[action]

    def getCost(self, action):

        return actionsList.cost[action]

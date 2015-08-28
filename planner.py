import actionsList

class aStarPlanner:

    step = 0
    actions = []
    count = 0
    


    def planner(self, goal):

        aStarPlanner.actions = []
        aStarPlanner.step = 0
        currAction = ""
        currPrecondition = ""
        preconditionFlag = False
        a = actionsList.actionsList()
        print aStarPlanner.actions

        if len(a.actionFromEffect[goal]) == 2:
            currAction = findCheapest(goal)
        else:
            currAction = a.actionFromEffect[goal][0]
            
        while preconditionFlag == False:

            aStarPlanner.actions.append(currAction)
            aStarPlanner.step+=1

            currPrecondition = a.findPrecondition(currAction)

            if a.checkEffect(currPrecondition) == True:
                preconditionFlag = True
            else:
                if len(a.actionFromEffect[currPrecondition]) == 2:
                    currAction = aStarPlanner.findCheapest(currPrecondition)
                else:
                    currAction = a.actionFromEffect[currPrecondition][0]

        print "the list of actions is: " + str(aStarPlanner.actions)

    def findCheapest(effect):

        a = actionsList.actionsList()
        
        actionCost1 = a.getCost(a.actionFromEffect[effect][0])
        actionCost2 = a.getCost(a.actionFromEffect[effect][1])

        if a.checkEffect(a.findPrecondition(a.actionFromEffect[effect][0])) == False:
            actionCost1+=1

        if a.checkEffecT(a.findPrecondition(a.actionFromEffect[effect][1])) == False:
            actionCost2+=1

        if actionCost1 <= actionCost2:
            return a.actionFromEffect[effect][0]
        else:
            return a.actionFromEffect[effect][1]
        

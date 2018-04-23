#It is better to create nodes to parse the files rather than use an array otherwise we will be repeating the same steps over and over again.

class Node:
    character = ''
    hueristic = -1
    nodeLeft = None
    nodeRight = None
    nodeAbove = None
    nodeBelow = None
    xLocation = -1
    yLocation = -1
    nodesLeadingToThis = [] #In Astar this keeps track of the nodes that where before it.
    checked = 0
    mapPosition = -1
    nodeDistance = {}


    def __init__(self, nodeAbove, nodeBelow, nodeRight, nodeLeft, character):
        self.character = character
        self.nodeAbove = nodeAbove
        self.nodeBelow = nodeBelow
        self.nodeLeft = nodeLeft
        self.nodeRight = nodeRight
        self.nodeDistance={}

    def checkedNode(self):
        self.checked = 1

    #returns 1 if all of the children have been checked, 0 if there is a child that needs to be checked out
    def checkOutChildren(self):
        flag = 1
        if (self.nodeAbove != None):
            if (self.nodeAbove.checked == 0 and self.nodeAbove.getChar() != '%'):
                flag = 0
        if (self.nodeBelow != None):
            if (self.nodeBelow.checked == 0 and self.nodeBelow.getChar() != '%'):
                flag = 0
        if (self.nodeLeft != None):
            if (self.nodeLeft.checked == 0 and self.nodeLeft.getChar() != '%'):
                flag = 0
        if (self.nodeRight != None):
            if (self.nodeRight.checked == 0 and self.nodeRight.getChar() != '%'):
                flag = 0
        return flag

    def setLocation(self,x,y):
        self.xLocation = x
        self.yLocation = y

    def setEdge(self, edgeValue, node):
        self.nodeDistance[node] = edgeValue



    def getLocation(self):
        return self.xLocation,self.yLocation

    def setAbove(self, node):
        self.nodeAbove = node

    def setHueristic(self, hueristic):
        self.hueristic = hueristic

    def getHueristic(self):
        return self.hueristic

    def setBelow(self, node):
        self.nodeBelow = node

    def setLeft(self, node):
        self.nodeLeft = node

    def setRight(self, node):
        self.nodeRight = node

    def setCharacter(self, character):
        self.character = character

    def setNodes(self, nodeAbove, nodeBelow, nodeRight, nodeLeft):
        self.nodeBelow = nodeBelow
        self.nodeAbove = nodeAbove
        self.nodeLeft = nodeLeft
        self.nodeRight = nodeRight

    def above(self):
        return self.nodeAbove

    def below(self):
        return self.nodeBelow

    def left(self):
        return self.nodeLeft

    def right(self):
        return self.nodeRight

    def getChar(self):
        return self.character

    #following is for testing
    def dumpData(self):
        print("Above is: {}, Below is {}, Right is {}, Left is {}, Char is {}".format(self.nodeAbove.getChar(), self.nodeBelow.getChar(), self.nodeRight.getChar(), self.nodeLeft.getChar(),self.character))

if __name__ == "__main__":
     pass
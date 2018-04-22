#This class represents the maze itself
from __future__ import print_function
from node import Node
XDIM = 500
YDIM = 500
WINSIZE = [XDIM,YDIM]
from geometry_msgs.msg import PoseStamped
import std_msgs.msg
import tf
import rospy
import time
import cv2

class Maze:
    startingNode = None
    height = 0
    width = 0
    exitNode = []
    nodeList = []
    nodesTraveled = 0
    map = None
    emptyMaze = None

    def __init__(self, maze):
        self.map = maze
        self.height = self.getHeight()
        self.width = self.getWidth()
        self.exitNode = []
        self.nodeList = []
        self.parse()
        



#Bulk of the ECE445 code is going to go here
    def positionInMaze(self):
        print("HI")
        pass

    def getLocalNodes(self, radius, referenceNode):
        localNodes = []
        referenceX = referenceNode.xLocation
        referenceY = referenceNode.yLocation
        legalPositions =[] #Contains all (x,y) tuples that are legel
        for x in range(-radius, radius+1):
            for y in range(-radius, radius+1):
                final_x = referenceX + x
                final_y = referenceY + y
                if(final_x < 0 or final_y > self.width or (final_x ==referenceX and final_y ==referenceY)):
                    continue
                if(final_y < 0 or final_y > self.height):
                    continue
                legalPositions.append( (final_x,final_y) )
        for node in self.nodeList:
            if( (node.xLocation,node.yLocation) in legalPositions and node.getChar() == '.'):
                localNodes.append(node)
        return localNodes





    def printPathSize(self, nodeList):
        counter = 0
        for node in nodeList:
            if node.getChar() != ' ' and node.getChar() != '%':
                counter +=1
        return counter

    #This assumes map passed in is similar in structure to unsolved map
    def printNodeList(self, nodeList):
        #print to screen
        for row in range(0,self.height):
            for column in range(0,self.width):
                print(self.nodeList[self.width*row + column].getChar(), end='')
            print('\n')
        #print to file
        f = open('data', 'w')
        for row in range(0,self.height):
            for column in range(0,self.width):
                f.write(self.nodeList[self.width*row + column].getChar())
            f.write('\n')

#This first fills in the nodeList list above that contains all the nodes, after that we go through the list and assign the nodes their left,rights,above, and belows by iterating over the list.
    def parse(self):
        #First fill nodeList
        for position in range(0,self.height*(self.width+1)-1):
            if(self.map[position] != '\n'):
                character = self.map[position]
                newNode = Node(None, None, None, None, character)
                newNode.mapPosition = position
                self.nodeList.append(newNode)
                if (character == 'P'):
                    self.startingNode = newNode
                elif (character == '.'):
                    self.exitNode.append(newNode)

        #Fill in location of node in (x,y) coordinates
        for row in range(0,self.height):
            for column in range(0,self.width):
                currentNode = self.nodeList[self.width*row + column]
                currentNode.setLocation(column,row)

        #The following loop fills in the neighboring node data for each node and gets their hueristic
        for position in range(0,len(self.nodeList)):
                #Create a new node
                nodeAbove= nodeBelow= nodeLeft= nodeRight = None
                currentNode = self.nodeList[position]
                nonReachableNode = None
                if (position - self.width < 0):
                    nodeAbove = nonReachableNode
                else:
                    nodeAbove = self.nodeList[position-self.width]

                if (position +self.width >= len(self.nodeList)):
                    nodeBelow = nonReachableNode
                else:
                    nodeBelow = self.nodeList[position+self.width]

                if (position % self.width == self.width-1):
                    nodeRight = nonReachableNode
                else:
                    nodeRight = self.nodeList[position+1]

                if (position % self.width == 0):
                    nodeLeft = nonReachableNode
                else:
                    nodeLeft = self.nodeList[position-1]

                currentNode.setNodes(nodeAbove, nodeBelow, nodeRight, nodeLeft)
                # Get hueristic and put in node
                currentNodeX, currentNodeY = currentNode.getLocation()
                finalNodeX, finalNodeY = self.exitNode[0].getLocation() #Hard coding this for one ending case
                manhattanX = abs(currentNodeX-finalNodeX)
                manhattanY = abs(currentNodeY-finalNodeY)
                currentNode.setHueristic(manhattanX+manhattanY)

    def getWidth(self):
        firstColumn = self.map.split('\n',1)[0]
        return firstColumn.count('%')

    def getHeight(self):
        return self.map.count('\n') + 1 #Add one because last line wont have new line.
    def turnDirections(self,arr):
        if(len(arr)==0):
            return []
        returnArray=[]
        startDirection="Go Up"#Orientation at P
        print("WE ARE CURRENTLY STARTING AT P IN DIRECTION: "+ startDirection)
        map={"Go Up":1,"Go Right":2,"Go Down":3,"Go Left":4}
        returnArray.append(90*(map[startDirection]-map[arr[0]]))
        for index,direction in enumerate(arr):
            try:
                turnValue=map[direction]-map[arr[index+1]]
                returnArray.append((turnValue*-90))
            except:
                pass
        return returnArray
#Pose Stamped message
    def aStar(self):
        exploreTuples = [(self.startingNode, self.startingNode.hueristic)]
        exploredNodes = []
        while (len(exploreTuples) != 0):
            lowestWeightNode = (
            None, self.width + self.height + 100000000)  # This is max size of manhattan distance + a lot
            for node, weight in exploreTuples:
                if weight <= lowestWeightNode[1]:
                    lowestWeightNode = (node, weight)
            if (lowestWeightNode[0] == None):
                print("FOOBAR")
            exploreTuples.remove(lowestWeightNode)
            outputArray=[]
            # This goes from . to P so we need to reverse everything
            if (lowestWeightNode[0].getChar() == '.'):
                if(lowestWeightNode[0].nodeAbove==lowestWeightNode[0].nodesLeadingToThis[0]):
                    outputArray.append("Go Down")
                if (lowestWeightNode[0].nodeBelow == lowestWeightNode[0].nodesLeadingToThis[0]):
                    outputArray.append("Go Up")
                if (lowestWeightNode[0].nodeLeft == lowestWeightNode[0].nodesLeadingToThis[0]):
                    outputArray.append("Go Right")
                if (lowestWeightNode[0].nodeRight == lowestWeightNode[0].nodesLeadingToThis[0]):
                    outputArray.append("Go Left")
                for index,nodes in enumerate(lowestWeightNode[0].nodesLeadingToThis):
                    if (nodes.getChar() != 'P'):  # Commenting this out so it doesnt edit map for unoptimzzed testing
                        nodes.setCharacter('o')
                        #This goes from . to P so we need to reverse everything
                        if(nodes.nodeAbove==lowestWeightNode[0].nodesLeadingToThis[index+1]):
                            outputArray.append("Go Down")
                        if(nodes.nodeBelow==lowestWeightNode[0].nodesLeadingToThis[index+1]):
                            outputArray.append("Go Up")
                        if(nodes.nodeLeft==lowestWeightNode[0].nodesLeadingToThis[index+1]):
                            outputArray.append("Go Right")
                        if(nodes.nodeRight==lowestWeightNode[0].nodesLeadingToThis[index+1]):#
                            outputArray.append("Go Left")


                self.printNodeList(self.nodeList)
                directionToGo=(outputArray[::-1])
                directionTurn=self.turnDirections(outputArray[::-1])
                poseArray=[]
		pub=rospy.Publisher('chatter',PoseStamped, queue_size=1000)
		rospy.init_node('demo_pub_node')		
		r=rospy.Rate(1)
                for index,direction in enumerate(directionToGo):
                    p=PoseStamped()
                    p.header.stamp=rospy.get_rostime()
                    p.header.frame_id='base_link'
                    p.pose.position.x=1#THIS MIGHT NEED TO BE CHANGED LATER. I ASSUME THAT IT IS ROTATE THEN MOVE
                    p.pose.position.y=0
                    p.pose.position.z=0
                    q=tf.transformations.quaternion_from_euler(directionTurn[index],0,0)
                    p.pose.orientation.x=q[0]
                    p.pose.orientation.y=q[1]
                    p.pose.orientation.z=q[2]
                    p.pose.orientation.w=q[3]
                    poseArray.append(p)

		#Set up ROS publishing
		
		i=0
                while not rospy.is_shutdown():
		    try:
			pub.publish(poseArray[i])
			key = cv2.waitKey(1) & 0xFF

	   		# if the `q` key was pressed, break from the loop
	   		if key == ord("i"):
	      		    i+=1
		    except Exception as e:
		        print(e)

                return len(lowestWeightNode[0].nodesLeadingToThis) + 1  # Include +1 to add distance to goal
            exploredNodes.append(lowestWeightNode[0])
            nodesBefore = [lowestWeightNode[0]] + lowestWeightNode[0].nodesLeadingToThis
            # Update childrens nodesBefore then put in explore
            if (lowestWeightNode[0].nodeBelow.getChar() != '%' and lowestWeightNode[0].nodeBelow not in exploredNodes):
                lowestWeightNode[0].nodeBelow.nodesLeadingToThis = nodesBefore
                exploreTuples.append(
                    (lowestWeightNode[0].nodeBelow, lowestWeightNode[0].nodeBelow.hueristic + len(nodesBefore)))
            if (lowestWeightNode[0].nodeAbove.getChar() != '%' and lowestWeightNode[0].nodeAbove not in exploredNodes):
                lowestWeightNode[0].nodeAbove.nodesLeadingToThis = nodesBefore
                exploreTuples.append(
                    (lowestWeightNode[0].nodeAbove, lowestWeightNode[0].nodeAbove.hueristic + len(nodesBefore)))
            if (lowestWeightNode[0].nodeLeft.getChar() != '%' and lowestWeightNode[0].nodeLeft not in exploredNodes):
                lowestWeightNode[0].nodeLeft.nodesLeadingToThis = nodesBefore
                exploreTuples.append(
                    (lowestWeightNode[0].nodeLeft, lowestWeightNode[0].nodeLeft.hueristic + len(nodesBefore)))
            if (lowestWeightNode[0].nodeRight.getChar() != '%' and lowestWeightNode[0].nodeRight not in exploredNodes):
                lowestWeightNode[0].nodeRight.nodesLeadingToThis = nodesBefore
                exploreTuples.append(
                    (lowestWeightNode[0].nodeRight, lowestWeightNode[0].nodeRight.hueristic + len(nodesBefore)))
        return -1


#THIS IS FOR TESTING ONLY, WRITE MAIN CODE IN main.py
if __name__ == "__main__":
    inmap1 = """%%%%%%%
%P%.  %
% %%% %
%     %
%%%%%%%"""

    maze = Maze(inmap1)
    maze.aStar()

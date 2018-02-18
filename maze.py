#This class represents the maze itself
from __future__ import print_function
from node import Node
XDIM = 500
YDIM = 500
WINSIZE = [XDIM,YDIM]



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


#THIS IS FOR TESTING ONLY, WRITE MAIN CODE IN main.py
if __name__ == "__main__":
    inmap1 = """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%         % %           %     %           %           %    .%
% %%%% %% % % %%%%% %%%%% %%% % %%%% %% %%% %% %% %%% % % % %
% %     %   %     %       %   %       %     %   % % %   % % %
% % %%% % %%%% %% %%%%%%%%% %%%%% %%% % %%% % % % % %%%%% % %
% %   %   %       %       %       %   %   % % % %     %   % %
% % %%% %%% %%% %%% % %%% %%%% %% % %%% % %%% % %%% %%% %%% %
%   %     %     %   % %         % % %   %     %   % %   % % %
% %%% %%% %%%%% %%%%% % %%% %%% %%%%% %%%%%% %%%% %%% %%% % %
%     %       %         % % %         %   %     %     %   % %
% %%%%% %%%%% %%%%% %%% % % % %%%%%%%%% % % %%% %%% %%% %%% %
% %   % %   %         % %   % %     %   % % %           %   %
% % %%% % %%% %%%%% % % %%%%% % % %%% % % %%% %%%%% %%%%% %%%
%   %   % %       % % %   %   % %   % % %     %     %   % % %
% %%% %%% % % %%% %%% %%% % %%% %%% % % %%%%%%%%% %%% % % % %
% %   %   % %   %   % %   % %     %   %   %     % %   %   % %
%   %%% % % % % % % % % %%% % %%%%%%% %%% % %%% % % %%%%%%% %
% %   % %   % %   %   % %                 % %   % % %       %
% %%% %%% %%% %%% % %%% % %%% % %%%%%% %%%% % %%%%% % % %%% %
%   %         %   % %   % %   %         %   % %     % % %   %
%%% %%% % %%%%% %%%%% %%%%% %%% %%%%%%% % %%% % %%%%%%% % %%%
%P    %       %             %         %     %           %   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""


    maze = Maze(inmap1)
    maze.parse()

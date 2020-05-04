#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from IPython.display import clear_output 
import random 
import numpy
#import py_getch

class Cube:
    "Has 6 sides" 
    "   U     "
    " L F R B "
    "   D     "
    
    sides=list([1]*6)
    count=0
    def __init__(self):
        for i in range(6):
            self.sides[i]=Side("ulfrbd"[i])

    def __str__(self):
        text=" "*15+"-"*13+"\n"
        for i in range(2,-1,-1):
            #text+=(" "+""*3*(7-3*i)+"╔"+"═"*(20)+"|" + self.sides[0].color(self.sides[0].tiles[3*i]) + " " + self.sides[0].color(self.sides[0].tiles[3*i+1]) + " " + self.sides[0].color(self.sides[0].tiles[3*i+2]) +"|"+"═"*20+"╗"+ " "*4)
            text+=(" "*13+" | " + self.sides[0].color(self.sides[0].tiles[3*i]) + " " + self.sides[0].color(self.sides[0].tiles[3*i+1]) + " " + self.sides[0].color(self.sides[0].tiles[3*i+2])+" |\n")
        text+=" "+("-"*13+" ")*4+"\n"
        for i in range(2,-1,-1):
            for j in range(1,5):
                if j==1:
                    text+="| "
                text+=self.sides[j].color(self.sides[j].tiles[3*i])+" "+self.sides[j].color(self.sides[j].tiles[3*i+1])+" "+self.sides[j].color(self.sides[j].tiles[3*i+2])+" | "
            text+="\n"
        text+=" "+("-"*13+" ")*4+"\n"
        for i in range(2,-1,-1):
            text+=(" "*13+" | " + self.sides[5].color(self.sides[5].tiles[3*i]) + " " + self.sides[5].color(self.sides[5].tiles[3*i+1]) + " " + self.sides[5].color(self.sides[5].tiles[3*i+2]) + " |\n")
        text+=" "*15+"-"*13
        return text

    "Menu"
    def menu(self):
        action=1
        while(action>0):
            clear_output()
            print(self)
            try:
                action=int(input("What action would you like to do?\n1 - Scramble\n2 - Free Play\n3 - Solve Completely\n4 - Solve Partly\n0 - Exit\n\n\t\t\t"))
            except:
                print("Wrong input, try again!")
            if action==1:
                self.scramble()
            elif action==2:
                self.freePlay()
            elif action==3:
                self.solve()
                input("Press Enter to continue...")
            elif action==4:
                self.solve(int(input(f"How far do you want to solve?\n1 - Orient\n2 - Top Plus\n3 - Whole top Side\n4 - Flip\n5 - Second Layer\n6 - New Top Plus\n7 - Whole New Top\n8 - Final Corners\n9 - Completely\n\n\t\t\t")))
                action=3
                input("Press Enter to continue...")
            else:
                print("Good-Bye!")
                return
            #getch.getch("Press any key to continue")


    "Represantation methods"
    def ltoi(self,letter):
        "Returns the side index according to letter"
        dic={"u":0,"l":1,"f":2,"r":3,"b":4,"d":5}
        return dic[letter]

    def itol(self,sideNum):
        "Returns the side index according to letter"
        dic={0:"u",1:"l",2:"f",3:"r",4:"b",5:"d",6:"xy",7:"xz",8:"yz"}
        return dic[sideNum]

    def rightOf(self,sideName):
        return {"l":"f","f":"r","r":"b","b":"l"}[sideName]

    def leftOf(self,sideName):
        return {"l":"b","f":"l","r":"f","b":"r"}[sideName]

    def twin(self,NandI):
        "Returns twin (name,index)"
        return {("u",1):("f",7),("u",3):("l",7),("u",5):("r",7),("u",7):("b",7),
                ("l",1):("d",3),("l",3):("b",5),("l",5):("f",3),("l",7):("u",3),
                ("f",1):("d",7),("f",3):("l",5),("f",5):("r",3),("f",7):("u",1),
                ("r",1):("d",5),("r",3):("f",5),("r",5):("b",3),("r",7):("u",5),
                ("b",1):("d",1),("b",3):("r",5),("b",5):("l",3),("b",7):("u",7),
                ("d",1):("b",1),("d",3):("l",1),("d",5):("r",1),("d",7):("f",1)}[NandI]

    def corner(self,NandI):
        "Returns rest of corner ((rName,rIndex),(lName,lIndex))"
        corners=[(("u",0),("f",6),("l",8)),(("u",2),("r",6),("f",8)),(("u",6),("l",6),("b",8)),(("u",8),("b",6),("r",8)),
                (("d",0),("b",2),("l",0)),(("d",2),("r",2),("b",0)),(("d",6),("l",2),("f",0)),(("d",8),("f",2),("r",0))]
        for x in corners:
            if NandI in x:
                for i in range(3):
                    if x[i]==NandI:
                        return [x[(i+1)%3],x[(i+2)%3]]

    def find(self,partColors):
        "partColors=['color1',...]"
        "Returns [(sideName1,sideIndex1),...]"
        size=len(partColors)
        if size==7:
            size=1
            able=[4]
        elif size==2:
            able=[1,3,5,7]
        else:
            able=[0,2,6,8]
        for i in "ulfrbd":
            for j in able:
                if size==1:
                    if self.sides[self.ltoi(i)].tiles[j]==partColors:
                        return ((i,j))
                elif self.sides[self.ltoi(i)].tiles[j]==partColors[0]:
                    if size==1:
                        return ((i,j))
                    elif size==2:
                        if self.sides[self.ltoi(self.twin((i,j))[0])].tiles[self.twin((i,j))[1]]==partColors[1]:
                            return [(i,j),self.twin((i,j))]
                    else:
                        if self.sides[self.ltoi(self.corner((i,j))[0][0])].tiles[self.corner((i,j))[0][1]]==partColors[1] and self.sides[self.ltoi(self.corner((i,j))[1][0])].tiles[self.corner((i,j))[1][1]]==partColors[2]:
                            return [(i,j),self.corner((i,j))[0],self.corner((i,j))[1]]

    "Rotation methods"
    def rotate(self,sideName,rTimes=1):
        "Rotates the relevant side rTimes times clockwise, and swaps surrounding side's closest tiles"
        "Input: 'u',2 for rotating upper side twice clockwise"
        if (rTimes%4>0):
            if rTimes%4==3:
                self.count-=2
            print(sideName)
            if len(sideName)!=2:
                self.sides[self.ltoi(sideName)].rotate()
            self.swapTriplets(sideName)
            self.rotate(sideName,rTimes-1)
            self.count+=1

    def swapTriplets(self,refSideName):
        "Swaps triplets on surrounding sides / middles clockwise"
        surSides,surTiles=self.sidesToSwap(refSideName)
        temp=[1]*3
        surSides.reverse()
        surTiles.reverse()
        for i in range(-1,4):
            for j in range(3):
                if i==-1:
                    temp[j]=self.sides[self.ltoi(surSides[0])].tiles[surTiles[0][j]]
                elif i<3:
                    self.sides[self.ltoi(surSides[i])].tiles[surTiles[i][j]]=self.sides[self.ltoi(surSides[i+1])].tiles[surTiles[i+1][j]]
                else:
                    self.sides[self.ltoi(surSides[i])].tiles[surTiles[i][j]]=temp[j]

    def sidesToSwap(self,let):
        "Returns [Relevant side's names in the clockwise order tuple,respectively ordered tiles tuples]"
        "dic(let)[0][i] side's dic(let)[1][i] tuple will be replaced"
        dic={            
            "u":[["l","b","r","f"],[[6,7,8],[6,7,8],[6,7,8],[6,7,8]]],
            "l":[["u","f","d","b"],[[0,3,6],[0,3,6],[0,3,6],[8,5,2]]],
            "f":[["u","r","d","l"],[[0,1,2],[6,3,0],[8,7,6],[2,5,8]]],
            "r":[["u","b","d","f"],[[2,5,8],[6,3,0],[2,5,8],[2,5,8]]],
            "b":[["u","l","d","r"],[[6,7,8],[0,3,6],[2,1,0],[8,5,2]]],
            "d":[["l","f","r","b"],[[0,1,2],[0,1,2],[0,1,2],[0,1,2]]],
            "xy":[["l","f","r","b"],[[3,4,5],[3,4,5],[3,4,5],[3,4,5]]],
            "xz":[["u","r","d","l"],[[3,4,5],[7,4,1],[5,4,3],[1,4,7]]],
            "yz":[["b","d","f","u"],[[7,4,1],[1,4,7],[1,4,7],[1,4,7]]]}
        return dic[let]

    "Scramble"
    def scramble(self):
        print(" "*11+"Scrambling!")
        numOfActions=random.randint(10,20)
        sidesArray=numpy.random.randint(0, 8, numOfActions)
        rotationsArray=numpy.random.randint(1, 3, numOfActions)
        for i in range(numOfActions):
            self.rotate(self.itol(sidesArray[i]),rotationsArray[i])
        print(self)

    def freePlay(self):
        action="f"
        while action!="0":
            action=input("Enter action: u / l / f / r / b / d / xy / xz / yz followed by ' for counterclockwise\n0 - Exit Free Play\n\n\t\t\t")
            if action[-1]=="'":
                self.rotate(action[:-1],-1)
            elif action in ["u","l","f","r","b","d","xy","xz","yz"]:
                self.rotate(action,1)
            clear_output()
            print(self)

    "Solve"
    def solve(self,flag=9):
        self.count=0
        print("\t\t\tBegining SOLUTION!")
        self.orient()
        print("\t\t\tOriented!\n",self)
        if flag>1:
            self.greyPlus()
            print("\t\t\tGrey Plussed!\n",self)
        if flag>2:
            self.greyCorners()
            print("\t\t\tGrey Cornered!\n\t\t\tTop - Complete!\n",self)
        if flag>3:
            self.flip()
            print("\t\t\tFlipped!\n",self)
        if flag>4:
            self.secLayer()
            print("\t\t\tSecond Layer - Complete!\n",self)
        if flag>5:
            self.newUpPlus()
            print("\t\t\tNew Top Plussed!\n",self)
        if flag>6:
            self.newUpCorners()
            print("\t\t\tNew Top Cornered!\n\t\t\tNew Top Complete!\n",self)
        if flag>7:
            self.finalCorners()
            print("\t\t\tFinal Cornered!\n",self)
        if flag>8:
            self.finalCenters()
            print("\t\t\tFinal Centered!")
            print("\t\t\tSolution COMPLETE!\n",self)
        print("\t\t\tSolved in "+str(self.count)+" rotations!")

    "Orient Cube"
    def orient(self):
        pointer=self.find(self.sides[0].rightColor())
        if self.find(self.sides[0].rightColor())[0][0]!=self.sides[0].name:
            self.rotate({"l":"xz","r":"xz","d":"xz","f":"yz","b":"yz"}[pointer[0][0]],{"l":1,"r":-1,"d":2,"f":1,"b":-1}[pointer[0][0]])
        pointer=self.find(self.sides[1].rightColor())
        if pointer[0][0]!=self.sides[1].name:
            self.rotate("xy",{"f":3,"r":2,"b":1}[pointer[0][0]])

    "UP side methods"
    def greyPlus(self):
        for i in [1,3,5,7]:
            twinside={1:2,3:1,5:3,7:4}[i]
            destination=[(self.sides[0].name,i),(self.twin((self.sides[0].name,i)))]
            pointer=self.find([self.sides[0].rightColor(),self.sides[twinside].rightColor()])
            if pointer!=destination:
                #Step I - bring the Grey tile of the pointer to the respective of d side
                #not from bottom parts or (upper switched)
                if pointer[1][0] in "lfrb".replace(destination[1][0],""):
                    self.rotate(pointer[1][0],{7:2,5:1,3:-1,1:0}[pointer[1][1]])
                #from bottom parts that need switching
                elif pointer[1][0]=="d":
                    self.rotate(pointer[0][0],-1)
                    self.rotate({"l":"f","f":"r","r":"b","b":"l"}[pointer[0][0]],-1)
                    self.rotate("d",-1)
                    self.rotate({"l":"f","f":"r","r":"b","b":"l"}[pointer[0][0]],1)
                #from upper and switched
                elif pointer[1][0]=="u":
                    self.rotate(pointer[0][0],1)
                    self.rotate({"l":"f","f":"r","r":"b","b":"l"}[pointer[0][0]],-1)
                    self.rotate("d",-1)
                    self.rotate({"l":"f","f":"r","r":"b","b":"l"}[pointer[0][0]],1)
                #Step II - move to mirror below destination
                #if we switched
                if pointer[1][0] in"ud":
                    self.rotate("d",self.ltoi(destination[1][0])-self.ltoi(pointer[0][0]))
                #if we didnt switch
                else:
                    self.rotate("d",self.ltoi(destination[1][0])-self.ltoi(pointer[1][0]))
                #Step III - fix possible derails
                # if rightgrey was in a 3 \ 5 index and in "lfrb" and didnt end up underneath distination:
                if (pointer[1][0] in "lfrb") and (pointer[1][0]!=destination[1][0]) and (pointer[1][1] in [3,5]):
                    self.rotate(pointer[1][0],{5:-1,3:1}[pointer[1][1]])
                # if rightgrey in 1 index of a "lfrb"
                elif (pointer[0][1]==1) and (pointer[0][0] in "lfrb".replace(destination[1][0],"")):
                    self.rotate(pointer[0][0],1)
                #Step IV - rotate to destination
                if pointer[1] not in [(destination[1][0],3),(destination[1][0],5)]:
                    self.rotate(destination[1][0],2)
                elif pointer[1]==(destination[1][0],3):
                    self.rotate(destination[1][0],1)
                elif pointer[1]==(destination[1][0],5):
                    self.rotate(destination[1][0],-1)

    def greyCorners(self):
        for i in [0,2,6,8]:
            neighbor={0:(2,1),2:(3,2),6:(1,4),8:(4,3)}[i]
            destination=[(self.sides[0].name,i),(self.sides[neighbor[0]].name,6),(self.sides[neighbor[1]].name,8)]
            pointer=self.find([self.sides[0].rightColor(),self.sides[neighbor[0]].rightColor(),self.sides[neighbor[1]].rightColor()])        
            if pointer!=destination:
                j=i
                #Step I - lower the part
                for tile in pointer:
                    if tile[0]=="u":
                        j=tile[1]
                        ourSide={0:"f",2:"r",6:"l",8:"b"}[j]
                        self.rotate(ourSide,-1)
                        self.rotate("d",-1)
                        self.rotate(ourSide,1)
                        self.rotate("d",1)
                    elif tile[0]=="d":
                        j={0:6,2:8,6:0,8:2}[tile[1]]

                #Step II - move below
                if (j-i)%4==0 and j!=i:
                    self.rotate("d",2)
                elif (i,j) in [(0,2),(2,8),(8,6),(6,0)]:
                    self.rotate("d",-1)
                elif (j,i) in [(0,2),(2,8),(8,6),(6,0)]:
                    self.rotate("d",1)

                #step III - switch until in place
                ourSide={0:"f",2:"r",6:"l",8:"b"}[i]
                while [self.sides[0].tiles[i],self.sides[self.ltoi(ourSide)].tiles[6]]!=[self.sides[0].rightColor(),self.sides[self.ltoi(ourSide)].rightColor()]:
                    self.rotate(ourSide,-1)
                    self.rotate("d",-1)
                    self.rotate(ourSide,1)
                    self.rotate("d",1)

    "Flipping for user"    
    def flip(self):
        self.rotate("r",2)
        self.rotate("yz",2)
        self.rotate("l",2)

    "Second layer methods"
    def secLayer(self):
        #newOrient={1:1,2:4,3:3,4:2}
        for i in "frbl":
            pointer=self.find([self.sides[self.ltoi(i)].tiles[4],self.sides[self.ltoi(self.rightOf(i))].tiles[4]])
            destination=[(i,5),(self.rightOf(i),3)]
            if pointer!=destination:
                #Step I - if in bad secondlayer or on top
                if (pointer[0][1]==3) and (pointer[0][0]!="u"):
                    self.simpleSecLayerR(pointer[1][0])
                    self.rotate("u",self.ltoi(pointer[0][0])-self.ltoi(i)+1)
                elif (pointer[0][1]==5) and (pointer[0][0]!="u"):
                    self.simpleSecLayerL(pointer[1][0])
                    self.rotate("u",self.ltoi(pointer[0][0])-self.ltoi(i)-1)
                elif (pointer[0][1]==7) and (pointer[0][0]!="u"):
                    self.rotate("u",self.ltoi(pointer[0][0])-self.ltoi(i))
                #Step II.0 - i7,twin <-> i5,twin
                if pointer[0][0]!="u":
                    self.simpleSecLayerR(i)
                #StepII.1 - need to switch from his right because the correct i5 was facing up
                else:
                    self.rotate("u",self.ltoi(pointer[1][0])-self.ltoi(i)-1)
                    self.simpleSecLayerL(self.rightOf(i))

    def simpleSecLayerR(self,sideName):
        "replaces current5,twin <-> current7,twin"
        self.rotate("u",1)
        self.rotate(self.rightOf(sideName),1)
        self.rotate("u",-1)
        self.rotate(self.rightOf(sideName),-1)
        self.rotate("u",-1)
        self.rotate(sideName,-1)
        self.rotate("u",1)
        self.rotate(sideName,1)

    def simpleSecLayerL(self,sideName):
        "replaces current3,twin <-> current7,twin"
        self.rotate("u",-1)
        self.rotate(self.leftOf(sideName),-1)
        self.rotate("u",1)
        self.rotate(self.leftOf(sideName),1)
        self.rotate("u",1)
        self.rotate(sideName,1)
        self.rotate("u",-1)
        self.rotate(sideName,-1)

    "New UP side methods"
    def newUpPlus(self,count=0):
        #Recursive method for turning the new up side into +
        if count==0:
            for x in [1,3,5,7]:
                if self.sides[0].tiles[x]==self.sides[5].rightColor():
                    count+=1
        if count==4:
            return
        #we want arrow to bottom right or horizontal line
        if ((count==2) and (((self.sides[0].tiles[1]==self.sides[0].tiles[3])or(self.sides[0].tiles[5]==self.sides[0].tiles[7])) or ((self.sides[0].tiles[1]==self.sides[5].rightColor())and(self.sides[0].tiles[7]==self.sides[5].rightColor())))):
            self.rotate("u",1)
            print("rotated u")
        #execute algoryhm
        self.rotate("f",1)
        self.rotate("r",1)
        self.rotate("u",1)
        self.rotate("r",-1)
        self.rotate("u",-1)
        self.rotate("f",-1)
        if self.sides[0].tiles[1]==self.sides[0].tiles[3]:
            self.newUpPlus(count+2)
        else:
            self.newUpPlus(count)

    def newUpCorners(self):
        #Recursive method for turning the new up side into +
        count=0
        for x in [0,2,6,8]:
            if self.sides[0].tiles[x]==self.sides[5].rightColor():
                count+=1
        #we want a fish pointing to bottom left
        if count==1:
            while self.sides[0].tiles[0]!=self.sides[5].rightColor():
                self.rotate("u",1)
        #enable proceeding
        elif count==2:
            if (self.sides[0].tiles[0]==self.sides[0].tiles[8]) and (self.sides[0].tiles[0]!=self.sides[5].rightColor()):
                    self.rotate("u",1)
            else:
                while (self.sides[0].tiles[0]!=self.sides[5].rightColor()) and (self.sides[0].tiles[2]!=self.sides[5].rightColor()):
                    self.rotate("u",1)
        elif count==4:
            return
        #execute algorythm
        self.rotate("r",1)
        self.rotate("u",1)
        self.rotate("r",-1)
        self.rotate("u",1)
        self.rotate("r",1)
        self.rotate("u",2)
        self.rotate("r",-1)
        self.newUpCorners()

    def finalCorners(self):
        #Recursive method for aranging final corners
        count=0
        correct=[]
        newFrontSide="f"
        for i in "lfrb":
            if self.sides[self.ltoi(i)].tiles[6]==self.sides[self.ltoi({"l":"l","f":"b","r":"r","b":"f"}[i])].rightColor():
                count+=1
                correct.append(i)
        if count==4:
            return
        #we want correct in back left
        if count==1:
            newFrontSide=self.rightOf(correct[0])
        #we want both correct to the back
        elif count==2:
            if correct[0]==self.leftOf(correct[1]):
                newFrontSide=self.leftOf(correct[0])
            elif correct[1]==self.leftOf(correct[0]):
                newFrontSide=self.leftOf(correct[1])
            elif "l" in correct:
                newFrontSide="l"
        #execute algorythm
        self.rotate(newFrontSide,-1)
        self.rotate(self.leftOf(newFrontSide),1)
        self.rotate(newFrontSide,-1)
        self.rotate(self.rightOf(newFrontSide),2)
        self.rotate(newFrontSide,1)
        self.rotate(self.leftOf(newFrontSide),-1)
        self.rotate(newFrontSide,-1)
        self.rotate(self.rightOf(newFrontSide),2)
        self.rotate(newFrontSide,2)
        if count==2:
            self.rotate("u",-1)
        self.finalCorners()

    def finalCenters(self):
        #Recursive method for aranging final centers
        count=0
        correct=[]
        newFrontSide="f"
        for i in "lfrb":
            if self.sides[self.ltoi(i)].tiles[7]==self.sides[self.ltoi({"l":"l","f":"b","r":"r","b":"f"}[i])].rightColor():
                count+=1
                correct.append(i)
        if count==4:
            return
        #we want correct in left
        if count==1:
            newFrontSide=self.rightOf(correct[0])
        #execute algorythm
        self.rotate(self.rightOf(newFrontSide),2)
        self.rotate("u",1)
        self.rotate(newFrontSide,1)
        self.rotate(self.rightOf(self.rightOf(newFrontSide)),-1)
        self.rotate(self.rightOf(newFrontSide),2)
        self.rotate(newFrontSide,-1)
        self.rotate(self.rightOf(self.rightOf(newFrontSide)),1)
        self.rotate("u",1)
        self.rotate(self.rightOf(newFrontSide),2)
        self.finalCenters()

class Side:
    "6 7 8"
    "3 4 5"
    "0 1 2"

    def __init__(self,sideName):
        "Input: u for upper side"
        self.name=sideName
        self.tiles=list([self.rightColor()]*9)

    def __str__(self):
        text=""
        for i in range(2,-1,-1):
            text+=("\t\t\t|" + self.tiles[3*i] + "\t" + self.tiles[3*i+1] + "\t" + self.tiles[3*i+2] + "\t|\n")
        return text

    def rotate(self):
        "Rotates the Side clockwise once"
        self.tiles=list([self.tiles[2],self.tiles[5],self.tiles[8],self.tiles[1],self.tiles[4],self.tiles[7],self.tiles[0],self.tiles[3],self.tiles[6]])

    def color(self,colorstr="Grey  "):
        return {"Black  ":'\x1b[37;40m',
                "Red    ":'\x1b[41m',
                "Green  ":'\x1b[42m',
                "Orange ":'\x1b[43m',
                "Blue   ":'\x1b[44m',
                "Grey   ":'\x1b[47m',}[colorstr]+"   "+'\x1b[0m'

    def rightColor(self):
        relate={
            "u":"Grey   ",
            "l":"Green  ",
            "f":"Red    ",
            "r":"Blue   ",
            "b":"Orange ",
            "d":"Black  "}
        return relate[self.name]
    
#Main
Rubik=Cube()
Rubik.menu()


# In[ ]:





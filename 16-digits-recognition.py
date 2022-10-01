import numpy as np
import pygame, sys
from pygame.locals import *
import math
import random

pygame.init()
pygame.display.init()
surface=pygame.display.set_mode((1000,600),0,32)

digits=[0,1,2,3,4,5,6,7,8,9]
pic=[[],[],[],[],[],[],[],[],[],[]]
pic[0]=np.array([[0,1,1,1,0],[1,0,0,0,1],[1,1,0,0,1],[1,0,1,0,1],[1,0,0,1,1],[1,0,0,0,1],[0,1,1,1,0]], dtype=float)
pic[1]=np.array([[0,0,1,0,0],[0,1,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1]], dtype=float)
pic[2]=np.array([[1,1,1,1,1],[1,0,0,0,1],[0,0,0,0,1],[1,1,1,1,1],[1,0,0,0,0],[1,0,0,0,1],[1,1,1,1,1]], dtype=float)            
pic[3]=np.array([[0,1,1,1,0],[1,0,0,0,1],[0,0,0,0,1],[0,1,1,1,0],[0,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]], dtype=float)   
pic[4]=np.array([[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1],[0,0,0,0,1],[0,0,0,0,1],[0,0,0,0,1]], dtype=float)     
pic[5]=np.array([[1,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1],[0,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1]], dtype=float)             
pic[6]=np.array([[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,0],[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1]], dtype=float)    
pic[7]=np.array([[1,1,1,1,1],[0,0,0,0,1],[0,0,0,0,1],[0,0,0,1,0],[0,0,1,0,0],[0,1,0,0,0],[1,0,0,0,0]], dtype=float)                          
pic[8]=np.array([[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]], dtype=float)     
pic[9]=np.array([[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1],[0,0,0,0,1],[0,0,0,0,1],[0,0,0,0,1]], dtype=float)                                                    

error=np.array([[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1]])

testX=250
testY=230
x_corr=650
y_corr=230

WHITE=(255,255,255)
RED = (255,0,0)
YELLOW=(255,255,0)
BLACK=(0,0,0)
surface.fill(BLACK)

font=pygame.font.Font('freesansbold.ttf', 16) 
pygame.display.flip()
MAX_EPOCH=1000
MIN_ERR=0.001 
lr=0.3
trials=0
np.set_printoptions(precision=2)


def drawDig(arr, col1, col2):
    for j in range(7):
        for k in range(5):
            sq=[(x_corr+k*20,y_corr+j*20),(x_corr+k*20,y_corr+20+j*20),(x_corr+20+k*20,y_corr+20+j*20),(x_corr+20+k*20,y_corr+j*20)]
            if arr[j][k]==1:
                pygame.draw.polygon(surface, col1, sq)
            else:
                pygame.draw.polygon(surface, col2, sq)   
                
def drawTest(arr, col1, col2):
    for j in range(7):
        for k in range(5):
            sq=[(testX+k*20,testY+j*20),(testX+k*20,testY+20+j*20),(testX+20+k*20,testY+20+
            j*20),(testX+20+k*20,testY+j*20)]
            if arr[j][k]==1:
                pygame.draw.polygon(surface, col1, sq)
            else:
                pygame.draw.polygon(surface, col2, sq)
                
def drawRand(col1,col2):
    for j in range(7):
        for k in range(5):
            sq=[(testX+k*20,testY+j*20),(testX+k*20,testY+20+j*20),(testX+20+k*20,testY+20+
            j*20),(testX+20+k*20,testY+j*20)]
            a=(int)(random.random()*10)
            if a>6:
                pygame.draw.polygon(surface, col1, sq)
            else:
                pygame.draw.polygon(surface, col2, sq)
                
def cells():
    for j in range(y_corr,y_corr+160,20):
        pygame.draw.line(surface, WHITE, (x_corr,j), (x_corr+100,j), 1)
        
    for j in range(x_corr,x_corr+120,20):
        pygame.draw.line(surface, WHITE, (j,y_corr), (j,y_corr+140), 1)
        
    for j in range(testY,testY+160,20):
        pygame.draw.line(surface, WHITE, (testX,j), (testX+100,j), 1)
        
    for j in range(testX,testX+120,20):
        pygame.draw.line(surface, WHITE, (j,testY), (j,testY+140), 1)    

class sample:
    def __init__(self, num):
        self.num=num
        self.images=[pic[num]]
        self.arr=pic[num]
        cells()
        self.items=[]
        self.weights=[]
        for j in range(10):
            self.weights.append(2*np.random.rand(35,)-np.ones(35, dtype=float))
        
    def gl_r1(self):
        self.arr=self.images[0]
        tmp=self.arr.copy()
        drawTest(self.arr,RED,BLACK)
        for k in range(7):
            for j in range(5):
                flip=(int)(random.random()*10)
                change=random.random()*0.6
                fac=255*change
                B=(0+fac, 0+fac, 0+fac)
                W=(255-fac, 255-fac, 255-fac)
                sq=[(testX+j*20,testY+k*20),(testX+j*20,testY+20+k*20),(testX+20+j*20,testY+20+k*20),(testX+20+j*20,testY+k*20)]
                if flip==2:
                    if self.arr[k][j]==1:
                        pygame.draw.polygon(surface, B, sq)
                        tmp[k][j]=change
                    else:
                        pygame.draw.polygon(surface, W, sq)    
                        tmp[k][j]=1-change
                else:
                    if self.arr[k][j]==1:
                        pygame.draw.polygon(surface, RED, sq)
                    else:
                        pygame.draw.polygon(surface, BLACK, sq) 
        cells()
        self.images.append(tmp)
        
    def gl_rAll(self):
        for j in range(29):
            self.gl_r1()
            pygame.display.flip()
            cells()
        
        for img in self.images:
            self.items.append(np.reshape(img, (35,)))

class Perceptron:
    def __init__(self,num):
        self.number=num
        self.thres=0
        self.expected=np.zeros(10)
        self.expected[num]=1
        self.err=0
        
    def train(self,samp):
        for j in range(30):
            target=self.expected[samp.num]
            output=self.FwdOut(samp.items[j],np.squeeze(samp.weights[self.number]))
            diff=target-output
            self.err=self.err+abs(diff)
            samp.weights[self.number]=samp.weights[self.number]+lr*diff*samp.items[j]
            self.thres=self.thres-lr*diff

    def FwdOut(self,samples,weight):
        if samples.dot(weight)-self.thres>0:
            return 1
        return 0
       
              
class recognize:
    def __init__(self):
        self.digits=[]  
        self.perceptrons=[]                
        for j in range(10):
            self.digits.append(sample(j))
            self.perceptrons.append(Perceptron(j))    

    def gl_r(self):
        for dig in self.digits:
            dig.gl_rAll()
            cells()
            pygame.display.flip()
            pygame.time.Clock().tick(60)
            
    def training(self):
        for Perceptron_num in range(10):
            trials=0
            absErr=1000
            while absErr>MIN_ERR and trials<=MAX_EPOCH:
                absErr=0
                self.perceptrons[Perceptron_num].err=0
                for Sample_Digit in range(10):
                    self.perceptrons[Perceptron_num].train(self.digits[Sample_Digit])
                    absErr=self.perceptrons[Perceptron_num].err
                print("Perceptron Number: ", Perceptron_num)
                print("Trial Number: ",trials)
                print("Error: ",absErr)
                print()
                trials=trials+1         
        
                
    def test(self):
        for d in range(10):
            for s in range(10):
                print(self.perceptrons[d].FwdOut(self.digits[s].items[3],self.digits[s].weights[d]), end=" ")
            print()
        print()

topButtons=[]
topCommands=["Generate", "Train", "Recognize", "Noise", "Clear"]

def classify(arr, t):
    if t==-1:
        drawDig(error,YELLOW,BLACK)
        cells()
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        print("Resulting number: error")
    else:
        cells()
        temp=np.reshape(arr,(35,))
        for per in r.perceptrons:
            if per.FwdOut(temp,r.digits[t].weights[per.number])==1:
                drawDig(pic[per.number], YELLOW, BLACK)
                cells()
                pygame.display.flip()
                pygame.time.Clock().tick(60)
                print("Resulting number:",per.number)

def setTop():
    for j in range(5):
        text = font.render(topCommands[j], True, WHITE, BLACK) 
        textRect = text.get_rect()
        textRect.center = (240+130*j, 550) 
        surface.blit(text, textRect)
        topButtons.append(textRect)
        
bottomButtons=[]
newfont=pygame.font.Font('freesansbold.ttf', 32) 

def setBottom():    
    for j in range(11):
        if j==10:
            text = newfont.render("r",True,WHITE,BLACK)
        else:
            text = newfont.render(str(j), True, WHITE, BLACK) 
        textRect = text.get_rect()
        textRect.center = (230+60*j, 50) 
        surface.blit(text, textRect)
        bottomButtons.append(textRect)
        
        
def setup(): 
    setTop()
    setBottom()
    cells()

def addN(test):
        tmp=test.copy()
        drawTest(tmp,RED,BLACK)
        for k in range(7):
            for j in range(5):
                flip=(int)(random.random()*6)
                change=random.random()*0.6
                fac=255*change
                B=(0+fac, 0+fac, 0+fac)
                W=(255-fac, 255-fac, 255-fac)
                sq=[(testX+j*20,testY+k*20),(testX+j*20,testY+20+k*20),(testX+20+j*20,testY+20+k*20),(testX+20+j*20,testY+k*20)]
                if flip==2:
                    if test[k,j]==1.0:
                        pygame.draw.polygon(surface, B, sq)
                        tmp[k,j]=change
                    else:
                        pygame.draw.polygon(surface, W, sq)    
                        tmp[k,j]=1-change
                else:
                    if test[k,j]==1:
                        pygame.draw.polygon(surface, RED, sq)
                    else:
                        pygame.draw.polygon(surface, BLACK, sq) 
        cells()
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        return tmp
    
r=recognize()
setup()
pygame.display.flip()
tmp=[]
void=np.zeros((7,5))

def clear():
    drawTest(void, RED, BLACK)
    drawDig(void, YELLOW, BLACK)
    cells()
    pygame.display.flip()
    setup()
            
numTest=0

while True:
    pos = pygame.mouse.get_pos()
    pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
    for j in range(5):
        if topButtons[j].collidepoint(pos) and pressed1:
            if j==0:
                r.gl_r()
            elif j==1:
                r.training()
            elif j==2:
                classify(tmp,numTest)                
            elif j==3:
                addN(tmp)
            elif j==4:
                clear()
                
    for j in range(11):
        if bottomButtons[j].collidepoint(pos) and pressed1:
            clear()
            if j==10:
                drawRand(RED,BLACK)
                tmp=error.copy()
                numTest=-1
            else: 
                drawTest(pic[j],RED,BLACK)
                tmp=pic[j].copy()
                numTest=j
            cells()
            pygame.display.flip()
            pygame.time.Clock().tick(60)
                   
    for event in pygame.event.get():        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        
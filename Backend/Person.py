from Bullet import Bullet
class Person():
    def __init__(self):
        self.socket=None
        self.x=0
        self.y=0
        self.r=0
        self.d=0
        self.bullets=[]
        
    def setSocket(self,socket):
        self.socket=socket

    def getSocket(self):
        return self.socket

    def move(self):
        self.x+=1
        self.y+=1
        self.r+=1

    def shoot(self):
        bullet=Bullet()
        self.bullets.append(bullet)

    def getData(self):
        return {"x":self.x,"y":self.y,"r":self.r,"d":self.d,"bullets":[bullet.getData() for bullet in self.bullets]}

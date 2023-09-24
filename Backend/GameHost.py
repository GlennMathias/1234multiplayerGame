import asyncio
from random import random
import uuid
import websockets
import json
import threading


from Person import Person
from FlagPost import FlagPost
from Flag import Flag

websocket_g=None

global test_socket
test_socket=None

# Group class and group manager class

    
class Group():
    def __init__(self):
        self.players=[]
        self.socket=None
        self.flagPosts=[]
        self.flags=[]
        self.id=0

    def addPlayer(self,player):
        print("added Player")
        self.players.append(player)
        print(self.players)
    
    def getId(self):
        return str(self.id)

    def setId(self,id):
        self.id=id

    def addFlagPost(self,flagpost):
        self.flagPosts.append(flagpost)

    def addFlag(self,flag):
        self.flags.append(flag)

    def setSocket(self,socket):
        self.socket=socket

    def getSocket(self):
        return self.socket

    async def sendData(self):
        for player in self.players:
            if (player.getSocket() != None):
                
                data={"group":{"players":[player.getData() for player in self.players],
                        "flags":[flag.getData() for flag in self.flags],
                        "flagPosts":[flagPost.getData() for flagPost in self.flagPosts],
                        "objects":[]
                        }
              }
                await(player.getSocket().send(json.dumps(data)))

class PlayGround():
    def __init__(self):
        pass

class GroupManagementSystem():
    def __init__(self):
        self.groups=[]
        self.socket=None

    def __getId__(self):
        gid=uuid.uuid4()
        print(str(gid))
        return gid

    def addGroup(self,group):
        group.setId(self.__getId__())
        self.groups.append(group)
        return group.getId()

    def getGroup(self,id):
        for group in self.groups:
            if group.getId()==id:
                return group

    async def sendData(self):
        while True:
            for group in self.groups:
                await(group.sendData())
                

# group and gm init



gms=GroupManagementSystem()


def dataMiddleware():
    loop=asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(gms.sendData())
    loop.close()

def actionMiddleware():
    loop=asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(gms.move())
    loop.close()
t1=threading.Thread(target=dataMiddleware)
t1.start()

#t2=threading.Thread(target=actionMiddleware)
#t2.start()


async def server(websocket,path):
    print("server started")
    global test_socket
    global websocket_g
    async for message in websocket:
        parsed_message=json.loads(message)
        print(parsed_message)
        if parsed_message['request']!= "":
            if parsed_message['request']['action']=="createGroup":
                print(parsed_message['user_details'])
                group=Group()
                player=Person()
                player.setSocket(websocket)
                group.addPlayer(player)
                groupId=gms.addGroup(group)
                await(websocket.send(json.dumps({"systemData":{"result":"success","groupId":groupId}})))
            if parsed_message['request']['action']=="joinGroup":
                print(parsed_message['user_details']['groupId'])
                group_id=parsed_message['user_details']['groupId']
                group= gms.getGroup(group_id)
                player=Person()
                player.setSocket(websocket)
                group.addPlayer(player)
                await(websocket.send(json.dumps({"systemData":{"result":"success"}})))


start_server = websockets.serve(server,"localhost",5500)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


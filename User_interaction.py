import threading as th

class User_interaction (th.Thread):

    def __init__(self, peer):
        th.Thread.__init__(self)
        self.peer = peer

    def run(self):
    	while True :
    		command = input("command #!> ")
    		if command == "msg":
    			self.peer.sendMsg()
    		elif command == "addData" :
    			self.peer.dataCheck()
    			

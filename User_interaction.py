import threading as th

class User_interaction (threading.Thread):

    def __init__(self, peer):
        threading.Thread.__init__(self)
        self.peer = peer

    def run(self):
        while True :
			command = input("command #!> ")

			if command == "msg":
				self.peer.sendMsg()

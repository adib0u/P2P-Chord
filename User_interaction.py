import threading as th

class User_interaction (th.Thread):

	def __init__(self, peer):
		th.Thread.__init__(self)
		self.peer = peer

	def run(self):
		print("\u001B[32m" + "=== Commandes dispo : msg | addData | getData" + "\u001B[0m")
		while True :
			command = input()
			if command == "msg":
				self.peer.sendMsg()
			elif command == "addData" :
				self.peer.dataCheck()
			elif command == "getData" :
				self.peer.getData()
				

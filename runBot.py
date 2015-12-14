#!/usr/bin/python3
import time, threading

restart = True
while restart:
	exec(compile(open("IRC.py").read(), "IRC.py", "exec"), globals(), locals())
	server = IRCServer("config.json", "omnimaga")
	server.start()
	while server.is_alive():
		time.sleep(2)
	if server.restart:# and not self.end and not self.allowRestart or self.restartOnExc:
		restart = True
		del server
		print("restart in 2 seconds")
		time.sleep(2)
		print("restarting now...")
	else:
		restart = False
		print("exiting...")
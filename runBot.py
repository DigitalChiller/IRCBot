#!/usr/bin/python3
import time, threading, sys, traceback
import Echo

if len(sys.argv) >= 2:
	name = sys.argv[1]

if len(sys.argv) >= 3:
	joinChansOnStart = str(sys.argv[2]).lower() == "true"
else:
	joinChansOnStart = True

restart = True
while restart:
	try:
		exec(compile(open("IRC.py").read(), "IRC.py", "exec"), globals(), locals())
		server = IRCBot(name, joinChansOnStart)
		server.start()

		while server.is_alive():
			time.sleep(1)

		restart = server._restart
		joinChansOnStart = server.joinChansOnStart

		del server
	except Exception as e:
		Echo.end()
		print(traceback.format_exc())

	if restart:# and not self.end and not self.allowRestart or self.restartOnExc:
		print("restart in 2 seconds")
		time.sleep(2)
		print("restarting now...")
	else:
		restart = False
		print("exiting...")
		break

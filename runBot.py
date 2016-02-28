#!/usr/bin/python3

## LICENSE
#    This file is part of nBot.
#
#    nBot is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nBot is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with nBot.  If not, see <http://www.gnu.org/licenses/>.
#

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
		server.join()
		restart = server._restart
		del server

	except Exception as e:
		Echo.end()
		print(traceback.format_exc())

	if restart:
		print("restart in 2 seconds")
		time.sleep(2)
		print("restarting now...")
	else:
		restart = False
		print("exiting...")
		break

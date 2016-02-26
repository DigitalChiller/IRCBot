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


## variables
# msg = message dict
# args = list of args
# nickHgl = is bot addressed? (bot: <message>)
# target = channel or private chat
# fromOwner = author is owner
# 
## functions
# self.feedback(msg)
#  use this to send something back
# self.botdo(action, *args, **kwargs)
#  use this to tell the bot to do something

if nickHgl and msg["cmdPref"] == ",":
	if fromOwner or auth(uperms, plName, msg["cmd"]):
		if msg["cmd"] == "help":
			if len(args) == 0:
				self.feedback("Hello, I'm nBot!")
				self.feedback("valid help arguments are:")
				self.feedback("'bot' for detailed information about me")
				self.feedback("'cmd <command>' for information about a command")
				self.feedback("'pl <plugin>' for information about a plugin")
				self.feedback("here is a list of commands:")
				self.feedback("*totally legit list*") #self.usercmd
			elif len(args) == 1:
				if msg["args"] == "bot":
					self.feedback("[insert information here]")
				else:
					self.handleError("syntax")
			else:
				if args[0] == "cmd":
					if len(args) > 3:
						self.handleError("syntax")
					else:
						if len(args) == 2:
							plugin = None
						elif len(args) == 3:
							plugin = args[2]
						
						sendSyntax(self, args[1], plugin)

				elif args[0] == "pl":
					self.feedback("pl info")
				else:
					self.handleError("syntax")


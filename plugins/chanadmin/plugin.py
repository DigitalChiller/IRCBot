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

if nickHgl and not fromOwner and not auth(uperms, plName, msg["cmd"]):
	caperms = self.permM.getPermsOfGroup("#chanadmin")

	if auth(caperms, plName, msg["cmd"]):
		if msg["cmd"] == "join":
			if len(args) == 0:
				self.handleError("syntax")
			elif len(args) == 1:
				if isAdminOfChan(msg["nick"], msg["args"], bot, line):
					bot.join(msg["args"])
					self.feedback("success")
			else:
				self.handleError("syntax")

		elif msg["cmd"] == "part":
			if len(args) > 1:
				self.handleError("syntax")
			else:
				if len(args) == 0:
					chan = target
				else:
					chan = msg["args"]
				if isAdminOfChan(msg["nick"], chan, bot, line):
					bot.part(chan)
					self.feedback("success")


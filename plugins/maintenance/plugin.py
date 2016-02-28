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

if nickHgl:
	if fromOwner or auth(uperms, plName, msg["cmd"]):
		if msg["cmd"] == "restartBot":
			if len(args) == 0:
				self.feedback("bye, restarting")
				bot.shutdown("restart", "bye, restarting now", 1, 1)
			else:
				self.handleError("syntax")

		elif msg["cmd"] == "reconnectBot":
			if len(args) == 0:
				self.feedback("bye, reconnecting now")
				bot.shutdown("reconnect", "bye, reconnecting now", 1, 1)
			else:
				self.handleError("syntax")

		elif msg["cmd"] == "stopBot":
			if len(args) == 0:
				self.feedback("going down now, bye")
				bot.shutdown("stop", "bye, going down", 1, 1)
			else:
				self.handleError("syntax")

		elif msg["cmd"] == "updateBot":
			if len(args) == 0:
				self.feedback("not implemented")
			else:
				self.handleError("syntax")



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
# bot.botdo(action, *args, **kwargs)
#  use this to tell the bot to do something

if nickHgl:
	if fromOwner or auth(uperms, plName, msg["cmd"]):
		if msg["cmd"] == "join":
			if len(args) == 1:
				bot.join(msg["args"])
			else:
				self.handleError("syntax")

		elif msg["cmd"] == "part":
			if len(args) == 0:
				bot.part(target)
			elif len(args) == 1:
				bot.part(msg["args"])

		elif msg["cmd"] == "nick":
			if len(args) == 1:
				bot.changeNick(args[0])
			else:
				self.handleError("syntax")

		elif msg["cmd"] == "exit":
			self.feedback("not implemented")

		elif msg["cmd"] == "privmsg":
			if len(args) > 1:
				bot.privmsg(args[0], " ".join(args[1:]))
			else:
				self.handleError("syntax")

		elif msg["cmd"] == "sendraw":
			if len(args) > 1:
				bot.sendraw(msg["args"])
			else:
				self.handleError("syntax")

		elif msg["cmd"] == "refreshconfig":
			bot.configFile.read()
			bot.config = bot.configFile.data
			self.feedback("success")

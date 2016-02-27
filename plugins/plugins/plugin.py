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
		if msg["cmd"] == "listPlugins":
			if len(args) == 0:
				self.feedback(self.lsPlugins())
			else:
				self.handleError("syntax")

		elif msg["cmd"] == "addPlugin":
			if len(args) == 2:
				if args[0] == "user":
					plH = bot.plH_user
				elif args[0] == "server":
					plH = bot.plH_server
				else:
					plH = None
					self.feedback("unknown mode")
				if plH != None:
					if not args[1] in bot.config["plugins"][args[0]]:
						try:
							plH.addPlugin(args[1])
							bot.config["plugins"][args[0]].append(args[1])
							bot.configFile.save()
							self.feedback("success!")
						except:
							error(target)
					else:
						self.feedback("plugin already added")
			else:
				self.handleError("syntax")

		elif msg["cmd"] == "remPlugin":
			if len(args) == 2:
				if args[0] == "user":
					plH = bot.plH_user
				elif args[0] == "server":
					plH = bot.plH_server
				else:
					plH = None
					self.feedback("unknown mode")
				if plH != None:
					if args[1] in bot.config["plugins"][args[0]]:
						try:
							plH.remPlugin(args[1])
							bot.config["plugins"][args[0]].remove(args[1])
							bot.configFile.save()
							self.feedback("success")
						except:
							self.error(target)
					else:
						self.feedback("plugin not added")

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

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

# def isAdminOfChan(user, chan, bot):
# 	if  chan in bot.chans:
# 		if bot.chans[chan].get(user, None) in [""]:
# 			return True
# 		else:
# 			return False
# 	else:
# 		bot.botdo("raw", "names " + chan)
# 		return False

if nickHgl and not fromOwner and not auth(uperms, plName, msg["cmd"]):
	caperms = self.permM.getPermsOfGroup("#chanadmin")

	if auth(caperms, plName, msg["cmd"]):
		if msg["cmd"] == "join":
			if len(args) == 0:
				self.handleError("syntax")
			elif len(args) == 1:
				if isAdminOfChan(msg["nick"], msg["args"], bot, line):
					bot.botdo("join", msg["args"])
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
					bot.botdo("part", chan)
					self.feedback("success")



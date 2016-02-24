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
#bot.patUMnorm = re.compile(r"(?:(?P<hgl>\w+):\s)?((?:[,.:;?!])(?P<cmd>\w+)\s?)?(?P<args>.*)(?P<reply>)(?P<server>)", re.I)

if nickHgl:
	if fromOwner or auth(uperms, plName, msg["cmd"]):
		if msg["cmd"] == "reconnect":
			self.feedback("bye, I'm failing")
			bot.botdo("reconnect")

		elif msg["cmd"] == "do0":
			self.permM.update()
			self.feedback("success")

		elif msg["cmd"] == "do1":
			self.feedback(bot.chans)

		elif msg["cmd"] == "do2":
			threads = threading.enumerate()
			fb = []
			for t in threads:
				fb.append(t.name)
			self.feedback("'" + "', '".join(fb) + "'")

		elif msg["cmd"] == "do3":
			bot.botdo("raw", "names #digital")
			self.feedback("do3")
#self.echo(msg["cmd"])
if "user" in msgType:
	if not hasattr(self, "callresponse"):
		self.callresponseFile = File(self.path + msgType[0], "_msg/callResponse.json", echo = self.echo)
		self.callresponse = self.callresponseFile.data

	if authed and nickHgl:
		if msg["cmd"] == ":mutecallresponse":
			if len(args) >= 1:
				for chan in args:
					if chan not in self.callresponse["muted"]:
						self.callresponse["muted"].append(chan)

		elif msg["cmd"] == ":unmutecallresponse":
			if len(args) >= 1:
				for chan in args:
					if chan in self.callresponse["muted"]:
						self.callresponse["muted"].remove(chan)

		elif msg["cmd"] == ":listmutedcallresponse":
			self.privmsg(target, self.callresponse["muted"])

		elif msg["cmd"] == ":reloadcallresponse":
			self.callresponseFile.readFile()
			self.callresponse = self.callresponseFile.data
			self.privmsg(target, "reloaded!")


	temp = msg["suffix"].lower().replace(self.nick.lower(), "$nick").replace(" \x01", "\\x01").replace("\x01", "\\x01").lower()

	if temp in self.callresponse["trigger"]:
		for r in self.callresponse["trigger"][temp]:
			self.privmsg(target, r.replace('$nick',self.nick).replace("\\x01action","\x01ACTION").replace("\\x01","\x01").replace('$msg_author_nick', msg["nick"]))
#"""
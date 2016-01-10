
if "server" in msgType:
	if msg["reply"] == "353":
		#NAMES
		#self.chans[msg["target"]] = msg["suffix"].split()
		target = msg["target"]
		if target not in list(self.chans.keys()):
			self.chans[target] = {}
		for user in msg["suffix"].split():
			if user[0] in ["+","%","~","&"]:
				self.chans[target][user[1:]] = user[0]
			else:
				self.chans[target][user] = ""

	elif msg["reply"] == "352":
		#WHO
		if re.match(self.patMsgWHO, msg["suffix"]) != None:
			m = re.match(self.patMsgWHO, msg["suffix"]).groupdict()
			temp = m["nick"] + "!" + m["ident"] + "@" + m["ip"]
			self.users[temp.lower()] = m

	elif msg["reply"] == "315":
		#self.echo(self.users, depth = 2)
		#End of WHO
		pass

	elif msg["reply"] == "432":
		#Erroneous Nickname: Illegal characters
		self.nick = self.oldNick
	elif msg["reply"] == "317":
		self.temp = {}
		self.temp["317"] = {}
		self.temp["317"][msg["target"]] = line
		#Erroneous Nickname: Illegal characters


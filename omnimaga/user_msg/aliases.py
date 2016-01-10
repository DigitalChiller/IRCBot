if "user" in msgType:
	if not hasattr(self, "aliases"):
		self.aliasesFile = File(self.path + msgType[0], "_msg/aliases.json", echo = self.echo)
		self.aliases = self.aliasesFile.data

	if msg["cmd"] != "":
		if msg["cmd"] not in list(self.aliases.keys()):
			for cmd in self.aliases:
				if msg["cmd"] in self.aliases[cmd]:
					msg["cmd"] = cmd
					break
					
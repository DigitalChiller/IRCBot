if "user" in msgType:
	if not hasattr(self, "helpData"):
		self.helpFile = File(self.path + msgType[0], "_msg/help.json", echo = self.echo)
		self.helpData = self.helpFile.data

	if nickHgl:
		if msg["cmd"] == "?help":
			tempTo = msg["nick"]
			if len(args) == 1:
				if args[0] in list(self.helpData.keys()):
					tempHelp = self.helpData[args[0]]
					self.notice(tempTo, "( Help - {nick} - {cmd} )".format(nick=self.nick, cmd=args[0]))
					#self.notice(tempTo, "Help Text for '{cmd}':".format(cmd=args[0]))

					if type(tempHelp) is list:
						for l in tempHelp:
							self.notice(msg["nick"], str(l))
					else:
						self.notice(tempTo, "arguments:")
						self.notice(tempTo, " "*3 + self.helpData[args[0]]["arguments"])

						self.notice(tempTo, "info:")
						for h in tempHelp["help"]:
							self.notice(tempTo, " "*3 + h)

						self.notice(tempTo, "examples:")
						for e in tempHelp["examples"]:
							self.notice(tempTo, " "*3 + e)

				else:
					self.notice(msg["nick"], "unknown Help request '" + str(args[0]) + "'")
					args = []		
			if len(args) == 0:
				tempPages = "'" + "', '".join(self.helpData["pages"]) + "'"
				self.notice(msg["nick"], "available Help Pages: " + tempPages)
				self.notice(msg["nick"], "{nick}: ?help <page|command>".format(nick=self.nick))
				self.notice(msg["nick"], "please report everything from typos to bugs to {boss}".format(boss=self.config["owner"].split("!")[0]))

		if authed:
			if msg["cmd"] == ":refreshhelpfile":
				self.helpFile.readFile()
				self.helpData = self.helpFile.data



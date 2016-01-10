if "user" in msgType:
	if authed and nickHgl:
		if msg["cmd"] == ":addalias":
			if len(args) >= 2:
				if not args[0] in list(self.aliases.keys()):
					self.aliases[args[0]] = []
				self.aliases[args[0]] += args[1:]
				self.aliasesFile.save()
				self.aliases = self.aliasesFile.data
			else:
				self.privmsg(target, "needs atleast 2 arguments")
		elif msg["cmd"] == ":removealias":
			if len(args) >= 2:
				if args[0] not in list(self.aliases.keys()):
					error = "user not found"
				else:
					remaining = set(self.aliases[args[0]]) - set(args[1:])
					if len(remaining) == 0:
						del self.aliases[args[0]]
					else:
						self.aliases[args[0]] = remaining
					self.aliasesFile.save()
					self.aliases = self.aliasesFile.data
			else:
				error = "needs atleast 2 arguments"
		elif msg["cmd"] == ":listalias":
			if len(args) == 0:
				self.privmsg(target, list(self.aliases.keys()))
			elif len(args) == 1:
				self.privmsg(target, self.aliases[args[0]])

		elif msg["cmd"] ==  ":refreshalias":
			self.echo("orrrrr")
			self.aliasesFile.readFile()
			self.aliases = self.aliasesFile.data
			self.privmsg(msg["nick"], "success")

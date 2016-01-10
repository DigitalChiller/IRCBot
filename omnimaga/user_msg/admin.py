#"""
arguments = {
	":part": ":part <channel[,...]>",
	":join": ":join <channel[,...]>",
	":nick": "<new nick name>",
	":exit": "[restart:<True|False>,][reason:<reason>,]",
	":refreshconfig": "None",
	":privmsg": "<target> <msg>",
	":sendraw": "<msg>",
	":removeextension": "<name.py> <type>",
	":addextension": "<name.py> <type>",
	":listextensions": "None",
	":refreshextensions": "None",
	":listgroup": "[<we!we@we.we>]",
	":newgroup": "<name> <command[,...]>",
	":delgroup": "<name>",
	":addcommand": "<group> <command[,...]>",
	":removecommand": "<group> <command[,...]>",
	":listcommand": "",
	":addgroup": "<we!we@we.we> <group[,...]>",
	":removegroup": "<we!we@we.we> <group[...]>"
}
#"""

if self.echoCmd:
	self.echo(msg, fancy = True)
if "user" in msgType:
	if authed and nickHgl:
		error = False
		updategroups = False
		syntax = ""
		if msg["cmd"] == ":part":
			if len(args) == 0:
				self.part(target)
			else:
				self.part(args)
				#error = "needs atleast 1 argument"

		elif msg["cmd"] == ":join":
			if len(args) >= 1:
				self.join(args)
			else:
				error = "needs atleast 1 argument"

		elif msg["cmd"] == ":nick":
			if len(args) == 1:
				self.changeNick(args[0])
			else:
				error = "needs exactly 1 argument"

		elif msg["cmd"] == ":exit":
			kwargs = self.strToDict(msg["args"])
			self.echo(kwargs, "warn")
			self.exit(**kwargs)

		elif msg["cmd"] == ":refreshconfig":
			self.configFile.readFile()
			self.config = self.configFile.data
			self.privmsg(target, "config refreshed!")
		elif msg["cmd"] == ":privmsg":
			self.privmsg(args[0], " ".join(args[1:]))

		elif msg["cmd"] == ":sendraw":
			if len(args) >= 2:
				self.sendRaw(msg["args"] + "\r\n")
			else:
				error = "needs atleast 2 arguments"

		elif msg["cmd"] == ":removeextension":
			if len(args) == 2:
				self.extHandler.rem(args[0], args[1])
			else:
				error = "needs exactly 2 arguments"

		elif msg["cmd"] == ":addextension":
			if len(args) == 2:
				self.extHandler.add(self.path, args[0], args[1])
				self.privmsg(target, "added extension: '{}', type '{}'".format(args[0], args[1]))
			else:
				error = "needs exactly 2 arguments"

		elif msg["cmd"] == ":listextensions":
			temp = self.extHandler.listExtensions()
			self.privmsg(target, temp)
			if False:
				temp = copy.deepcopy(self.extHandler._extensions)
				for t in temp:
					if len(temp[t]) > 0:
						for i,p in enumerate(temp[t]):
							temp[t][i] = str(p)
				self.privmsg(target, temp)
				self.echo(temp, "info", fancy=True)

		elif msg["cmd"] == ":refreshextensions":
			self.extHandler.reloadExtensions()
"""
		elif msg["cmd"] == ":listgroup":
			if len(args) == 1:
				if re.match(re.compile(r"\w+!\w+@\w+[-.w+]+"), args[0]) == None:
					error = "invalid user"
				elif args[0] not in list(self.permuser.keys()):
					error = "user not found"
				else:
					self.permuserFile.readFile()
					self.permuser = self.permuserFile.data
					self.privmsg(target, json.dumps(self.permuserFile.data))
					self.privmsg(target, list(self.permuser[args[0]]))
			else:
				self.groupsFile.readFile()
				self.groups = self.groupsFile.data
				self.privmsg(target, list(self.groups.keys()))
		
		elif msg["cmd"] == ":newgroup":
			if len(args) >= 2:
				if args[0] in self.groups:
					error = "this group does already exist."
				else:
					templist = self.strToList(args[1])
					self.groups[args[0]] = list(args[1:])
					self.echo(self.groupsFile.data)
					updategroups = True
			else:
				error = "needs atleast 2 arguments"

		elif msg["cmd"] == ":delgroup":
			if len(args) == 1:
				if args[0] in set(self.groups.keys()):
					del self.groups[args[0]]
					updategroups = True
				else:
					error = "this group does not exist"
			else:
				error = "needs exactly 1 argument"

		elif msg["cmd"] == ":addcommand":
			if len(args) >= 2:
				templist = self.strToList(args[1])
				self.groups[args[0]] += templist
				updategroups = True
			else:
				error = "needs atleast 2 arguments"

		elif msg["cmd"] == ":removecommand":
			if len(args) >= 2:
				templist = self.strToList(args[1])
				self.groups[args[0]] += templist
				updategroups = True
			else:
				error = "needs atleast 2 arguments"

		elif msg["cmd"] == ":listcommand":
			if len(args) >= 1:
				self.privmsg(target, self.groups[args[0]])
			else:
				error = "needs atleast 1 arguments"

		elif msg["cmd"] == ":addgroup":
			if len(args) >= 2:
				if re.match(re.compile(r"\w+!\w+@\w+[-.w+]+"), args[0]) == None:
					error = "invalid user"
				else:
					if not args[0] in list(self.permuser.keys()):
						self.permuser[args[0]] = []
					self.permuser[args[0]].extend(args[1:])
					self.permuserFile.save()
					self.permuser = self.permuserFile.data

			else:
				error = "needs atleast 1 argument"

		elif msg["cmd"] == ":removegroup":
			if len(args) >= 2:
				if re.match(re.compile(r"\w+!\w+@\w+[-.w+]+"), args[0]) == None:
					error = "invalid user"
				elif args[0] not in list(self.permuser.keys()):
					error = "user not found"
				else:
					remainingGroups = set(self.permuser[args[0]]) - set(args[1:])
					self.echo(remainingGroups)
					if len(remainingGroups) == 0:
						del self.permuser[args[0]]
					else:
						self.permuser[args[0]] = remainingGroups
					self.permuserFile.save()
					self.permuser = self.permuserFile.data
			else:
				error = "needs atleast 1 arguments"

		if updategroups:
			temp = self.groupsFile.save()
			self.groups = self.groupsFile.data
			self.echo(temp)
		if not error == False:
			self.notice(msg["nick"], error + "! arguments: '" + arguments[msg["cmd"]] + "'")

#"""
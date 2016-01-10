if "user" in msgType:
	try:
		if not authed:
			author = msg["nick"].lower()+"!"+msg["hostmask"].lower()
			if author in self.permuser:
				groups = self.permuser[author]
				for g in groups:
					if msg["cmd"] in self.roles[g] or "*" in self.roles[g]:
						authed = True
						break
		if not authed:
			if msg["cmd"] in self.roles["globaladmin"]:
				if not author in self.users:
					self.sendraw("WHO " + msg["nick"])
					self.lines.append(":op!fakeuser@nbot.d1g1t4l.be PRIVMSG {nick} :{nick}: :sr who {user}".format(nick = self.nick, user = msg["nick"]))
				else:
					auPref = self.users[author]["prefix"]
					if "*" in auPref:
						authed = True

	except Exception as e:
		self.echo(traceback.format_exc())

	if authed and nickHgl:
		feedback = False
		updaterole = False
		try:
			if msg["cmd"] == ":refreshrolefile":
				self.rolesFile.readFile()
				self.roles = self.rolesFile.data
				feedback = "success"
			
			if msg["cmd"] == ":refreshpermissionfile":
				self.permuserFile.readFile()
				self.permuser = self.permuserFile.data
				feedback = "success"
			
			elif msg["cmd"] == ":listroles":
				if len(args) == 1:
					if re.match(re.compile(r"\w+!\w+@\w+[-.w+]+"), args[0]) == None:
						feedback = "invalid user"
					elif args[0] not in list(self.permuser.keys()):
						feedback = "user not found"
					else:
						self.permuserFile.readFile()
						self.permuser = self.permuserFile.data
						self.privmsg(target, list(self.permuser[args[0]]))
				else:
					self.rolesFile.readFile()
					self.roles = self.rolesFile.data
					self.privmsg(target, list(self.roles.keys()))
			
			elif msg["cmd"] == ":listpermissions":
				if len(args) >= 1:
					if args[0] in list(self.roles.keys()):
						self.privmsg(target, self.roles[args[0]])
					else:
						feedback = "role not found"
				else:
					feedback = "needs atleast 1 arguments"
			
			elif msg["cmd"] == ":addrole":
				if len(args) >= 2:
					if re.match(re.compile(r"\w+!\w+@[-.\w+]+"), args[0]) == None:
						feedback = "invalid user"
					else:
						if not args[0] in list(self.permuser.keys()):
							self.permuser[args[0]] = []
						self.permuser[args[0]] += args[1:]
						self.permuserFile.save()
						self.permuser = self.permuserFile.data
						feedback = "success"
				else:
					feedback = "needs atleast 1 argument"

			elif msg["cmd"] == ":addpermission":
				if len(args) >= 2:
					if not args[0] in list(self.roles.keys()):
						self.roles[args[0]] = []
					self.roles[args[0]] += args[1:]
					updaterole = True
					feedback = "success"
				else:
					feedback = "needs atleast 2 arguments"

			elif msg["cmd"] == ":removerole":
				if len(args) >= 1:
					if re.match(re.compile(r"\w+!\w+@[-./w]+"), args[0]) == None:
						feedback = "invalid user"
					elif args[0] not in list(self.permuser.keys()):
						feedback = "user not found"
					else:
						if len(args) == 2:
							remaining = set(self.permuser[args[0]]) - set(args[1:])
							self.permuser[args[0]] = remaining
							self.echo(remaining)
						if len(args) == 1 or len(self.permuser[args[0]]) == 0:
							del self.permuser[args[0]]
						self.permuserFile.save()
						self.permuser = self.permuserFile.data
						feedback = "success"
				else:
					feedback = "needs atleast 1 arguments"

			elif msg["cmd"] == ":removepermission":
				if len(args) >= 1:
					if not args[0] in list(self.roles.keys()):
						if len(args) == 1:
							del self.roles[args[0]]
						else:
							self.roles[args[0]] += args[1:]
						updaterole = True
						feedback = "success"
					else:
						feedback = "role does not exist"
				else:
					feedback = "needs atleast 1 arguments"

			elif msg["cmd"] == ":addsubject" and False:
				if len(args) == 1:
					if args[0] in list(self.roles.keys()):
						feedback = "role already exists"
					else:
						updaterole = True
						feedback = "success"
				else:
					feedback = "needs exactly 1 argument"

			elif msg["cmd"] == ":removesubject" and False:
				if len(args) == 1:
					if args[0] in set(self.roles.keys()):
						updaterole = True
						feedback = "success"
					else:
						feedback = "this role does not exist"
				else:
					feedback = "needs exactly 1 argument"

		except Exception as e:
			self.echo(traceback.format_exc())
			self.privmsg(msg["nick"], e)
		finally:			
			if updaterole:
				temp = self.rolesFile.save()
				self.roles = self.rolesFile.data
				self.echo(temp)

			if not feedback == False:
				self.notice(msg["nick"], feedback)

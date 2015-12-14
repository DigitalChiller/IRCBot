
if re.match(self.patUserMsg, msg) != None:
	msgSp = re.fullmatch(self.patUserMsg, msg).groupdict()
	#self.echo(msgSp, fancy = False)
	self.isAllowed(msgSp)
	cmd = "__"+msgSp["command"]+"__"
	authed = self.authed
	msgSp["suffix"] = msgSp["suffix"].rstrip()
	msgSp["args"] = msgSp["args"].rstrip()
	args = msgSp["args"].split()
	temp = msgSp["suffix"].replace(self.nick, "$nick").replace("\x01", "\\x01").lower()
	
	if self.nick.lower() == msgSp["target"].lower():
		target = msgSp["nick"]
	else:
		target = msgSp["target"]
	if msgSp["hgl"] != None:
		nickHgl = str.lower(msgSp["hgl"]) == self.nick.lower()
	else:
		nickHgl = False
	
	if temp in self.config["commands"]:
		if type(self.config["commands"][temp]) is str:
			responses = []
			responses.append(self.config["commands"][temp])
		else:
			responses = self.config["commands"][temp]
		for r in responses:
			self.privmsg(target, r.replace('$nick',self.nick).replace("\\x01","\x01").replace('$msg_author_nick', msgSp["nick"]))

	elif authed and nickHgl and "__:part__:p__:leave__:l__".find(cmd) != -1:
		if len(args) >= 1:
			self.part(args)
	elif authed and nickHgl and "__:join__:j__".find(cmd) != -1:
		if len(args) >= 1:
			self.join(args)
	elif authed and nickHgl and "__:nick__:n__".find(cmd) != -1:
		if len(args) == 1:
			self.changeNick(args[0])
	elif authed and nickHgl and "__:exit__:e__:shutdown__:s__".find(cmd) != -1:
		if len(args) == 1:
			self.shutdown(restart = args[0])
		elif len(args) == 2:
			self.shutdown(restart = args[0], delay = args[1])
		elif len(args) >= 3:
			self.shutdown(restart = args[0], delay = args[1], quitMsg = " ".join(args[2:]))
		pass
	elif authed and nickHgl and "__:reloadconfig__:relconf__".find(cmd) != -1:
		self.configFile.readFile()
		self.config = self.configFile.data["server"][self.name]
		self.echo("config reloaded!")
		pass
	elif authed and nickHgl and "__:privmsg__:pm__".find(cmd) != -1:
		self.privmsg(msgSp["nick"], msgSp["args"])
		pass
	elif authed and nickHgl and "__:sendRaw__:sr__".find(cmd) != -1:
		self.sendRaw(msgSp["args"] + "\r\n")
		pass
	elif authed and nickHgl and "__:removeplugin__:remp__".find(cmd) != -1:
		if len(args) == 2:
			self.plHandler.rem(args[0], args[1])
			#self.echo(args)
		pass
	elif authed and nickHgl and "__:addplugin__:ap__".find(cmd) != -1:
		if len(args) == 2:
			self.plHandler.add(args[0], args[1])
		pass
	elif authed and nickHgl and "__:listplugins__:lp__".find(cmd) != -1:
		self.echo(self.plHandler._plugins)
		pass
	elif authed and nickHgl and "__:reloadplugins__:relp__".find(cmd) != -1:
		self.plHandler.reloadPlugins()
		pass
	elif authed and nickHgl and "__:cmd1__:cmd2__".find(cmd) != -1:
		#dostuff
		pass



elif re.match(self.patServerMsg, msg) != None:
	msgSp = re.fullmatch(self.patServerMsg, msg).groupdict()

	if msgSp["reply"] == "353": #NAMES
		self.chans[msgSp["target"]] = msgSp["suffix"].split()
	elif msgSp["reply"] == "352": #WHO
		#self.echo(msgSp["suffix"])
		if re.match(self.patMsgWHO, msgSp["suffix"]) != None:
			m = re.match(self.patMsgWHO, msgSp["suffix"]).groupdict()
			temp = m["ident"] + "@" + m["ip"]
			self.users[temp] = m
	elif msgSp["reply"] == "315": #End of WHO
		#self.userchanFile.saveJson()
		#self.echo(self.users, "[>] ", dpth = 1, cmpct = True)
		pass
	elif msgSp["reply"] == "432": #Erroneous Nickname: Illegal characters
		self.nick = self.oldNick


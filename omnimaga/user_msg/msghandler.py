if self.echoCmd:
	self.echo(msg)
if "user" in msgType:
	if authed and nickHgl and "__:part__:p__:leave__:l__".find(cmd) != -1:
		if len(args) >= 1:
			self.part(args)
	elif authed and nickHgl and "__:join__:j__".find(cmd) != -1:
		if len(args) >= 1:
			self.join(args)
	elif authed and nickHgl and "__:nick__:n__".find(cmd) != -1:
		if len(args) == 1:
			self.changeNick(args[0])
	elif authed and nickHgl and "__:exit__:e__".find(cmd) != -1:
		kwargs = {}
		try:
			temp = []
			if len(args) == 0:
				pass
			elif msg["args"].find(","):
				temp = msg["args"].split(",")
			else:
				temp.append(msg["args"])
			self.echo(temp, "warn")
			for arg in temp:
				t = arg.split(":")
				kwargs[t[0]] = t[1]
			self.exit(**kwargs)
		except Exception as e:
			self.echo(e, "warn")
	elif authed and nickHgl and "__:reloadconfig__:relconf__".find(cmd) != -1:
		self.configFile.readFile()
		self.config = self.configFile.data["server"][self.name]
		self.echo("config reloaded!")
		pass
	elif authed and nickHgl and "__:privmsg__:pm__".find(cmd) != -1:
		self.privmsg(args[0], " ".join(args[1:]))
		pass
	elif authed and nickHgl and "__:sendRaw__:sr__".find(cmd) != -1:
		self.sendRaw(msg["args"] + "\r\n")
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
	elif authed and nickHgl and "__:break__:b__".find(cmd) != -1:
		self.detectTimeout = False
		self.echoPiong = False
		#self.echo(self.doPingPong)
		#self.breakstuff = True
		#dostuff
		pass
	elif not authed and nickHgl and "__:cmd1__:cmd2__".find(cmd) != -1:
		#dostuff
		pass



elif msgType == "server":
	if msg["reply"] == "353": #NAMES
		self.chans[msg["target"]] = msg["suffix"].split()
	elif msg["reply"] == "352": #WHO
		#self.echo(msg["suffix"])
		if re.match(self.patMsgWHO, msg["suffix"]) != None:
			m = re.match(self.patMsgWHO, msg["suffix"]).groupdict()
			temp = m["ident"] + "@" + m["ip"]
			self.users[temp] = m
	elif msg["reply"] == "315": #End of WHO
		#self.userchanFile.saveJson()
		#self.echo(self.users, "[>] ", dpth = 1, cmpct = True)
		pass
	elif msg["reply"] == "432": #Erroneous Nickname: Illegal characters
		self.nick = self.oldNick


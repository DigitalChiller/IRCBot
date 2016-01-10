if "user" in msgType:
	error = False
	#self.echo(msg, fancy = False)
	if msg["cmd"] == "!uptime":
		if len(args) == 1:
			infotype = "uptime"
		else:
			infotype = args[1]
			waitfor = "317 {nick} {user} ".format(nick=self.nick, user=args[0])
			cmd = 'self.lines.append(":user!fakeuser@nbot.d1g1t4l.be PRIVMSG {target} :{nick}: :uauptime {user} {type}")'.format(target=target,nick=self.nick, user=args[0], type=infotype)
			threading.Thread(None, self.task, args=[cmd], kwargs={"waitfor":waitfor}).start()
			self.sendRaw("WHOIS " + args[0])

	elif nickHgl:
		if msg["cmd"] == ":uauptime":
			if len(args) == 2:
				try:
					tempTime = int(self.temp["317"][args[0]].split()[5])
					tempInfo = None
					if args[1] == "uptime":
						tempInfo = str(datetime.timedelta(seconds=int(time.time()) - tempTime))
					elif  args[1] in ["sign-on", "sign on"]:
						tempInfo = str(datetime.datetime.fromtimestamp(float(tempTime)))
					elif args[1] == "idle":
						tempTime = int(self.temp["317"][args[0]].split()[4])
						tempInfo = str(datetime.timedelta(seconds=int(tempTime)))
					if tempInfo == None:
						self.privmsg(target, "Error: unknown specifier")
					else:
						self.privmsg(target, "{user}'s {type}: {time}".format(user=args[0], type=args[1], time=tempInfo))
				except Exception as e:
					self.privmsg(target, "Error: no information about the uptime available")
					self.echo(traceback.format_exc())
	if error != False:
		self.notice(msg["nick"], error)


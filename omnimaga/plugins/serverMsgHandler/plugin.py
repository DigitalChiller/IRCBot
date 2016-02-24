### Variables
## call args
# msg = message dict
# nickhlg = is bot addressed? (bot: <message>)
# userperm = not implemented yet, probably permissions of the message author
# 
## return args
# handled = is the message handled by this plugin
# feedback = message sent back to channel

try:
	if msg["reply"] == "353":
		#NAMES
		target = msg["all"].split()[4]
		if target not in bot.chans:
			bot.chans[target] = {}
		user = msg["suffix"].lower().split()[2:]
		user[0] = "".join(user[0][1:])
		for u in user:
			if u[0] in ["+","%","~","&","@"]:
				bot.chans[target][u[1:]] = u[0]
			else:
				bot.chans[target][u] = ""

	elif msg["reply"] == "352":
		#WHO
		if re.match(bot.patMsgWHO, msg["suffix"]) != None:
			m = re.match(bot.patMsgWHO, msg["suffix"]).groupdict()
			temp = m["nick"] + "!" + m["ident"] + "@" + m["ip"]
			bot.users[temp.lower()] = m

	elif msg["reply"] == "315":
		#bot.echo(bot.users, depth = 2)
		#End of WHO
		pass

	elif msg["reply"] == "432":
		#Erroneous Nickname: Illegal characters
		bot.nick = bot.oldNick
	elif msg["reply"] == "317":
		bot.temp = {}
		bot.temp["317"] = {}
		bot.temp["317"][msg["target"]] = line
		#Erroneous Nickname: Illegal characters

except Exception as e:
	tb = traceback.format_exc()
	echo(tb, "warn")
	bot.privmsg(bot.config["owner"],tb.splitlines()[-1])



uperms = self.permM.perms(msg["ident"].lower())

def auth(perms, plName, *args):
	args = list(args)
	args += ["*"]
	for a in args:
		if plName+"."+a in perms:
			return True
	return False
	#return plName + ".*" in uperms or plName+"."+cmd in uperms

def isAdminOfChan(user, chan, bot, line=None):
	if  chan in bot.chans:
		if bot.chans[chan].get(user.lower(), None) in ["%","~","&","@"]:
			return True
	else:
		bot.botdo("raw", "names " + chan)
		time.sleep(0.4)
		if line != None:
			threading.Timer(0.5, bot.fakesend, (line,)).start()
	return False

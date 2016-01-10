def __init__():
	arguments = {}
	helptext = {}

def timed(command):
	exec(command)


if "user" in msgType:
	if authed and nickHgl:

		if msg["cmd"] == ":toggleEchoPiong":
			self.echoPiong = not self.echoPiong

		elif msg["cmd"] == ":toggleDetectTimeout":
			self.detectTimeout = not self.detectTimeout

		elif msg["cmd"] == ":toggleDoPiong":
			self.doPiong = not self.doPiong

		elif msg["cmd"] == ":action0":
			self.privmsg(target, "hey")
			pass

		elif msg["cmd"] == ":action1":
			self.privmsg(target, list(self.callresponse.keys()))
			pass

		elif msg["cmd"] == ":action2":
			self.echo(self.chans, fancy = False, depth = 2)
			pass
		elif msg["cmd"] == ":action3":
			self.echo("aher")
			threading.Timer(1,exec, args=["self.waitFor('dotheflop');self.echo('dotheflop')", globals(), locals()]).start()
			pass


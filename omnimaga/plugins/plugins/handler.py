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
	if nickHgl:
		if msg["cmd"] == ":listextensions":
			if len(args) == 0:
				feedback = {} 
				for t in bot.extensions:
					feedback[t] = list(bot.extensions[t].keys())
			elif len(args) == 1:
				if args[0] in bot.extensions:
					feedback = list(bot.extensions[args[0]].keys())
				else:
					error = "Extension type not found"
			else:
				error = "syntax"

		elif msg["cmd"] == ":addextension":
			if len(args) == 1:
				try:
					ext = bot.addExtension(args[0])
				except Exception as e:
					echo(traceback.format_exc(), "warn")
					if type(e) is FileNotFoundError:
						error = "Extension is damaged or does not exist"
					else:
						sendowner(traceback.format_exc().splitlines()[-1])
						error = "unknown"
				else:
					feedback = "success!"
			else:
				error = "syntax"

		elif msg["cmd"] == ":removeextension":
			if len(args) == 1:
				try:
					ext = bot.removeExtension(args[0])
				except Exception as e:
					echo(traceback.format_exc(), "warn")
					if type(e) is FileNotFoundError:
						error = "Extension not found"
					else:
						sendowner(traceback.format_exc().splitlines()[-1])
						error = "unknown"
				else:
					if len(args) == 1:
						handles = ext.handles
					else:
						handles = args[1:]
					feedback = "success!"
			else:
				error = "syntax"


		elif msg["cmd"] == ":do3":
			feedback = "do3"

		else:
			handled = False
except Exception as e:
	tb = traceback.format_exc()
	echo(tb, "warn")
	bot.privmsg(target,tb.splitlines()[-1])



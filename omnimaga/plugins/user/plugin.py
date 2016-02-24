## variables
# msg = message dict
# args = list of args
# nickHgl = is bot addressed? (bot: <message>)
# target = channel or private chat
# fromOwner = author is owner
# 
## functions
# self.feedback(msg)
#  use this to send something back
# self.botdo(action, *args, **kwargs)
#  use this to tell the bot to do something

if nickHgl:
	if msg["cmd"] == "cmd1":
		self.feedback("cmd1")

	elif msg["cmd"] == "cmd2":
		self.feedback("cmd1")



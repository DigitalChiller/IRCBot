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
# bot.botdo(action, *args, **kwargs)
#  use this to tell the bot to do something

if nickHgl:
	if fromOwner or auth(uperms, plName, msg["cmd"]):
		if len(args) == 0:
			if msg["cmd"] == "refreshpermfile":
				self.permM.readConf()
				self.feedback("success")

			elif msg["cmd"] == "lsgroups":
				self.feedback(self.permM.getGroups())

		elif len(args) == 1:
			if msg["cmd"] == "lsuperms":
				self.feedback(self.permM.perms(args[0]))

			elif msg["cmd"] == "lsgperms":
				self.feedback(self.permM.getPermsOfGroup(args[0]))

			elif msg["cmd"] == "lsugroups":
				self.feedback(self.permM.getGroupsOfUser(args[0]))

			elif msg["cmd"] == "newGroup":
				self.permM.newGroup(args[0])
				self.feedback("success")

			elif msg["cmd"] == "delGroup":
				self.permM.delGroup(args[0])
				self.feedback("success")

		else:
			if msg["cmd"] == "addUserToGroup":
				self.permM.addUserToGroup(args[0].lower(), args[1:])
				self.feedback("success")

			elif msg["cmd"] == "remUserFromGroup":
				self.permM.remUserFromGroup(args[0].lower(), args[1:])
				self.feedback("success")

			elif msg["cmd"] == "addPermToGroup":
				echo("hey")
				self.permM.addPermToGroup(args[0], args[1:])
				self.feedback("success")

			elif msg["cmd"] == "remPermFromGroup":
				#echo(args[1:])
				self.permM.remPermFromGroup(args[0], args[1:])
				self.feedback("success")



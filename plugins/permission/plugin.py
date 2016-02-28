## LICENSE
#    This file is part of nBot.
#
#    nBot is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nBot is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with nBot.  If not, see <http://www.gnu.org/licenses/>.
#


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

if nickHgl:
	if fromOwner or auth(uperms, plName, msg["cmd"]):
		if len(args) == 0:
			if msg["cmd"] == "refreshPermFile":
				self.permM.readConf()
				self.feedback("success")

			elif msg["cmd"] == "listGroups":
				self.feedback(self.permM.getGroups())

		elif len(args) == 1:
			if msg["cmd"] == "listPermsOfUser":
				self.feedback(self.permM.perms(args[0]))

			elif msg["cmd"] == "listPermsOgGroup":
				self.feedback(self.permM.getPermsOfGroup(args[0]))

			elif msg["cmd"] == "listGroupsOfUser":
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



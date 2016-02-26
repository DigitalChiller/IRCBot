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


for i in range(0,1):
	pass
	if action == "privmsg" and len(args) == 2:
		self.privmsg(args[0], args[1])
	elif action == "notice" and len(args) == 2:
		self.notice(args[0], args[1])
	elif action == "warn" and len(args) == 1:
		self.sendowner(args[0])
	elif action == "raw" and len(args) == 1:
		self.sendRaw(args[0])
	elif action == "part" and len(args) == 1:
		self.part(args[0])
	elif action == "join" and len(args) == 1:
		self.join(args[0])

	elif action == "reconnect":
		self.failed = True
		self.failinfo.append({"type":"debug", "time":time.time()})

	elif action == "plugin":
		if len(args) <= 1:
			retvar = False
		elif len(args) >= 2:
			if args[0] == "user":
				plH = self.plH_user
			elif args[0] == "server":
				plH = self.plH_server
			else:
				retvar = False
				break
			if args[1] == "list":
				retvar = plH.lsPlugins()
			elif len(args) == 4:
				if args[2] == "add":
					if not args[3] in self.config["plugins"][args[0]]:
						plH.addPlugin(args[3])
						self.config["plugins"][args[0]].append(args[3])
					else:
						retvar = False
				elif args[2] == "remove":
					if args[3] in self.config["plugins"][args[0]]:
						plH.remPlugin(args[3])
						self.config["plugins"][args[0]].remove(args[3])
					else:
						retvar = False

	elif action == "perm":
		if len(args) == 1:
			if args[0] == "listgroups":
				retvar = self.permM.getGroups()
			else:
				retvar = False
		elif len(args[0]) == 2:
			if args[0] == "listuperms":
				retvar = self.permM.getPermsOfUser(args[1])
			elif args[0] == "listgperms":
				retvar = self.permM.getPermsOfGroup(args[1])
			elif args[0] == "listugroups":
				retvar = self.permM.getGroupsOfUser(args[1])
			if args[0] == "add":
				retvar = self.permM.getPermsOfUser(args[1])

			else:
				pass

	else:
		echo(args)
		echo(kwargs)
		retvar = False

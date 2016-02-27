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

if nickHgl and msg["cmdPref"] in [",","?"]:
	if msg["cmd"] == "help":
		if len(args) == 0:
			self.feedback("Hello, I'm nBot!")
			self.feedback("Syntax: " + self.help["help"][0])
			self.feedback("all user commands:")
			self.feedback("'"+"', '".join(self._usercmds)+"'") #self.usercmd

		else:
			sendSyntax(self, msg["args"])
	elif fromOwner or auth(uperms, plName, msg["cmd"]):
		if msg["cmd"] == "reloadHelp":
			if len(args) == 1:
				if self.reloadHelp(args[0]):
					self.feedback("success")
				else:
					self.feedback("fail")
			else:
				self.handleError("syntax")

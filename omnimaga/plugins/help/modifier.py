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

def sendSyntax(self, cmd):
	for p in self.lsPlugins():
		helptext = self.plVars[p].help.get(cmd, None)
		if helptext != None:
			break
	if helptext == None:
		helptext = ["no help aviable, report this"]
		return False

	for l in helptext:
		self.feedback(l)

	return True

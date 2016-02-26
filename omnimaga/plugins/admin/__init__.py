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

try:
	#create files and stuff
	self.infotext = "this extension is a template"

	
	self.helpcmd = {}
	self.helpcmd["all"] = ["list of commands"]
	self.helpcmd[":cmd"] = {"syntax":":cmd <syntax>","info":"that command does not exist"}
	
	self.helpperm = {}
	self.helpperm["all"] = ["list of all permissions except plname.* or plname.cms"]

	self.settings = {"all":[]} #TODO

	self.handles = ["user"]

except:
	#fail, report it
	traceback.print_exc()

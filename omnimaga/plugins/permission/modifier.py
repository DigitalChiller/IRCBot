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

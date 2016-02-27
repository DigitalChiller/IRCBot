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
# 
## Variables
# msg = message dict, look at IRC.py
# args = list of args
# nickHgl = is bot addressed directly? (bot: <message>)
# target = channel or private chat most responses should go in
# fromOwner = author is owner
# bot = the bot object
# uperms = list of permission the user has
# 
## Functions
# self.feedback(msg)
#  use this to send responses
# auth(perms, plName, command/permission*)
#  use this to test if a user is authed to execute a command
# isAdminOfChan(user, chan, bot, line, sendDelay)
#  use this to detect if a user is chanadmin in the channel. see permission/modifier.py

if nickHgl and msg["cmdPref"] == ",":
	if fromOwner or auth(uperms, plName, msg["cmd"]):
		if msg["cmd"] == "togglePingPong":
			bot.logPingPong = not bot.logPingPong
			self.feedback("logPingPong: " + str(bot.logPingPong))

		elif msg["cmd"] == "do0":
			self.feedback(colored(bold("Test:test"), "red")+italic("test"))

		elif msg["cmd"] == "do1":
			self.feedback("buh")
			bot.shutdown("restart")
			#bot._stopnow = True

		elif msg["cmd"] == "do2":
			threads = threading.enumerate()
			fb = []
			for t in threads:
				fb.append(t.name)
			self.feedback("'" + "', '".join(fb) + "'")

		elif msg["cmd"] == "do3":
			bot.sendraw("names #digital")
			self.feedback("do3")

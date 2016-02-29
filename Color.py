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

reset = "\x0F"

colors = {
	"white": "00",
	"black": "01",
	"blue": "02",
	"green": "03",
	"red": "04",
	"brown": "05",
	"purple": "06",
	"orange": "07",
	"yellow": "08",
	"lightgreen": "09",
	"cyan": "10",
	"lightcyan": "11",
	"lightblue": "12",
	"pink": "13",
	"grey": "14",
	"lightgrey": "15"
}

def bold(msg):
	return "\x02" + str(msg) + "\x02"

def color(msg):
	return "\x03" + str(msg) + "\x03"

def italic(msg):
	return "\x1D" + str(msg) + "\x1D"

def underline(msg):
	return "\x1F" + str(msg) + "\x1F"

def swapFB(msg):
	return "\x16" + str(msg) + "\x16"


def colored(msg, fg="default", bg="default"):
	return color(colors.get(fg,"99") + "," + colors.get(bg,"99") + str(msg))


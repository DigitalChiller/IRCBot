#!/usr/bin/python3

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


#import traceback, json, socket, time, re, chardet, random, threading
#import queue, pprint, sys, signal, ssl, curses
#from echo import Echo
#===== import stuff
import traceback
import datetime
import re
import time
import socket
import chardet
import random
import threading
import queue
import pprint
import sys
import os
import signal
import ssl
import copy
import curses
import curses.textpad
import json
import Echo 	#look at Echo.py

def randStr(length):
		temp = ''
		for i in range(length):
			temp = temp + random.choice('abcdefghijklmnopqrstuvwxyz')
		return temp	

class VariableBundle(object):
	"""use this for variable managing"""
	pass
	# def __init__(self):
	# 	super(VariableBundle, self).__init__()
		
class Config():
	"""
	This class is for easier File handling.
	"""
	def __init__(self, filePath, *args):
		self.filePath = filePath
		self.read()
	
	def read(self):
		with open(self.filePath) as f:
			lines = f.readlines()
			self.data = json.loads("\n".join(lines))
		return self.data

	def save(self):
		with open(self.filePath, "w") as f:
			json.dump(self.data, f, indent = 4)



class SocketHandler(threading.Thread):
	"""docstring for SocketHandler"""
	def __init__(self, address, port, buffersize, encoding, is_ssl=False, name="sHandler"):
		super(SocketHandler, self).__init__()
		self.name = name
		self.address = address
		self.port = port
		self.buffersize = buffersize
		self.encoding = encoding
		self.is_ssl = is_ssl

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if self.is_ssl:
			self.s = ssl.wrap_socket(self.s)

		self.connected = False
		self._stopnow = False
		self.q = queue.Queue()
		self.failed = False
		self.failinfo = {}

	def run(self):
		self.s.connect((self.address,self.port)) #connect to the server
		self.connected = True

		while not self._stopnow:
			stuff = self.s.recv(self.buffersize)
			try:				#trying to decode the message
				stuff = stuff.decode(self.encoding)
			except:
				if stuff != '':
					try:
						stuff = stuff.decode(chardet.detect(stuff)['encoding'])
					except Exception as e:
						if e is BrokenPipeError or ConnectionResetError:
							echo(traceback.format_exc(), "warn")
							self.failed = True
							self.failinfo = {"type":type(e).__name__, "time":time.time()}
							return

			for line in stuff.replace("\r","").split("\n"):		#split received messages by new lines and put them into self.lines
				self.q.put(line)

	def stop(self):
		self.s.shutdown(0)
		self.s.close()
		self._stopnow = True

	def send(self, msg):
		self.s.send(bytes(msg, self.encoding))						



class PermissionManager(object):
	"""docstring for PermissionManager"""
	def __init__(self, configDir, default=None):
		super(PermissionManager, self).__init__()
		self.default = default
		self.configDir = configDir

		self._groups = {} #group:{perms}
		self._users = {} #user:{groups}
		self._perms = {} #user:{perms} #don't edit, will be updated automatically

		self._configFile = Config(self.configDir+"perm-config.json")
		
		self.readConf()

		# self._data = self._configFile.read()
		# self._groups = self._data["groups"]
		# self._users = self._data["users"]
		# self.update()


	def newGroup(self, group):
		#creates a new group
		if group in self._groups:
			return False
		else:
			self._groups[group] = []
			self.update()
			return True

	def delGroup(self, group):
		#removes an existing group
		if group in self._groups:
			self._groups.remove(group)
			self.update()
			return True
		else:
			return False


	def addPermToGroup(self, group, perms):
		#adds permissions to an existing group
		if group in self._groups:
			self._groups[group].extend(perms)
			self.update()
			return True
		else:
			return False
			

	def remPermFromGroup(self, group, perms):
		#removes permissions from an existing group
		if group in self._groups:
			for p in perms:
				if p in self._groups[group]:
					self._groups[group].remove(p)
			self.update()
			return True
		else:
			return False


	def addUserToGroup(self, user, groups):
		#adds an user to groups
		if user not in self._users:
			self._users[user] = []

		for g in set(groups):
			if g not in self._users[user] and g in self._groups:
				self._users[user].append(g)

		self._users[user] = list(set(self._users[user]))
		self.update()

	def remUserFromGroup(self, user, groups):
		#removes an user from groups
		for g in set(groups):
			if g in self._groups:
				self._users[user].remove(g)
				self.update()

	def getGroups(self):
		#returns a list with all groups
		return list(self._groups)

	def getGroupsOfUser(self, user):
		#returns a list with all groups of an user
		return self._users.get(user, self.default)

	def getPermsOfGroup(self, group):
		#returns a list with all permissions of a group
		return self._groups.get(group, self.default)

	def getPermsOfUser(self, user):
		#returns a list with all permissions of an user
		return self._perms.get(user, self.default)


	def update(self):
		for u in self._users:
			self._perms[u] = []
			for g in self._users[u].copy():
				if g in self._groups:
					echo(g)
					self._perms[u].extend(self._groups[g])
				else:
					self._users[u].remove(g)

		self._data["groups"] = self._groups
		self._data["users"] = self._users
		self._configFile.save()

	def readConf(self):
		self._data = self._configFile.read()
		self._groups = self._data["groups"]
		self._users = self._data["users"]
		self.update()

	def perms(self, user):
		return self.getPermsOfUser(user)



class PluginHandler(threading.Thread):
	"""docstring for ExtensionHandler"""

	def __init__(self, dataDir, bot, *, pluginDir="plugins/", name="plHandler"):
		super(PluginHandler, self).__init__()
		self.name = name
		self.bot = bot
		self.dataDir = dataDir
		self.pluginDir = pluginDir
		self._plugins = {}
		self._modifiers = {}

		self.plVars = {}
		self.lastTarget = ""

		self.q = queue.Queue()
		self._stopnow = False

	def run(self):
		while not self._stopnow:
			while self.q.empty():
				if self._stopnow:
					return
				time.sleep(0.01)

			lvars = self.q.get()

			self.lastTarget = lvars["msg"]["target"]
			lvars["self"] = self
			lvars["bot"] = self.bot

			for l in [self._modifiers, self._plugins]:
				for i in l.copy():
					try:
						lvars["plName"] = i.split("/")[-2]
						lvars["pv"] = self.plVars[lvars["plName"]]

						with open(i) as f:
							exec(f.read(), globals(), lvars)
					except:
						error(info=i)

			self.q.task_done()
	
	def stop(self):
		self._stopnow = True

	def feedback(self, msg):
		if self.lastTarget != "":
			self.bot.privmsg(self.lastTarget, msg)
		else:
			echo("target unknown, couldn't send '" + line + "'")

	def handleError(self, error, *args, fb=True):
		if error == "syntax":
			self.feedback("invalid syntax: " + " ".join(args))

		elif error == "unknown":
			self.feedback("Unknown error: something unexpected happend")

		else:
			self.feedback(error + ": " + " ; ".join(args))


	def addPlugin(self, plName):
		try:
			pldir = self.pluginDir + plName + "/"
			dataDir = self.dataDir + plName + "/"
			plFiles = os.listdir(pldir)
			try:
				dFiles = os.listdir(dataDir)
			except FileNotFoundError:
				os.makedirs(dataDir)
			except Exception as e:
				raise e

			if "plugin.py" in plFiles:
				self._plugins[pldir + "plugin.py"] = {} 
			if "modifier.py" in plFiles:
				self._modifiers[pldir + "modifier.py"] = {}

			self.plVars[plName] = VariableBundle()
			self.plVars[plName].name = plName
			self.plVars[plName].dataDir = dataDir
			self.plVars[plName].info = "no information specified"
			self.plVars[plName].help = {}

			lvars = {}
			lvars["pv"] = self.plVars[plName]
			lvars["self"] = self
			lvars["bot"] = self.bot


			with open(pldir + "__init__.py") as f:
				exec(f.read(), globals(), lvars)

			if "help.py" in plFiles:				
				with open(pldir + "help.py") as f:
					exec(f.read(), globals(), lvars)

			echo("added plugin " + plName)

		except:
			error(info=plName)
			return False
		else:
			return True

	def remPlugin(self, plName):
		try:
			pldir = self.pluginDir + plName + "/"

			if pldir + "plugin.py" in self._plugins:
				self._modifiers.remove(pldir + "plugin.py")			

			if pldir + "modifier.py" in self._modifiers:
				self._modifiers.remove(pldir + "modifier.py")

		except:
			echo(traceback.format_exc(), "warn")
			return False
		else:
			return True

	def lsPlugins(self):
		temp = []
		for p in self._plugins:
			temp.append(p.split("/")[-2])
		return temp

	def reloadHelp(self, plName):
		try:
			pldir = self.pluginDir + plName + "/"
			self.plVars[plName].help = {}
			lvars = locals()
			lvars["pv"] = self.plVars[plName]
			with open(pldir + "help.py") as f:
				exec(f.read(), globals(), lvars)

			return True
		except:
			error()
			return False



class IRCBot(threading.Thread):
	"""docstring for IRCServer"""
	def __init__(self, name, dojoin = True, *, doMsgHandle = True, buffer = 4096, encoding = 'UTF-8'):
	
		super(IRCBot, self).__init__()
		global SCREEN
		global LogOutp
		global echo

		SCREEN = Echo.start() 
		LogOutp = Echo.ScrollText(scrollback = 200, posy = 0, posx = 0, height= 24, width = 80, logFile = "server/" + name + "/logs.txt")
		echo = LogOutp.echo


		LogOutp.addPref("warn", "\r{warn}", curses.color_pair(11)) #these define custom prefixes for the console output
		LogOutp.addPref("ping", "\r(ping)", curses.color_pair(11))	
		LogOutp.addPref("recv", "\r[recv]", curses.color_pair(15))
		LogOutp.addPref("send", "\r[send]", curses.color_pair(16))
		
		global error
		error = self.error

		echo("-----SETTING EVERYTHING UP-----")

		self.handle_resize()

		signal.signal(signal.SIGWINCH, self.handle_resize)

		# Bot name, not irc nick!
		self.serverName = name #the name (folder) of the server/bot, each must be unique
		#os.chdir(self.serverName)
		# path to the Bot directory
		self.botDir = "server/" + name + "/"

		# buffer size
		self.buffer = buffer
		# prefered encoding, do i even use this?
		self.encoding = encoding

		# indicates if the bot is correctly connected to the server, True if so, False otherwise
		self.connected = False
		# indicates if the bot is shutting down, True if so, False otherwise
		self._stopnow = False
		# self explaining
		self._paused = False
		# indicates whether the bot will restart or fully quit after shutdown, True if restart, False if fully quit
		self._restart = True
		# indicates if something bad happend, True if so, False otherwise 
		self.failed = False
		# list of information about the fail, every list item is a dict which must contain "type":"<type>" and "time":time.time(), it can contain more
		self.failinfo = [{"type":None, "time":time.time()}]

		# indicates if the bot answers pings, True if so, False otherwise
		self.answerPing = True

		# indicates if the bot pings the server, True if so, False otherwise
		self.sendPing = True
		
		# indicates if ping/pong messages are logged, True if so, False otherwise
		self.logPingPong = True

		# time between ping requests from the bot
		self.pingFrequency = 105
		
		# maximum time waited for the server to response to a ping
		self.maxPingTimeout = 42

		# if true the bot shuts down on pingtimeouts
		self.doDetectTimeout = True	#if True the bot restarts or shuts down when the bot detects a Ping Timeout
		
		# indicates if MOD is logged, True if not so, False otherwise
		self.blockMOTD = False 			#if True MOTD is not logged
		# indicates if detailed command information are logged 
		self.debug_logcmd = False
		self.echoCmd = False #old
		# indicates if an Exception will be raised somwhere
		self.debug_break = False
		self.breakstuff = False #old
		# indicates if the bot will join the channels listed in the config after connect
		self.joinChansOnStart = dojoin
		# indicates if extensions will handle msgs, True if so, False otherwise
		self.handleUserMsg = True
		self.handleServerMsg = True 
		self.doMsgHandle = doMsgHandle	#old #if True extensions are executed 
		# holds fake msg. used to prevent invinite fakesends, {"msg":time.time()}
		self.fakeMsg = {}

		### FILES
		# config file, holds general data about the bot and the connection
		self.configFile = Config(self.botDir + "config.json")
		self.config = self.configFile.data
		
		# passwords
		self.__pswFile = Config("pw.json").data		#the password file where all passwords are stored, i seperated them for easier code sharing :)

		### IRC Client Information
		# current irc nick name of the bot
		self.nick = None
		# previous irc nick name of the bot
		self.oldNick = None
		# identity
		self.identity = self.config["ident"]		#bot's identity
		# realname
		self.realname = self.config["realname"]		#bot's realname
		# use localhost instead of network
		self.localhost = str(self.config["localhost"]).lower() == "true"
		# network address, that is not where the bot connects to
		self.network = self.config["network"]
		# port
		self.port = int(self.config["port"])		#the port the bot connects to
		# indicates if ssl will be used, True if so, False otherwise
		self.ssl = str(self.config["ssl"]).lower() == "true"
		# default greet message, will be PRIVMSGed to channels after join and NOTICEd to the owner
		self.greetMsg = self.config["greetMsg"]
		# default quit message
		self.quitMsg = self.config["quitMsg"]		
		
		# phrases searched for in all messages, False if not found, complete line otherwise
		self.search = {}	#phrases the bot listens to. if found the complete line will be put as value
		# uhh uhhm
		self.chans = {}		#information returned to a names request
		# heehee
		self.users = {}		#information returned to a who request

		### re PATTERN JUNGLE MESS
		# every message line the client receives will be split on these
#		self.patServerMsg = re.compile(r":(?P<all>((?P<server>[a-z0-9.-]+)\s(?P<reply>\d+|PONG)\s(?P<nick>\w+)(?:[= ]+)?(?P<target>#?\w+)?)(?:[\s: ]*)(?P<suffix>.*))(?P<hostmask>)(?P<hgl>)(?P<cmd>)(?P<args>)", re.I)
		self.patUMPre = re.compile(r":((?P<nick>\w+)!~?(?P<hostmask>[a-z0-9.@-]+)\s(?P<type>\w+)[\s:]+(?P<target>#?[a-zA-Z0-9-]+))(?:\s:)(?P<suffix>.*)", re.I)
		self.patUMPre = re.compile(r":((?P<ident>(?P<nick>[a-zA-Z0-9]+)!~?(?P<hostmask>[a-z0-9.@-]+))\s(?P<type>\w+)[\s:]+(?P<target>#?[\w-]+))(?:\s:)(?P<suffix>.*)", re.I)

		self.patServerMsg = re.compile(r":(?P<all>((?P<server>[a-z0-9.-]+)\s(?P<reply>\d\d\d|\w+)\s(?P<nick>[a-z0-9.-]+)\s(?P<suffix>.*)))(?P<target>)(?P<hostmask>)(?P<hgl>)(?P<cmd>)(?P<args>)", re.I)
		self.patUMnorm = re.compile(r"(?:(?P<hgl>\w+):\s)?(?P<cmd>[,.:;?!]\w+)\s?(?P<args>.*)(?P<reply>)(?P<server>)", re.I)
		self.patUMnorm = re.compile(r"(?:(?P<hgl>\w+):\s)?((?P<cmdPref>[,.:;?!])(?P<cmd>\w+)\s?)?(?P<args>.*)(?P<reply>)(?P<server>)", re.I)
		self.patMsgWHO = re.compile(r"~?(?P<ident>\w+)\s(?P<ip>[a-z0-9\.\-]+)\s(?P<server>[a-z0-9.-]+)\s(?P<nick>\w+)\s(?P<away>H|G)(?P<registered>r?)(?P<bot>B?)(?P<prefix>\*?[%~+@&]?)\s(?P<steps>:[0-9])\s(?P<realname>.*)", re.I)
		self.patNoneMsg = re.compile(r"((?P<nick>)(?P<hostmask>)(?P<type>)(?P<target>))(?P<suffix>(?:(?:(?P<hgl>))(?P<cmd>)(?P<args>))?)(?P<reply>)(?P<server>).*?", re.I)
		self.patUMvoid = re.compile(r"(?P<hgl>)(?P<cmd>)(?P<args>)(?P<reply>)(?P<server>).*", re.I)

		#self.patUMnorm = re.compile(r"(?:(?P<hgl>\w+):)?\s?(?P<cmd>:\S*)\s?(?P<args>.*)(?P<reply>)(?P<server>)", re.I)
		#self.patUserMsg = re.compile(r":((?P<nick>\w+)!~?(?P<hostmask>[a-z0-9.@-]+)\s(?P<type>\w+)[\s:]*(?P<target>#?\w+))(?:\s:)?(?P<omnom>\([#O]\)<\w+>)\s?(?P<suffix>(?:(?P<hgl>\w*):)*\s?(?P<cmd>\S*)\s?(?P<args>.*))(?P<reply>)(?P<server>)", re.I)



		# Handler
		self.handler = []

		self.plH_user = PluginHandler(dataDir=self.botDir, bot=self)
		self.handler.append(self.plH_user)

		self.plH_server = PluginHandler(dataDir=self.botDir, bot=self)
		self.handler.append(self.plH_server)

		if self.localhost:
			temp = "127.0.0.1" #not working
		else:
			temp = self.config["network"]

		self.sH_irc = SocketHandler(temp, self.port, self.buffer, self.encoding, self.ssl)
		self.handler.append(self.sH_irc)
		
		
		for plName in self.config["plugins"]["user"]:
			try:
				self.plH_user.addPlugin(plName)
			except:
				error()

		for plName in self.config["plugins"]["server"]:
			try:
				self.plH_server.addPlugin(plName)
			except:
				error()

		### THREADS
		self.thread_connect = threading.Thread(None, self.connect, "connect")				#thread for the connect function
		#self.thread_recv = threading.Thread(None, self.receive, "receive")					#thread for the receive function
		self.thread_handle = threading.Thread(None, self.handle, "handle")					#thread for the message handling function
		self.thread_detectTimeout = threading.Thread(None, self.detectTimeout, "dTimeout")	#thread for the Ping Timeout detection
		#self.thread_consInp = threading.Thread(None, self.handle_consInp)
		

		signal.signal(signal.SIGINT, self.handle_keybInt)		


	def run(self):
		# this function is called when the bot starts
		# error detection/handling and other stuff
		self.thread_connect.start()
		self.thread_handle.start()
		self.thread_detectTimeout.start()
		self.plH_user.start()
		self.plH_server.start()
		#self.thread_consInp.start()
		while not self._stopnow:
			try:
				if self.debug_break:
					self.debug_break = False
					raise I_like_trains
				if self.sH_irc.failed:
					self.failed = True
					self.failinfo.insert(0, self.sH_irc.failinfo)

				if self.failed:
					echo(self.failinfo[0], "warn")
					self.connected = False
					
					echo("closing connection")
					self.sH_irc.stop()

					echo("clearing queues")
					self.plH_user.q.queue.clear()
					self.sH_irc.q.queue.clear()
					
					echo("deleting socket and threads")
					del self.sH_irc
					del self.thread_connect

					echo("recreating socket and threads")
					self.sH_irc = SocketHandler(self.config["ipconnect"], self.port, self.buffer, self.encoding, self.ssl)
				
					self.thread_connect = threading.Thread(None, self.connect, "connect")
					self.failed = False

					echo("waiting 21 seconds")
					time.sleep(21)
					
					echo("reconnecting NOW")
					self.thread_connect.start()

				if self._stopnow == True:
					break
				time.sleep(0.42)

			except Exception as e:
				echo(traceback.format_exc(), "warn")
				time.sleep(4)
				return

		echo("waiting for threads to stop...")
		
		for h in self.handler:
			h.stop()

		for t in threading.enumerate():
			try:
				omitted = False
				if t.ident == None:
					omitted = "not started"
				elif t == threading.main_thread():
					omitted = "main thread"
				elif t == threading.current_thread():
					omitted = "current thread"
				elif t.daemon:
					omitted = "daemon"

				if omitted:
					echo("omitted {omitted} thread {thread}".format(thread=t.name, omitted=omitted))
				else:
					echo("joining thread {thread}".format(thread=t.name))
					t.join(5)
					if t.is_alive():
						echo("thread {thread} did not exit within 5 seconds!".format(thread=t.name))
					else:
						echo("thread {thread} exited!".format(thread=t.name))
			except:
				echo(traceback.format_exc(), "warn")

		echo("all threads stopped!")
		echo("exiting in 2 seconds")
		time.sleep(2)
		Echo.end(SCREEN)
		return
				 
	def detectTimeout(self):
		#this function detects ping timouts and pings the server regulary
		while not self._stopnow:
			while not self.connected:
				if self._stopnow:
					return
				time.sleep(1)

			try:
				for i in range(0, self.pingFrequency):
					if self._stopnow:
						return
					time.sleep(1)
					
				pingStr = randStr(10).upper() + "-" + self.nick
				self.sendRaw("PING :" + pingStr, verbose = self.logPingPong)
				pong = self.waitFor(":%s PONG %s :%s" % (self.network, self.network, pingStr), timeout = self.maxPingTimeout, verbose = False)
				
				if type(pong) is float: # or type(pong) is int:
					temp = "pingtimeout! %s" % pong
					echo(temp, "warn")
					self.failed = True
					self.failinfo.insert(0, {"type":"PingTimeout: " + str(pong), "time":time.time()})

			except:
				echo(traceback.format_exc(), "warn")

	def handle(self):
		# this function is for message handling

		while not self._stopnow:
			# sleep when nothing to do
			try:
				if self.sH_irc.q.empty():
					time.sleep(0.1)
				else:
					line = self.sH_irc.q.get()

					# search
					for item in self.search:
						if line.find(item) != -1:
							self.search[item] = line
					
					if re.match(self.patUMPre, line) != None:
						echo(line, "recv")
						msg = re.match(self.patUMPre, line).groupdict()
						try:
							msg.update(re.match(self.patUMnorm, msg["suffix"]).groupdict())
						except:
							msg.update(re.match(self.patUMvoid, "blah").groupdict())

						# replace None with "" and strip spaces
						for item in msg:
							if msg[item] == None:
								msg[item] = ""
							else:
								msg[item] = msg[item].strip()

						if self.connected and self.doMsgHandle:
							# lowercase ident only
							msg["ident"] = msg["ident"].lower()

							author = msg["nick"].lower()+"!"+msg["hostmask"].lower()
							fromOwner = msg["ident"] == self.config["owner"].lower()

							if msg["args"].find(" ") != -1:
								args = msg["args"].split()		#make a list out of the arguments
							
							elif msg["args"] == "":
								args = []
							
							else:
								args = [msg["args"]]
							
							# defines response target, author as target it private chat, channel otherwise
							if self.nick.lower() == msg["target"].lower():
								target = msg["nick"]
							else:
								target = msg["target"]


							# detects if the bot is addressed directly
							nickHgl = str.lower(msg["hgl"]) == self.nick.lower() 

							self.plH_user.q.put({"msg":msg, "args":args, "target":target, "fromOwner":fromOwner, "nickHgl":nickHgl, "line":line})
							self.sH_irc.q.task_done()

					elif re.match(self.patServerMsg, line) != None:
						msg = re.match(self.patServerMsg, line).groupdict()
						if self.logPingPong == False and msg["reply"] in ["PING", "PONG"]:
							pass
						else:
							echo(line, "recv")
						
						self.plH_server.q.put({"msg":msg})
						self.sH_irc.q.task_done()
					else:
						msg = re.match(self.patNoneMsg, line).groupdict()
						echo(line, "recv")
						if line.find("PING") != -1:	#Ping request response thing
							self.sendRaw("PONG {}\r\n".format(".".join(line.split()[1:3])))

						self.sH_irc.q.task_done()
			except:
				error()

	def error(self, target=False, info=""):
		tb = traceback.format_exc()
		echo(tb, "warn")
		echo("info:" + info, "warn")
		self.sendowner(tb.splitlines()[-1])
		if self.connected and target:
			self.privmsg(target, tb.splitlines()[-1])

	def botdo(self, action, *args, **kwargs):
		retvar = True
		try:
			with open("botdo.py") as f:
				exec(f.read(), globals(), locals())
		except:
			error()
			return retvar

	def sendowner(self, msg):
		self.notice(self.config["owner"].split("!")[0], msg)

	def connect(self):
		# function for connection to the server and handshaking, #TODO recheck
		def tryNick():
			for temp in self.config['nick']:
				if self.oldNick == None:
					if self.ison(temp) == False:
						self.changeNick(temp)

		nickServ = self.config["nickserv"] != ""
		quotePass = self.config["quotepass"] != ""
		firstMsg = self.config["firstMsg"]
		self.nick = self.oldNick = None

		self.sH_irc.start()
		time.sleep(0.42)

		self.changeNick(self.config['nick'][0])
		#self.changeNick(randStr(10))
		self.sendRaw("USER %s %s %s %s\r\n" % ("nBot","youwishyoudknow",self.serverName, self.realname))
		# self.waitFor(firstMsg, timeout = 5)

		i = 1
		while not self._stopnow:
			wait = self.waitFor("001", 2.1)
			if type(wait)is float:
				if i < len(self.config["nick"]):
					self.changeNick(self.config["nick"][i])
					i += 1
				else:
					echo("all nicks taken", "warn")
					self._restart = False
					self._stopnow = True
					return
			else:
				break

		if quotePass:
			self.sendRaw("PASS {username}:{password}".format(username=self.config["quotepass"], password=self.__pswFile[self.serverName][self.config["quotepass"]]))		

		if nickServ:
			self.sendRaw("PRIVMSG nickServ :identify %s %s\r\n" % (self.config["nickserv"], self.__pswFile[self.serverName][self.config["nickserv"]]))
			self.waitFor(":+r")
		
		if self.oldNick == None and nickServ and False:
			self.privmsg("nickServ", "ghost " + self.config["nick"][0] + " " + self.__pswFile[self.serverName][self.config["nickserv"]])
			waitFor(nickServ)
			self.changeNick(self.config["nick"][0])

		for mode in self.config["modes"]:
			self.sendRaw(":%s MODE %s :%s\r\n" % (self.nick, self.nick, mode))

		for chans in self.config["channel"]:
			self.join(chans)
		
		echo("connected!")
		self.connected = True

	def sendRaw(self, msg, pref = "send", verbose = True):
		if verbose == True:
			echo(msg, pref)
		elif verbose == False:
			pass
		else:
			echo(verbose, pref)

		try:
			msg = str(msg).replace("\r", "").replace("\n", "") + "\r\n"
			self.sH_irc.send(msg)
			#self.sH_irc.send(bytes(msg, self.encoding))
		except Exception as e:
			if e is BrokenPipeError:
				echo("brokenPipe!", "warn")
				self.brokenPipe = True
			elif e is ConnectionResetError:
				echo("connectionReset", "warn")
				self.connectionReset = True
			echo(traceback.format_exc(), "warn")
			
	def join(self, chan, msg = ""):
		if chan[0] == "_":
			pass
		elif chan[0] == "#":
			self.sendRaw("JOIN :%s\r\n" % (chan))
			self.chans[chan] = {}
			self.who(chan)
		else:
			self.notice(chan)

	def part(self, chan):
		self.sendRaw("PART %s\r\n" % chan)
		self.chans[chan] = {}

	def fakesend(self, line):
		if line in self.fakeMsg:
			if time.time() - self.fakeMsg[line] < 4.2:
				return False
		self.fakeMsg[line] = time.time()
		echo("resending '"+line+"'")
		self.sH_irc.q.put(line)
	
	def privmsg(self, target, msg = "Hey!"):
		self.sendRaw("PRIVMSG %s :%s\r\n" % (target, msg))

	def notice(self, target, msg = "Hey!"):
		self.sendRaw("NOTICE %s : %s\r\n" % (target, msg))

	def ison(self, nick):
		self.sendRaw("ISON :%s\r\n" % (nick))
		data = self.waitFor(" 303 ")
		if type(data) is not str:
			retVar = False
		else:
			retVar = data.lower().find(nick.lower()) != -1
		return retVar

	def changeNick(self, nick):
		self.oldNick = self.nick
		self.sendRaw("NICK %s \r\n" % (nick))
		self.nick = nick

	def waitFor(self, key, timeout = 4.2, verbose = True):
		if verbose:
			echo("waiting for %s" % (key))
		if not key in self.search:
			self.search[key] = False
	
		startTime = time.time()
		endTime = startTime + timeout
		passedTime = 0
		while passedTime < timeout and not self._stopnow:
			if self.search[key] != False:
				ret = self.search[key]
				del self.search[key]
				if verbose:
					echo("'%s' found!" % (key))
				return ret
			passedTime = time.time() - startTime
		if verbose:
			echo("timeout %s: '%s'" % (passedTime, self.search[key]))
		del self.search[key]
		return float(passedTime)

	def count(self, start, stop, delay, *, msg = "counter: {}" , pref = "info", freq = 1, formats):
		if freq == 0:
			freq = 1
		elif freq < 0 and start < stop or freq > 0 and start > stop:
			freq = -freq
		
		for i in range(start, stop, freq):
			echo(msg.format(i, **formats), pref)
			time.sleep(delay)

	def who(self, target):
		self.sendRaw("WHO %s\r\n" % (target))

	def task(self, *commands, waitfor=None):
		if waitfor != None:
			self.waitFor(waitfor)
		for c in commands:
			try:
				exec(c, globals(), locals())
			except Exception as e:
				echo(traceback.format_exc(), "warn")

	def handle_keybInt(self, *args):
		echo("KeyboardInterrupt", "warn")
		echo(args, "warn")
		self.exit(restart = False, reason = "manual shutdown")#(quitDelay = 1, stopDelay = 0)
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		
	def handle_resize(self, *args):
		w,h = self.getTerminalSize_linux()
		LogOutp.win.resize(h,w)
		SCREEN.resize(h,w)
		curses.resizeterm(h,w)
		LogOutp.height = h - 1
		LogOutp.width = w - 1
		LogOutp.refr()

	def shutdown(self, *, reason = None, restart = None, stopDelay = 1, quitDelay = 1):
		if reason == None:
			reason = self.quitMsg
		
		if restart == None:
			restart = self._restart
		else:
			restart = str(restart).lower() == "true"

		self.willStop = True
		thread_exit = threading.Thread(target = self.exit, name = "exit", args = (), kwargs = {"stopDelay": stopDelay, "quitDelay": quitDelay, "reason": reason, "restart": restart})
		thread_exit.start()

	def exit(self, *, reason = "bye", restart = None, **kwargs):
		if restart != None:
			self._restart = str(restart).lower() == "true"

		self._stopnow = True
		self.sendRaw("QUIT %s" % (reason))
		self.connected = False
		time.sleep(0.5)
		self.sH_irc.s.close()

	def getTerminalSize_linux(self):	#I copied this from: http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
		def ioctl_GWINSZ(fd):
			try:
				import fcntl, termios, struct, os
				cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,'1234'))
			except:
				return None
			return cr
		cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
		if not cr:
			try:
				fd = os.open(os.ctermid(), os.O_RDONLY)
				cr = ioctl_GWINSZ(fd)
				os.close(fd)
			except:
				pass
		if not cr:
			try:
				cr = (env['LINES'], env['COLUMNS'])
			except:
				return None
		return int(cr[1]), int(cr[0])

if __name__ == "__main__" and False:
	exec(open("omnimaga/extensions/echo.py").read(), globals(), locals())
	e = Extension()
	e.handle()
	sys.exit()
	restart = True
	while restart == True:
		server = IRCServer("config.json",str(sys.argv[1]))
		server.start()
		while server.is_alive():
			time.sleep(2)
		if server.restart:# and not self.end and not self.allowRestart or self._restartOnExc:
			restart = True
			del server
			print("restart in 2 seconds")
			time.sleep(2)
			print("restarting now...")
		else:
			restart = False
			print("exiting...")

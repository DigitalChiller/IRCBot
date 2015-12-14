#!/usr/bin/python3

#TODO: add CMD 'Okieee :D'

import traceback, json, socket, time, re, chardet, random, threading, queue, pprint, sys

#debugMode = True #indicates debugmode
#encoding = 'UTF-8'

class Output():
	def __init__(self, defaultPref = None, debugMode = True, file = None):
		#super(Output, self).__init__()
		if file != None and False:
			self.historyFile = DataFile(historyFile)
			self.history = self.historyFile.data
		else:
			self.history = None

		self.warn = "\033[1m\033[31m\033[40m(warn)\033[0m "
		self.norm = "\033[1m\033[96m\033[40m(info)\033[0m "
		
		self.debugMode = debugMode

		if defaultPref == None:
			self.pref = self.norm
		else:
			self.pref = defaultPref


	def echo(self, msg, pref = None, *, printEnd = None, fancy = True, dpth = None, cmpct = False):
		if pref == None:
			pref = self.pref
		if type(msg) is not str:
			msg = str(msg).replace("\r", "")
		if msg != "":
			if fancy:
				try:
					#temp = msg.replace("'", '"')
					temp = json.loads(msg)
					temp = pprint.PrettyPrinter(compact = cmpct, depth = dpth).pformat(msg)
					temp = str(msg.replace("\n", "\n" + pref))
					msg = temp
				except Exception as e:
					pass
			msg = msg.rstrip("\n")
			print(str(pref) + str(msg) + "\033[0m", end = printEnd)#.replace("\n", "\033[0m\n"))
			if self.history != None:
				self.history += str(pref) + str(msg) + "\033[0m"
				self.historyFile.save()
			#print("\033[0m")
		return

class DataFile():
	"""docstring for DataFile"""
	def __init__(self, fileName):
		#super(DataFile, self).__init__()
		self.echo = Output(debugMode = True)
		if type(fileName) is not str:
			return False
		self.fileName = fileName
		self.fileType = fileName.split(".")[1]
		self.readFile()
		return
	
	def __repr__(self):
		return self.fileName

	def readFile(self):
		with open(self.fileName) as f:
			if self.fileType == "json":
				lines = f.readlines()
				data = json.loads("\n".join(lines))
			elif self.fileType == "py":
				data = compile(f.read(), self.fileName, "exec")
			else:
				data = f.read()
		self.data = data
		return self.data

	def save(self):
		with open(self.fileName, "w") as f:
			try:
				if self.fileType == "json":
					json.dump(self.data, f, indent = 4)
				else:
					f.write(self.data)
			except Exception as e:
				self.echo(e, Output.warn)
				return False
			else:
				return True
		if self.fileType == "json" and False:
			self.echo("error: %s is not a json file" % (self.fileName), "(log!) ")
			return False
		elif self.data == False:
			self.echo("error: %s something enexpected happend!", "(log!) ")
			return False

class PluginHandler():
	"""docstring for PluginHandler"""
	def __init__(self):
		#super(PluginHandler, self).__init__()
		self.echo = Output(debugMode = True, defaultPref = "\033[1m\033[97m\033[40m(pLog)\033[0m ").echo
		self._plugins = {
			"timed": [],
			"msg": []
		}
		

	def addFromJson(self, json):
		for plType in self._plugins:
			if plType in json:
				for p in json[plType]:
					if type(p) is str:
						self.add(p, plType, True)
					else:
						self.add(p.fileName, plType, True)

	def add(self, fileNamePath, plType, quiet = False):
		if plType in self._plugins:
			f = DataFile(fileNamePath)
			self._plugins[plType].append(f)
			if not quiet:
				self.echo("added %s plugin: %s" % (plType, fileNamePath))

	def rem(self, fileNamePath, plType):
		if plType in self._plugins:
			for p in self._plugins[plType]:
				if fileNamePath == p.fileName:
					self._plugins[plType].remove(p)
					self.echo("removed %s plugin: %s" % (plType, p))

	def reloadPlugins(self, plType = None):
		if plType == None:
			pluginList = self._plugins
			self._plugins = {
				"timed": [],
				"msg": []
			}
			self.addFromJson(pluginList)
		elif plType in self._plugins:
			pluginList = self._plugins[plType]
			self._plugins[plType] = []
			temp = []
			temp.append(pluginList)
			self.addFromJson(temp)

	def execPlugins(self, plType, gl, lc):
		if plType in self._plugins:
			for p in self._plugins[plType]:
				try:
					exec(p.readFile(), gl, lc)
				except Exception as e:
					self.echo("error when executing %s plugin: %s" % (plType, p))
					self.echo(traceback.format_exc(), "\033[1m\033[31m(exce)\033[0m")

class IRCServer(threading.Thread):
	"""docstring for IRCServer"""
	def __init__(self,config, name, *, output = Output(debugMode = True, defaultPref = "\033[1m\033[96m\033[40m(log )\033[0m ").echo, doHandle = True, buffer = 4096, encoding = 'UTF-8'):
		super(IRCServer, self).__init__()
		
		self.echo = output
		self.echo("-----SETTING UP EVERYTHING-----")
		
		self.connected = False
		self.stop = False
		self.restart = True

		self.serverName = name
		self.doHandle = doHandle
		self.name = name
		self.buffer = buffer
		self.encoding = encoding
		self.nick = self.oldNick = None

		self.configFile = DataFile(config)
		self.config = self.configFile.data["server"][name]

		self.__pswFile = DataFile("pw.json").data
		

		#self.userchanFile = DataFile("userchanlist.json")
		#self.users = self.userchanFile.data["users"] = {}
		#self.chans = self.userchanFile.data["chans"] = {}
		#self.userchanFile.save()

		self.identity = self.config["ident"]
		self.network = self.config["network"]
		self.port = self.config["port"]
		self.quitMsg = self.config["quitMsg"]

		self.data = ""		#everything received from the server
		self.preR = "\033[1m\033[93m\033[40m[recv]\033[0m " #36
		self.preS = "\033[1m\033[95m\033[40m[send]\033[0m "
		self.echoPiong = False
		self.lines = []
		self.search = {}
		self.chans = {}
		self.users = {}

		self.patServerMsg = re.compile(r":(?P<all>((?P<server>[a-z0-9.-]+)\s(?P<reply>\d+)\s(?P<nick>\w+)(?:[= ]+)?(?P<target>#?\w+)?)(?:[\s: ]*)(?P<suffix>.*))", re.I)
		self.patUserMsg = re.compile(r":((?P<nick>\w+)!(?P<hostmask>[a-z0-9.@-]+)\s(?P<type>\w+)[\s:]*(?P<target>#?\w+))(?:\s:)?(?P<suffix>(?:(?P<hgl>\w*):)*\s?(?P<command>\S*)\s?(?P<args>.*))", re.I)
		self.patMsgWHO = re.compile(r"(?P<ident>\w+)\s(?P<ip>[a-z0-9\.\-]+)\s(?P<server>[a-z0-9.-]+)\s(?P<nick>\w+)\s(?P<away>H|G)(?P<registered>r?)(?P<bot>B?)(?P<change>\*?)(?P<prefix>[%~+@&]?)\s(?P<steps>:[0-9])\s(?P<realname>.*)", re.I)

		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Define  IRC Socket

		self.plHandler = PluginHandler()
		self.plHandler.addFromJson(self.config["plugins"])
		self.thread_connect = threading.Thread(None, self.connect)
		self.thread_recv = threading.Thread(None, self.receive)
		self.handleLines = queue.Queue()

	def connect(self):

		def randStr(length):
			temp = ''
			for i in range(length):
				temp = temp + random.choice('abcdefghijklmnopqrstuvwxyz')
			return temp		

		def tryNick():
			for temp in self.config['nick']:
				if self.oldNick == None:
					if self.ison(temp) == False:
						self.changeNick(temp)

		nickServ = self.config["nickserv"] != 0
		
		self.server.connect((self.network,self.port)) #connect to the server
		self.server.recv(self.buffer) #Setting up the Buffer

		self.thread_recv.start()

		self.changeNick(randStr(10))
		self.waitFor("PING :")

		self.sendRaw("USER %s %s %s %s\r\n" % (self.identity,'omnimaga',self.serverName, "I_like_trains"))
		self.waitFor("001")

		tryNick()

		if nickServ:
			self.sendRaw("PRIVMSG nickServ :identify %s %s\r\n" % (self.config["nickserv"], self.__pswFile[self.serverName][self.config["nickserv"]]))
			self.waitFor(":+r")


		if self.oldNick == None and nickServ:
			self.privmsg("nickServ", "ghost " + self.config["nick"][0] + " " + self.__pswFile[self.serverName][self.config["nickserv"]])
			waitFor(nickServ)
			self.changeNick(self.config["nick"][0])

		for mode in self.config["modes"]:
			self.sendRaw(":%s MODE %s :%s\r\n" % (self.nick, self.nick, mode))
		

		for temp in self.config["channel"]:
			self.join(temp)

		self.connected = True
		return True

	def run(self):
		self.thread_connect.start()
		while not self.stop:#self.is_alive():
			if len(self.lines) == 0:
				time.sleep(0.01)
				#continue
			elif self.lines[0].find("PING :") == 0:
				self.search["PING :"] = self.lines[0]
				self.lines.pop(0)
				time.sleep(0.01)
			else:
				try:
					msg = self.lines[0]

					self.echo(msg, self.preR)

					for item in self.search:
						if msg.find(item) != -1:
							self.search[item] = msg

					if self.connected and self.doHandle and "PING".find(msg) != 0:
						self.plHandler.execPlugins("msg", globals(), locals())
					self.lines.pop(0)
				except:
					self.echo(traceback.format_exc(), Output.warn)
		return

	def receive(self):
		while self.is_alive():
			s = self.server.recv(self.buffer)
			try:
				s = s.decode(encoding)
			except:
				if s != '':
					try:
						s = s.decode(chardet.detect(s)['encoding'])
					except:
						s = 'False'
						pass #nothing changes

			if s.find("PING") == 0: #If PING is Found in the Data
				self.sendRaw("PONG %s\r\n" % (s.split()[1])) #Send back a PONG
				if self.echoPiong:
					self.echo(str(s).split()[1], "(PIONG) ")
			

			for line in s.replace("\r","").split("\n"):
				if line != "":
					self.lines.append(line)

	def isAllowed(self, msg):
		self.authed = False

		author = msg["nick"].lower()+"!"+msg["hostmask"].lower()
		if author not in self.config["permissions"]["users"]:
			#chan admin, default perms
			pass
		else:
			group = self.config["permissions"]["users"][msg["nick"].lower()+"!"+msg["hostmask"].lower()]["group"]
			if "*" in self.config["permissions"]["groups"][group]:
				self.authed = True
			elif msg["command"]:
				pass
		return self.authed


	def sendRaw(self, msg):
		if msg.find("PONG") != 0:
			self.echo(msg, self.preS)
		msg = msg.replace("\r", "").replace("\n", "") + "\r\n"
		self.server.send(bytes(msg, self.encoding))
	
	def join(self, target, msg = ""):
		if type(target) is str:
			temp = [target]
		else:
			temp = target
		for chan in temp:
			if chan[0] != "_":
				if chan[0] == "#":
					self.sendRaw("JOIN :%s\r\n" % (chan))
					self.chans[chan] = []
					self.who(chan)
				else:
					self.privmsg(chan)

	def part(self, target):
		if type(target) is str:
			leave = [target]
		else:
			leave = target
		for chan in leave:
			self.sendRaw("PART %s\r\n" % chan)
			if chan in self.chans:
				del self.chans[chan]

	def privmsg(self, target, msg = "Hey!"):
		self.sendRaw("PRIVMSG %s :%s\r\n" % (target, msg))

	def notice(self, target, msg = "Hey!"):
		self.sendRaw("NOTICE %s : %s\r\n" % (target, msg))

	def ison(self, nick):
		self.sendRaw("ISON :%s\r\n" % (nick))
		data = self.waitFor(" 303 ")
		retVar = data.lower().find(nick.lower()) != -1
		return retVar

	def changeNick(self, nick):
		self.oldNick = self.nick
		self.sendRaw("NICK %s \r\n" % (nick))
		self.nick = nick

	def waitFor(self, key):
		self.echo("waiting for %s" % (key))
		if not key in self.search:
			self.search[key] = False
		while self.search[key] == False:
			time.sleep(0.01)
		ret = self.search[key]
		self.echo("'%s' found!" % (key))
		del self.search[key]
		return ret

	def who(self, target):
		self.sendRaw("WHO %s\r\n" % (target))

	def shutdown(self, *, quitMsg = None, restart = True, delay = 2):
		self.restart = restart.lower() == "true"
		#timev
		if quitMsg == None:
			quitMsg = self.quitMsg
		
		thread_exit = threading.Thread(target = self.exit, name = "exit", args = (), kwargs = {"delay": delay, "quitMsg": quitMsg, "restart": restart})
		#self.runnignThreads.append(thread_exit)
		thread_exit.start()

	def exit(self, *, delay, quitMsg, restart, **kwargs):
		#startTime = int(time.time())
		remainingTime = int(delay)

		while not remainingTime <= 0:
			if self.stop:
				return
			remainingTime -= 10# round(time.time(), 0) - startTime
			self.echo("going down in %s!" % remainingTime)
			time.sleep(10)

		self.sendRaw("QUIT %s" % (quitMsg))
		self.stop = True

if __name__ == "__main__":
	omni = IRCServer("config.json","omnimaga")
	omni.start()
	while omni.is_alive():
		time.sleep(2)
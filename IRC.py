#!/usr/bin/python3

#TODO: add CMD 'Okieee :D'

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

class File():
	"""
	This calss is for easier File handling.
	"""
	def __init__(self, filePath, fileName, *, echo = print):

		self.echo = echo
		if type(fileName) is not str:
			return False
		self.fileName = fileName
		self.filePath = filePath
		self.fileType = fileName.split(".")[1]
		self.readFile()
		return
	
	def __repr__(self):
		return self.filePath + self.fileName

	def __str__(self):
		return "'" + self.filePath + self.fileName + "'"

	def readFile(self):
		with open(self.filePath + self.fileName) as f:
			if self.fileType == "json":
				lines = f.readlines()
				data = json.loads("\n".join(lines))
			elif self.fileType == "py":
				data = compile(f.read(),self.filePath + self.fileName, "exec")
			else:
				data = f.read()
		self.data = data
		return self.data

	def save(self):
		try:
			f = open(self.filePath + self.fileName, "w")
			if self.fileType == "json":
				json.dump(self.data, f, indent = 4)
			else:
				f.write(self.data)
			f.close()
		except Exception as e:
			f.close()
			self.echo(traceback.format_exc(), "warn")
			return False
		else:
			return True

class ExtensionHandler():
	"""
	this class is for easier extension Handeling
	"""
	def __init__(self, mainPath, fileName, echo = print):
		#super(ExtensionHandler, self).__init__()
		self.mainPath = mainPath
		self.echo = echo
		self.fileName = fileName

		self._extensionsFile = File(self.mainPath, self.fileName, echo = self.echo)
		self._extensions = self._extensionsFile.data
		self._extensionsList = {}
		self.addFromJson()

	def __repr__(self):
		return str(self.extensions)

	def addFromJson(self, filePath = None, fileName = None):
		if filePath != None:
			if fileName != None:
				jsonFile = File(filePath, fileName, echo = self.echo)
				json = jsonFile.data
			else:
				return
		else:
				json = self._extensions

		for extType in json:
			self._extensionsList[extType] = []
			for p in json[extType]:
				try:
					if type(p) is str:
						self.add(self.mainPath, p, extType)
					else:
						self.add(self.mainPath, p.fileName, extType)
				except:
					pass

	def add(self, filePath, fileName, extType, quiet = False):
		try:
			f = File(self.mainPath + extType +"/", fileName)
			for e in self._extensionsList[extType]:
				if str(e) == str(f):
					self._extensionsList[extType].remove(e)
			self._extensionsList[extType].append(f)
			if not str(f.fileName) in self._extensions[extType]:
				self._extensions[extType].append(f.fileName)
				self._extensionsFile.save()
				self._extensions = self._extensionsFile.data
		except Exception as e:
			self.echo(traceback.format_exc(), "warn")
		else:
			self.echo("added extension: '{}/{}'".format(extType, fileName))
	
	def rem(self, fileName, extType, quiet = False):
		for e in self._extensionsList[extType]:
			if e.fileName == fileName:
				self._extensionsList[extType].remove(e)
		if fileName in self._extensions[extType]:
			self._extensions[extType].remove(fileName)
			self._extensionsFile.save()
			self._extensions = self._extensionsFile.data
		if not quiet:
			self.echo("removed extension: '{}/{}'".format(extType, fileName))

	def reloadExtensions(self, extType = None):
		return False
		if extType == None:
			temp = copy.deepcopy(self._extensions)
			self._extensions = {
				"timed": {
					"path": "",
					"extensions": []
				},
				"msg": {
					"path": "",
					"extensions": []
				}
			}
			self.addFromJson(temp)
		elif extType in self._extensions:
			temp = copy.deepcopy(self._extensions[extType])
			self._extensions[extType] = {
				"path": "",
				"extensions": []
			}
			self.addFromJson(temp)

	def listExtensions(self):
		temp = {}
		for extType in self._extensions:
			temp[extType] = self._extensions[extType]
		self.echo(temp, "info", fancy=True)
		self.echo(self._extensionsList, fancy = True)
		return temp

	def execExtensions(self, extType, gl, lc):
		if extType in self._extensionsList:
			for p in self._extensionsList[extType]:
				try:
					exec(p.readFile(), gl, lc)
				except Exception as e:
					self.echo("error when executing %s extension: %s" % (extType, p))
					self.echo(traceback.format_exc(), "warn")


class IRCServer(threading.Thread):
	"""docstring for IRCServer"""
	def __init__(self, name, dojoin = True, *, doMsgHandle = True, buffer = 8192, encoding = 'UTF-8'):
	
		super(IRCServer, self).__init__()
		self.screen = Echo.start()

		self.name = name
		self.path = self.name + "/"

		self.win_log = Echo.ScrollText(scrollback = 200, posy = 0, posx = 0, height = curses.LINES - 1, width = curses.COLS - 1, logFile = self.path+self.name+"-logs.txt")
		self.win_log.addPref("warn", "\r{warn}", curses.color_pair(11)) #these define custom prefixes for the console output
		self.win_log.addPref("ping", "\r(ping)", curses.color_pair(11))	
		self.win_log.addPref("recv", "\r[recv]", curses.color_pair(15))
		self.win_log.addPref("send", "\r[send]", curses.color_pair(16))
		self.win_log.addPref("pipo", "\r[pipo]", curses.color_pair(17))
		
		self.echo = self.win_log.echo
		
		self.echo("-----SETTING EVERYTHING UP-----")

		signal.signal(signal.SIGINT, self.handle_keybInt)		
		signal.signal(signal.SIGWINCH, self.handle_resize)
		
		self.connected = False	#is True when connected to the server, False otherwise
		self.stop = False		#is True when the bot is going down, False when everythings fine
		self.restart = True		#is True when the bot is set to restart, False otherwise

		self.pingTimeout = False		#is False when no Ping Timeout occured, otherwise it holds time in seconds as float
		self.brokenPipe = False			#is False when no Broken Pipe Error occured, True otherwise
		self.connectionReset = False		#is False when no Connection Reset Error occured, True otherwise

		self.doPiong = True				#True when responses to Ping requests from the server
		self.echoPiong = False			#if True PING / PONG messages are logged, False otherwise
		self.maxInactivity = 20			#maximum amount of inactivity until PING request
		self.timeout = 10				#maximum amount of time until a PING Timeout is indicated
		self.doDetectTimeout = True	#if True the bot restarts or shuts down when the bot detects a Ping Timeout
		self.blockMOTD = True 			#if True MOTD is not logged

		self.echoCmd = False			#for debugging, if True it logs the splitted messages received from the server
		self.breakstuff = False			#for debugging, raises somewhere a error

		self.serverName = name			#the name (folder) of the server/bot, each must be unique
		self.joinChansOnStart = dojoin			#if True the bot joins channels on start up
		self.doMsgHandle = doMsgHandle	#if True extensions are executed
		self.buffer = buffer			#the buffer size
		self.encoding = encoding		#prefered encoding\ 

		self.nick = None				#the bot's nick
		self.oldNick = None				#the bot's previous nick

		#=====config file, holds general data about the bot and the connection
		self.configFile = File("", self.name.lower() + ".json", echo = self.echo) 
		self.config = self.configFile.data

		#=====holds which user (<nick>!<identity>@<hostmask>) has what roles
		self.permuserFile = File(self.path, "permuser.json", echo = self.echo)
		self.permuser = self.permuserFile.data

		#===== holds which role has access to which commands
		self.rolesFile = File(self.path, "roles.json", echo = self.echo)
		self.roles = self.rolesFile.data

		self.identity = self.config["ident"]		#bot's identity
		self.realname = self.config["realname"]		#bot's realname
		self.network = self.config["network"]		#the network the bot will be connected to, should be equal to the where the bot connects to. this is usefull when the server is running on the same host (localhost)
		self.port = int(self.config["port"])		#the port the bot connects to
		self.ssl = str(self.config["ssl"]).lower() == "true"	#if True ssl will be used
		self.greetMsg = self.config["greetMsg"]		#the default greet message
		self.quitMsg = self.config["quitMsg"]		#the default quit message
		
		self.__pswFile = File("", "pw.json", echo = self.echo).data		#the password file where all passwords are stored, i seperated them for easier code sharing :)
		
		self.lines = []		#all messages will be stored in this list split in lines
		self.search = {}	#phrases the bot listens to. if found the complete line will be put as value
		self.chans = {}		#information returned to a names request
		self.users = {}		#information returned to a who request

		#every message line the client receives will be split on these
		self.patServerMsg = re.compile(r":(?P<all>((?P<server>[a-z0-9.-]+)\s(?P<reply>\d+|PONG)\s(?P<nick>\w+)(?:[= ]+)?(?P<target>#?\w+)?)(?:[\s: ]*)(?P<suffix>.*))(?P<hostmask>)(?P<hgl>)(?P<cmd>)(?P<args>)", re.I)
		#self.patUserMsg = re.compile(r":((?P<nick>\w+)!~?(?P<hostmask>[a-z0-9.@-]+)\s(?P<type>\w+)[\s:]*(?P<target>#?\w+))(?:\s:)?(?P<omnom>\([#O]\)<\w+>)\s?(?P<suffix>(?:(?P<hgl>\w*):)*\s?(?P<cmd>\S*)\s?(?P<args>.*))(?P<reply>)(?P<server>)", re.I)
		self.patMsgWHO = re.compile(r"~?(?P<ident>\w+)\s(?P<ip>[a-z0-9\.\-]+)\s(?P<server>[a-z0-9.-]+)\s(?P<nick>\w+)\s(?P<away>H|G)(?P<registered>r?)(?P<bot>B?)(?P<prefix>\*?[%~+@&]?)\s(?P<steps>:[0-9])\s(?P<realname>.*)", re.I)
		self.patNoneMsg = re.compile(r"((?P<nick>)(?P<hostmask>)(?P<type>)(?P<target>))(?P<suffix>(?:(?:(?P<hgl>))(?P<cmd>)(?P<args>))?)(?P<reply>)(?P<server>).*?", re.I)
		self.patUMPre = re.compile(r":((?P<nick>\w+)!~?(?P<hostmask>[a-z0-9.@-]+)\s(?P<type>\w+)[\s:]+(?P<target>#?[\w-]+))(?:\s:)(?P<suffix>.*)", re.I)
		#self.patUMnorm = re.compile(r"(?:(?P<hgl>\w+):)?\s?(?P<cmd>:\S*)\s?(?P<args>.*)(?P<reply>)(?P<server>)", re.I)
		self.patUMnorm = re.compile(r"(?:(?P<hgl>\w+):\s)?(?P<cmd>[!:~@#$%^&*()_+?|]?\w*)\s?(?P<args>.*)(?P<reply>)(?P<server>)", re.I)
		self.patUMomnom = re.compile(r"(?:\((?P<omnom>[O#]*)\)<(?P<omnomnick>\w+)>)\s?(?P<suffix>(?:(?P<hgl>\w*):)?\s?(?P<cmd>\S*)\s?(?P<args>.*))(?P<reply>)(?P<server>)", re.I)
		self.patUMvoid = re.compile(r"(?P<hgl>)(?P<cmd>)(?P<args>)(?P<reply>)(?P<server>).*", re.I)

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #the socket the bot uses to connect
		#self.socket.settimeout(10)
		if self.ssl:
			self.socket = ssl.wrap_socket(self.socket)					#make the socket ssl

		#the handler for the extensions
		self.extHandler = ExtensionHandler(mainPath = self.path, fileName = "extensions.json", echo = self.echo)
		
		self.thread_connect = threading.Thread(None, self.connect, "connect")				#thread for the connect function
		self.thread_recv = threading.Thread(None, self.receive, "receive")					#thread for the receive function
		self.thread_handle = threading.Thread(None, self.handle, "handle")					#thread for the message handling function
		self.thread_detectTimeout = threading.Thread(None, self.detectTimeout, "dTimeout")	#thread for the Ping Timeout detection
		#self.thread_consInp = threading.Thread(None, self.handle_consInp)

	def receive(self):			#function for receiving and decoding messages, original: github.com/Sorunome/OmnomIRC/blob/master/irc/bot.py#L47-L56
		while not self.stop:
			s = self.socket.recv(self.buffer)
			try:				#trying to decode the message
				s = s.decode(self.encoding)
			except:
				if s != '':
					try:
						s = s.decode(chardet.detect(s)['encoding'])
					except Exception as e:
						if e is BrokenPipeError:
							self.echo("brokenPipe!", "warn")
							self.brokenPipe = True
						elif e is ConnectionResetError:
							self.echo("connectionReset", "warn")
							self.connectionReset = True
						self.echo(traceback.format_exc(), "warn")
						s = "."
						time.sleep(4)

			if s.find("PING") == 0 and self.doPiong:	#Ping request response thing
				self.sendRaw("PONG {}\r\n".format(".".join(s.split()[1:3])))
				if self.echoPiong:
					self.echo(str(s).split()[1], "pipo")
			

			for line in s.replace("\r","").split("\n"):		#split received messages by new lines and put them into self.lines
				if line != "":
					self.lines.append(line)

	def run(self):	#this function is called when the bot starts, it does error detection and stuff
		self.thread_connect.start()
		self.thread_handle.start()
		self.thread_detectTimeout.start()
		#self.thread_consInp.start()
		while not self.stop:
			try:
				if self.breakstuff:
					self.breakstuff = False
					raise I_like_trains
				if self.brokenPipe != False or self.pingTimeout != False:
					self.echo("Broken Pipe: {}".format(self.brokenPipe), "warn")
					self.echo("PingTimeout: {}".format(self.pingTimeout), "warn")
					self.echo("exiting...", "warn")
					self.exit()
					self.echo("reconnecting in 10 seconds")
					time.sleep(4)
				if self.stop == True:
					break
				time.sleep(0.42)

			except Exception as e:
				self.echo(traceback.format_exc(), "warn")
				time.sleep(4)
				return

		self.echo("waiting for threads to stop...")

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
					self.echo("omitted {omitted} thread {thread}".format(thread=t.name, omitted=omitted))
				else:
					self.echo("joining thread {thread}".format(thread=t.name))
					t.join(5)
					if t.is_alive():
						self.echo("thread {thread} did not exit within 5 seconds!".format(thread=t.name))
					else:
						self.echo("thread {thread} exited!".format(thread=t.name))
			except:
				self.echo(traceback.format_exc(), "warn")

		self.echo("all threads stopped!")
		self.echo("exiting in 2 seconds")
		time.sleep(2)
		Echo.end(self.screen)
		return
				 
	def detectTimeout(self):		#this function pings the server regulary
		while not self.connected:	#waits until the bot is connected
			if self.stop:
				return
			time.sleep(1)
		
		i = self.maxInactivity
		while not self.stop:
			if i >= 0:
				i -= 1
				time.sleep(1)
			else:
				i = self.maxInactivity
				
				pingStr = self.randStr(5).upper() + "-" + self.nick
				self.sendRaw("PING :%s" % pingStr, verbose = self.echoPiong)
				pong = self.waitFor(":%s PONG %s :%s" % (self.network, self.network, pingStr), timeout = self.timeout, verbose = False)
				
				if type(pong) is float or type(pong) is int:
					temp = "pingtimeout! %s" % pong
					self.echo(temp, "warn")
					if self.doDetectTimeout:
						self.pingTimeout = pong

	def handle(self):			#this function is for message handling
		while not self.stop:
			if len(self.lines) == 0:
				time.sleep(0.1)
			else:
				line = self.lines[0]
				self.lines.pop(0)
				for item in self.search:
					if line.find(item) != -1:
						self.search[item] = line


				if re.match(self.patUMPre, line) != None:
					msgType = ["user"]
					msg = re.match(self.patUMPre, line).groupdict()

					if msg["nick"].lower() == "omnomirc":
						msg.update(re.match(self.patUMomnom, msg["suffix"]).groupdict())
						msgType.append("omnomirc")
					else:
						try:
							msg.update(re.match(self.patUMnorm, msg["suffix"]).groupdict())
						except:
							msg.update(re.match(self.patUMvoid, "blah").groupdict())

					for item in msg:
						if msg[item] == None:
							msg[item] = ""

					self.echo(line, "recv")						#logging

					if self.connected and self.doMsgHandle:
						authed = self.isAuthed(msg)					#authing
						msg["suffix"] = msg["suffix"].strip() 		#removing all blanks from the beginning and end
						msg["args"] = msg["args"].strip()			#same here
						args = self.strToList(msg["args"], " ")		#make a list out of the arguments
						
						if self.nick.lower() == msg["target"].lower():	#that's for easier responding
							target = msg["nick"]
						else:
							target = msg["target"]

						if msg["hgl"] != None:			#detects nick highlighting
							nickHgl = str.lower(msg["hgl"]) == self.nick.lower() 
						else:
							nickHgl = False

						try:
							self.extHandler.execExtensions("user_msg", globals(), locals())		#execution of extensions
						except:
							self.echo(traceback.format_exc(), "warn")

				elif re.match(self.patServerMsg, line) != None:
					msg = re.match(self.patServerMsg, line).groupdict()
					msgType = ["server"]
					if msg["reply"] in ["PING", "PONG"]:
						if self.echoPiong:
							self.echo(line)						
					elif msg["reply"] == "372" and self.blockMOTD:		#blocks the MOTD if self.blockMOTD is True
						pass
					else:
						self.echo(line, "recv")

					if self.connected and self.doMsgHandle:
						try:
							self.extHandler.execExtensions("server_msg", globals(), locals())		#execution of extensions
						except:
							self.echo(traceback.format_exc(), "warn")

				else:
					msg = re.match(self.patNoneMsg, line).groupdict()
					msgType = ["other"]
					self.echo(line, "recv")

	def connect(self):		#function for connection to the server and doing handshake
		def tryNick():
			for temp in self.config['nick']:
				if self.oldNick == None:
					if self.ison(temp) == False:
						self.changeNick(temp)

		nickServ = self.config["nickserv"] != ""
		quotePass = self.config["quotepass"] != ""
		self.win_log.changeTitle("nBot - connecting")
		firstMsg = self.config["firstMsg"]

		self.socket.connect((self.config["ipconnect"],self.port)) #connect to the server

		self.socket.recv(self.buffer)	#Setting up the Buffer
		self.thread_recv.start()		#start the receive Thread
		
		self.changeNick(self.randStr(10))
		self.waitFor(firstMsg, timeout = 5)

		if quotePass:
			self.sendRaw("PASS {username}:{password}".format(username=self.config["quotepass"], password=self.__pswFile[self.serverName][self.config["quotepass"]]))		

		self.sendRaw("USER %s %s %s %s\r\n" % (self.identity,'omnimaga',self.serverName, self.realname))
		self.waitFor("266")
		
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
		
		self.echo("connected!")
		self.connected = True

	def isAuthed(self, msg):	#authed if author is owner
		authed = False
		author = msg["nick"].lower()+"!"+msg["hostmask"].lower()
		if author == self.config["owner"].lower():
			authed = True
		return authed

	def sendRaw(self, msg, pref = "send", verbose = True):
		if verbose == True:
			self.echo(msg, "send")
		elif verbose == False:
			pass
		else:
			self.echo(verbose, pref)

		try:
			msg = str(msg).replace("\r", "").replace("\n", "") + "\r\n"
			self.socket.send(bytes(msg, self.encoding))
		except Exception as e:
			if e is BrokenPipeError:
				self.echo("brokenPipe!", "warn")
				self.brokenPipe = True
			elif e is ConnectionResetError:
				self.echo("connectionReset", "warn")
				self.connectionReset = True
			self.echo(traceback.format_exc(), "warn")
			
	def join(self, target, msg = ""):
		temp = self.strToList(target)
		for chan in temp:
			chan = chan.strip()
			if chan[0] == "_":
				pass
			elif chan[0] == "#":
				self.echo(self.joinChansOnStart)
				if not self.connected and not self.joinChansOnStart:
					continue
				else:
					self.sendRaw("JOIN :%s\r\n" % (chan))
					self.chans[chan] = {}
					self.who(chan)
			else:
				self.notice(chan)

	def part(self, target):
		leave = self.strToList(target)
		for chan in leave:
			chan = chan.strip()
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
			self.echo("waiting for %s" % (key))
		if not key in self.search:
			self.search[key] = False
	
		startTime = time.time()
		endTime = startTime + timeout
		passedTime = 0
		while passedTime < timeout and not self.stop:
			if self.search[key] != False:
				ret = self.search[key]
				del self.search[key]
				if verbose:
					self.echo("'%s' found!" % (key))
				return ret
			passedTime = time.time() - startTime
		if verbose:
			self.echo("timeout %s: '%s'" % (passedTime, self.search[key]))
		del self.search[key]
		return passedTime

	def count(self, start, stop, delay, *, msg = "counter: {}" , pref = "info", freq = 1, formats):
		if freq == 0:
			freq = 1
		elif freq < 0 and start < stop or freq > 0 and start > stop:
			freq = -freq
		
		for i in range(start, stop, freq):
			self.echo(msg.format(i, **formats), pref)
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
				self.echo(traceback.format_exc(), "warn")

	def handle_keybInt(self, *args):
		self.echo("KeyboardInterrupt", "warn")
		self.echo(args, "warn")
		self.exit(restart = False, reason = "manual shutdown")#(quitDelay = 1, stopDelay = 0)
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		
	def handle_resize(self, *args):
		w,h = self.getTerminalSize_linux()
		self.win_log.win.resize(h,w)
		self.screen.resize(h,w)
		curses.resizeterm(h,w)
		self.win_log.height = h - 1
		self.win_log.width = w - 1
		self.win_log.refr()

	def shutdown(self, *, reason = None, restart = None, stopDelay = 1, quitDelay = 1):
		if reason == None:
			reason = self.quitMsg
		
		if restart == None:
			restart = self.restart
		else:
			restart = str(restart).lower() == "true"

		self.willStop = True
		thread_exit = threading.Thread(target = self.exit, name = "exit", args = (), kwargs = {"stopDelay": stopDelay, "quitDelay": quitDelay, "reason": reason, "restart": restart})
		thread_exit.start()

	def exit(self, *, reason = "bye", restart = None, **kwargs):
		if restart != None:
			self.restart = str(restart).lower() == "true"

		self.stop = True
		self.sendRaw("QUIT %s" % (reason))
		self.connected = False
		time.sleep(0.5)
		self.socket.close()

	def randStr(self, length):
			temp = ''
			for i in range(length):
				temp = temp + random.choice('abcdefghijklmnopqrstuvwxyz')
			return temp	

	def strToList(self, text, sep = ","):
		if type(text) is list:
			return text

		text = text.strip()
		if text == "":
			return []
		elif text.find(sep) == -1:
			return [text]
		else:
			text = text.split(sep)
			for i,item in enumerate(text):
				text[i] = item.strip()
				if text[i] == "":
					text.pop(i)
			return text

	def strToDict(self, text, sep = ",", sep2 = ":"):
		if type(text) is dict:
			return text
		if type(text) is str:
			text = self.strToList(text)	
		dictionary = {}
		#temp = text.split(sep)
		try:
			for item in text:
				t = item.split(sep2)
				dictionary[t[0].strip()] = t[1].strip()
			return dictionary
		except:
			return False


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
	sys.exit()
	restart = True
	while restart == True:
		server = IRCServer("config.json",str(sys.argv[1]))
		server.start()
		while server.is_alive():
			time.sleep(2)
		if server.restart:# and not self.end and not self.allowRestart or self.restartOnExc:
			restart = True
			del server
			print("restart in 2 seconds")
			time.sleep(2)
			print("restarting now...")
		else:
			restart = False
			print("exiting...")
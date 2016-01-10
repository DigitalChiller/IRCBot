#!/usr/bin/python3

import curses, time, traceback, json, pprint, sys, threading, curses.textpad

def start():
	curses.use_env(True)
	screen = curses.initscr()
	curses.start_color()
	curses.use_default_colors()
	curses.cbreak()
	curses.noecho()
	curses.curs_set(0)
	return screen

def end(screen = None):
	if screen != None:
		screen.clear()
		try:
			screen.refresh()
		except:
			pass
	curses.cbreak()
	curses.echo()
	curses.endwin()

class ScrollText():
	p = {
		"none": {
			"text": "",
			"color": 0
		},
		"info": {
			"text": "(info)",
			"color": 3072
		}
	}
	def __init__(self, scrollback = 200, posx = 0, posy = 0, height = 10, width = 20, defType = "info", logFile = None):
		#super(ScrollText, self).__init__()
		self.scrollback = scrollback
		self.posx = posx
		self.posy = posy
		self.height = height
		self.width = width
		self.curserLn = scrollback
		self.defType = defType
		self.doScroll = True
		self.text = []
		self.logFile = logFile

		temp = ""
		temp += "\n"*3
		temp += "="*20
		temp += "-"*20
		temp += "="*20
		temp += "\n"*3
		if logFile != None:
			with open(self.logFile, "a") as f:
				f.write(temp)

		for i in range(0, self.scrollback):
			self.text.append(["none", ""])

		for i in range(0, curses.COLORS):
			curses.init_pair(10+i, i, -1)

		self.win = curses.newwin(self.height, self.width, self.posy,self.posx)
		self.win.scrollok(1)
		self.win.idlok(1)
		self.win.move(self.height - 1, 0)
		threading.Thread(None, self.scroll, "Echo.scroll", daemon = True).start()

	def echo(self, msg, type = None, *, fancy = False, **kwargs):
		try:
			if type == None:
				type = self.defType
			msg = str(msg)
			msg = msg.rstrip("\n")
			msg = msg.replace("\r", "")
			
			if len(msg) > 0:
				if fancy:
					for i in range(0,2):
						try:
							temp = msg
							if i == 1 and False:
								self.echo("WTF HOW COULD THAT HAVE HAPPEND",warn)
								temp = msg.replace("'", '"')		#I keep that just for trolling Sorunome >D
							temp = json.loads(temp)
							temp = pprint.PrettyPrinter(**kwargs).pformat(temp)
							msg = temp
							break
						except Exception as e:
							pass
				text = ""
				for line in msg.split("\n"):
					temp = [type, line]
					text += self.p[type]["text"] + ":" + line + "\n"
					self.text.append(temp)
					self.text.pop(0)
					if self.curserLn >= self.scrollback:
						self.refr()
				if self.logFile != None:
					with open(self.logFile, "a") as f:
						f.write(text)
		except Exception as e:
			temp = traceback.format_exc().replace("\n", "\r\n")
			print("\n" + temp)

	def refr(self):
		try:
			self.win.clear()
			self.win.move(self.height-1, self.posx)
			for line in self.text[self.curserLn - self.height:self.curserLn]:
				self.win.scroll(1)
				self.win.addstr(self.p[line[0]]["text"].replace("\r", "") + " ", self.p[line[0]]["color"] | 2097152)
				self.win.addstr(line[1] + "\r")
			self.win.refresh()
		except:
			temp = traceback.format_exc().replace("\n", "\r\n")
			print("\n" + temp)
			#raise Exception

	def scroll(self):
		while True:
			key = self.win.getch()
			if key == 113:
				self.exit = True
				return
			elif self.curserLn > self.height and key == 65:
				self.curserLn -= 1
				self.refr()
			elif self.curserLn < self.scrollback and key == 66:
				self.curserLn += 1
				self.refr()

	def addPref(self, name, text, color):
		self.p[name] = {}
		self.p[name]["text"] = text
		self.p[name]["color"] = color

	def changeTitle(self, name):
		pass

	def save(self, filePath, fileName):
		with open(filePath + fileName, "a") as f:
			f.write("\n"*2 + "-"*21 + "\n"*2) #two newlines, 21 '-' chars and again two newlines
			t = ""
			for line in self.text:
				if line[0] != "none":
					t += ":".join(line)
					t += "\n"
			f.write(t)

class Input():
	"""docstring for Input"""
	def __init__(self, *, posy = 0, posx = 0, height = 10, width = 42 , afterEdit = False):
		#super(Input, self).__init__()
		self.posy = posy
		self.posx = posx
		self.height = height
		self.width = width
		self.afterEdit = afterEdit
		self.edit = True
		self.str = "!\"#234567890"
		self.str = "ABCDEFGHIJKLMNOPQRSTUFWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz[\]~"
		self.win = curses.newwin(self.height,self.width, self.posy,self.posx)
		self.win.leaveok(1)
		#self.textpad = curses.textpad.Textbox(self.win)

		threading.Thread(None, self.read, daemon = True).start()
	
	def read(self):
		while True:
			if self.edit:
				self.isWriting = True
				ch = self.win.getkey()
				try:
					self.win.addstr(0,10,str(curses.keyname(ord(ch)))+" "*4)
					self.win.addstr(1,10,str((ord(ch)))+" "*4)
					self.win.addstr(2,10,str((ch))+" "*4)
					
					self.win.refresh()
				except Exception as e:
					print(e)
					pass
					#self.win.addstr(0,10,str(int(ord(ch)))+" "*4)
				if self.edit and False:
					self.text = self.textpad.edit()
					self.isWriting = False
					self.win.clear()
					self.win.refresh()
			else:
				sys.exit()
				time.sleep(0.42)

if __name__ == "__main__" and False:
	try:
		start()
		inp = Input()
		while inp.isWriting:
			time.sleep(1)
	except Exception as e:
		raise
	else:
		pass
	finally:
		end()
		print("ur input was:")
		print(inp.text)
		pass
	sys.exit()
	raise KeyboardInterrupt
	try:
		start()	
		log = ScrollText(height = 22, width = 100, posx = 0, posy = 0)
		log.addPref("warn", "{warn}", curses.color_pair(11))
		echo = log.echo
		for i in range(1, 200):
			temp = str(i).zfill(5)
			echo(temp)
			time.sleep(0.5)
			#print(i, end="\r\n")

		while True:
			#log.refr()
			time.sleep(0.42)
		pass
	except Exception as e:
		print(traceback.format_exc().replace("\n", "\r\n"))
	finally:
		end()
		for item in log.text:
			print(item)
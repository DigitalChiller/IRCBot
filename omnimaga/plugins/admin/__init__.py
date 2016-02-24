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

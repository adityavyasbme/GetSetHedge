from src.features.features import Feature

class Custom_indicator(Feature):
	def __init__(self,name,parent,requires = ["Open","Close"]):
		self.name=name
		self.requires = requires
		self.parent = parent
		self.register()

	def indicator(self,data):
	    ans = data
	    ans = ans.rename(columns={"Open": "Feature1", "Close": "Feature3"})
	    return ans

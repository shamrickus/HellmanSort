import urllib2, re, sys
from HTMLParser import HTMLParser

from lxml import html

class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.begin = False
		self.beginA = False
		self.entries = []
		self.curDate = 0

	#Checks if we have a goal div
	def checkMatch(self, tag, clas, attr):
		if(tag == "div" and clas == "class" and re.match(r" *goaldescr goal\-priority\-[0-9].*", attr)):
			return True
		return False

	#Handles start html tags, keeps flags to see if we are currently in an element
	#THIS WILL NOT HANDLE NESTED GOALS
	def handle_starttag(self, tag, attrs):
		if(tag == "div"):
			if(self.checkMatch(tag, attrs[0][0], attrs[0][1])):	
				self.begin = True	
		elif(tag == "a" and attrs[0][0] == "name"):
			self.curDate = attrs[0][1]
		#print "Encountered a start tag:" + tag

	#Handles end html tags, adds entries if we are ending an appropriate tag
	def handle_endtag(self, tag):
		if(tag == "div" and self.begin == True):	
			self.begin = False
	# 	print "Encountered an end tag :", tag

	#This the data inbetween attributes
	def handle_data(self, data):
		if(self.begin == True):
			self.entries.append([data, self.curDate])
	# 	print "Encountered some data  :", data

	#Sorts the entries by date (reverse) to match hellman's site layout
	def sortEntries(self):
		self.entries.sort(key=lambda a: a[1], reverse=True)

	#Gets all the entries in an object
	def getEntries(self):
		ret = []
		self.sortEntries()
		for en in self.entries:
			ret.append(en[0])
		return ret

	#Gets the subset of entries from another object
	def getSubSet(self, entr):
		ret = []
		for ent in self.entries:
			for ent2 in entr:
				if(ent[0] == ent2):
					ret.append(ent)
		return ret

#Strips undefined html attributes and whitespace		
def getFeed(url):
	ret = urllib2.urlopen(url).read().replace("<em>", "").replace("</em>", "").replace("<strong>","").replace("</strong>", "").replace("<code>", "").replace("</code>", "").replace("\n","").replace("\t","")
	return ret


if __name__ == "__main__":
	mhp = MyHTMLParser()
	mhp2 = MyHTMLParser()

	if(len(sys.argv) != 3):
		print "Expects: python hellman.py schedule_page_link, learning_goals_link"
		sys.exit()

	print "Calculating..."

	mhp.feed(getFeed(sys.argv[1]))
	mhp2.feed(getFeed(sys.argv[2]))

	ents = mhp.getSubSet(mhp2.getEntries())

	for ent in ents:
		print ent[0]


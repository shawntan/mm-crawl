
def reward(document):
	doc_text = unicode(document.toPlainText(),errors="ignore")
	if doc_text.find("user:")>=0 and doc_text.find("created:")>=0:
		print doc_text
		return 100
	else: return -10

	"""
	links = document.findAll(".entry a")
	count =0
	for a in links:
		text = str(a.toPlainText())
		if text.find("mediafire.com"): count += 1
	
	if count:return count
	else: return -1
	"""

click_func = """
	var evt = document.createEvent('MouseEvents');
	evt.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
	Element.prototype.click = function() {
		this.dispatchEvent(evt);
	};
	"""

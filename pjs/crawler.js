var fs = require('fs');
var page = new WebPage(),
	url = "http://www.lifehacker.com";


page.onConsoleMessage = function(msg) {
	console.log(msg);
}

page.open(url,function(status){
	if(status !== "success") {
		console.log("Unable to access network");
	} else {
		console.log("retrieved page");
		var links = page.evaluate(function() {
			document.queryDocument = function(xpath) {
				var result = document.evaluate(
						xpath,
						document,null,
						XPathResult.ORDERED_NODE_ITERATOR_TYPE,null);
				if(result) {
					var node,res= [];
					do {
					   	if(node = result.iterateNext()) res.push({
							HTML:	node.outerHTML,
							url:	node.href
						});
					} while(node);
					return res;
				}
			}
			return document.queryDocument("//a");
		});
	
		fs.write('test',page.evaluate(function(){
			return document.documentElement.outerHTML;
		}),'w');
		
	}
});

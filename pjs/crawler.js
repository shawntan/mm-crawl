var fs = require('fs');
var page = new WebPage();

page.onResourceRequested = function (request) {
   // console.log('Request ' + JSON.stringify(request, undefined, 4));
};
page.onResourceReceived = function (response) {
	//console.log('Receive ' + JSON.stringify(response, undefined, 4));
};
page.onConsoleMessage = function(msg) {
	//console.log(msg);
}

function crawlPage(url,fun) {
	var pagecontent,done=false;
	page.open(url,function(status){
		if(status !== "success") {
			console.log("Unable to access network");
		} else if (!done) {
			done=true;
			var results = page.evaluate(function() {
				document.queryDocument = function(xpath) {
					var result = document.evaluate(
							xpath,
							document,null,
							XPathResult.ORDERED_NODE_ITERATOR_TYPE,null);
					if(result) {
						var node,res= [];
						do {
							if(node = result.iterateNext())  res.push(node);
						} while(node);
						return res;
					}
				}

				var links= [],el1 = document.queryDocument("//a");
				for(var i in el1) links.push({
					url: el1[i].href,
					html: el1[i].innerHTML
				});
				var iframes = [],el2= document.queryDocument("//iframe");
				//console.log(el2.length);
				for(var i in el2) if (el2[i].src) iframes.push(el2[i].src);

				return {links:links,iframes:iframes};
			});
			//console.log(links)
			for(var i in results.iframes) console.log(results.iframes[i]);
			//try to see how to load the iframes into divs
			fun( page.evaluate(function(){
				return document.documentElement.outerHTML;
			}) );
		}
	});
	return pagecontent;
}


crawlPage("http://www.lifehacker.com",function(str){/*console.log(str)*/});

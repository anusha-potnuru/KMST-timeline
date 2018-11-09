var articleStyle = {
	color: "#444",
	width: 150,                             
	topRadius: 3,                             
	starMargin: 2,                           
	maxImageHeight: 150,                     
	header: {                                 
		height: 50,                            
		text: {                                   
			font: "normal 14px 'Segoe UI'",       
			color: "#000",                      
			margin: 10,                          
			lineHeight: 18,                      
			numberOfLines: 2                      
		},
	},
	subheader: {                              
		height: 35,                            
		color: "#aaa",
		text: {                                   
			font: "normal 11px 'Segoe UI'",      
			color: "#000",                        
			margin: 10,                           
		}
	},
	shadow: {                                
		x: 0,                                 
		y: 0,                                 
		amount: 0,                            
		color: '#000'                         
	},
	border: {
		color: '#ddd',
		width: 1,
	},
	connectorLine: {                         
		offsetX: 18,                     
		offsetY: -20,
		thickness: 1,
		arrow: {
			width: 16, 
			height: 45 
		}
	}	
}

var articleActiveStyle = {  
	color: "#ff9300", 
	header: { 
		text: {
			color: "#000", 
		}
	},
	subheader: { 
		text:{
			color: "#ddd",
		},
		color: '#333',
	},
	shadow: {
		x: 3,
		y: 3,
		amount: 5,
		color: '#333'
	},
	border: {
		width: 2,
		color:"#2e6da4",
	},
	connectorLine: {
		thickness: 2,
	}
}

var timelineStyle = {
	width: document.getElementById('timelineJS').offsetWidth - 3,
	height: 475,
	verticalOffset:  30,
	draggingVicinity:{up:470, down:30},
	initialDate:{
		year: 2009,
		month: 1,
		day: 1
	},
	zoom: {
		initial: 35,
		minimum: 1,
		maximum: 74,
		wheelStep: 0.2,
		wheelSpeed: 2
	},
	style: {
		mainLine: {
			size: 7,
		},
		draggingHighlight: {
			area: { up: 10, down: 30 },
			color: "rgba(237,247,255,0.5)"
		},
		marker: {
			color: "#6097f2",
			futureColor: "#aaa",
			minorHeight: 5,	
			majorHeight: 9
		},
		dateLabel: {
			font: "italic 14px Calibri",
			color: "#000",
			futureColor: "#aaa",
			verticalOffset: 18
		}
	},
	article: {
		density: Histropedia.DENSITY_LOW,
		distanceToMainLine: 320,
		collectOngoing: false,
		autoStacking: {
			active: true,
			range: Histropedia.RANGE_SCREEN,
			rowSpacing: 50, 
			fitToHeight: true,
			topGap: 10
		},
		animation: {
			move: {
				active: true,
				duration: 700,	
				easing: 'swing'	
			},
			fade: { 
				active: true,		
				duration: 700,	
				easing: 'swing'	
			}
		},	
		periodLine: {
			spacing: 5,
			thickness:10,
			stacking: { 
				sorter: Histropedia.ARTICLE_FROM_SORTER, 
				reverseOrder: false 
			},
			defaultStyle: articleStyle,  
			defaultActiveStyle: articleActiveStyle,
		}
	},
	onArticleDoubleClick: function(article){
		document.getElementById('blankcard').style.display = "none";
		document.getElementById('name').innerHTML = '';
		document.getElementById('name').innerHTML = article.title;
		document.getElementById('image').src = '';
		if(article.image != null && article.image.currentSrc != undefined)
			document.getElementById('image').src = article.image.currentSrc;
		document.getElementById('launchdate').innerHTML = '<strong> Launch Date </strong> <em> No info available </em>'; 

		document.getElementById('launchdate').innerHTML = '<strong> Launch Date </strong> ' + article.subtitle;
		// document.getElementById('abstract').innerHTML = '';
		// document.getElementById('abstract').innerHTML = article.data.abstract;
		document.getElementById('site').innerHTML = '<strong> Launch Site: </strong> <em> No info available </em>';
		document.getElementById('site').innerHTML = '<strong> Launch Site: </strong> '+article.data.launchsite;
		document.getElementById('crew').innerHTML = '<em> No info available </em>';
		if(article.data.crew == "")
			document.getElementById('crew').innerHTML = '<em>--Unmanned mission--</em>';
		else
			document.getElementById('crew').innerHTML = article.data.crew;
		document.getElementById('wikipedia').style.display = "none";
		document.getElementById('wikipedia').innerHTML = '<em> No info available </em>';
		if(article.data.wikipedia != undefined){
			document.getElementById('wikipedia').href = article.data.wikipedia;
			document.getElementById('wikipedia').style.display = "block";
			document.getElementById('wikipedia').innerHTML = 'wikipedia/' + article.title;
		}
		document.getElementById('wikidata').style.display = "none";
		document.getElementById('wikidata').innerHTML = '<em> No info available </em>';
		if(article.data.wikidata != undefined){
			document.getElementById('wikidata').href = article.data.wikidata;
			document.getElementById('wikidata').innerHTML = 'wikidata/' + article.title;
			document.getElementById('wikidata').style.display = "block";
		}
		document.getElementById('dbpedia').style.display = "none";
		document.getElementById('dbpedia').innerHTML = '<em> No info available </em>';
		var wikilink = article.data.wikipedia.split("/");
		if(wikilink[0] != undefined){
			document.getElementById('dbpedia').href = 'https://dbpedia.org/page/' + wikilink[wikilink.length-1];
			document.getElementById('dbpedia').innerHTML = 'dbpedia/' + article.title;
			document.getElementById('dbpedia').style.display = "block";
		}
		// console.log(article);
	}
}
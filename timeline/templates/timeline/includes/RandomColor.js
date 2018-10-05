function getRandomColorHeader() {
		var letters1 = '6789abc';
		var color = '#';
		for (var i = 0; i < 6; i++) {
			color += letters1[Math.floor(Math.random() * 7)];
		}
		return color;
	}

	function getRandomColorSubHeader() {
	  var letters = 'def';
	  var color = '#';
	  for (var i = 0; i < 6; i++) {
	    color += letters[Math.floor(Math.random() * 3)];
	  }
	  return color;
}
function getRandomColorHeader() {
		var letters = 'ABCDEF';
		var color = '#';
		for (var i = 0; i < 6; i++) {
		color += letters[Math.floor(Math.random() * 6)];
		}
		return color;
	}

	function getRandomColorSubHeader() {
	  var letters = '789';
	  var color = '#';
	  for (var i = 0; i < 6; i++) {
	    color += letters[Math.floor(Math.random() * 3)];
	  }
	  return color;
}
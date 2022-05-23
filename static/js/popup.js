window.onload = function() {
	if(!window.location.hash) {
		window.location = window.location + '#loaded';
        setTimeout(function () {
		    window.location.reload();
        }, 2000)
	}
}
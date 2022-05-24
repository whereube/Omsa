window.onload = function() {
	if(!window.location.hash) {
		window.location = window.location + '#loaded';
        setTimeout(function () {
			$("#pop_box").remove();
        }, 2000)
	}
}
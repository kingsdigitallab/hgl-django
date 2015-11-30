/* UI and Foundation stuff here */

$(document).ready(function() {

	// Expand / Collapse

	$('.expander').bind("click", function() {
		$(this).next('.collapsible').slideToggle(400).removeClass("hide");
		$("i", this).toggleClass("fa-caret-down fa-caret-right");
		return false;
	});

});
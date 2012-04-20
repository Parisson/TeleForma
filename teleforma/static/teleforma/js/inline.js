var django_inline_edit_mode = false;

function form_submit() {
	var options = {
		target : $('#django_inline:parent'),
		success : function() {
			$('.editable').click(place_widget)
		}
	};
	$(this).ajaxSubmit(options);
	return false;
}
function place_widget() {
	$(this).load('/django_inline/widget/' + $(this).attr('id'), {}, function() {
				$('#django_inline').submit(form_submit)
			});
	$(this).unbind('click');
}
function toggle_mode() {
	if(django_inline_edit_mode == true)
	{
		$('.editable').unbind('click');
		$('.editable').removeClass('active_edit');
		django_inline_edit_mode = false;
	} else {
		$('.editable').click(place_widget);
		$('.editable').addClass('active_edit');
		django_inline_edit_mode = true;
	}
}
function django_inline() {
    $(document).keypress(function(e) {
    	if(e.ctrlKey && e.which==13)
    	{
    	   toggle_mode();
    	}
    });
}
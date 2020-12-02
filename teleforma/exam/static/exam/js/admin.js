var jQuery = django.jQuery;

//to send a csrftoken
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
jQuery.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    }
});



function updateCorrectors(){
    var period = $('[name="period"]').val();
    var course = $('[name="course"]').val();
    if(period && course) {
        var $correctors = $('[name="corrector"]');
        var oldValue = $('[name="corrector"]').val();
        $.get('/scripts/get-correctors', {period: period, course: course}, function (data) {
            $correctors.empty();
            for(var i=0; i<data.length ;i++)
                $correctors.append('<option value="'+data[i].value+'"">'+data[i].label+'</option>');
            $correctors.val(oldValue);
        });
    }
}


$(document).ready(function(){
    $('[name="period"], [name="course"]').on('change', updateCorrectors);
    updateCorrectors();
});
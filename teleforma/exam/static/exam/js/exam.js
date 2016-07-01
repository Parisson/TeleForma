
$(document).ready(function(){

    $( "#dialog_mark" ).dialog({
        autoOpen: false,
        draggable: false,
        resizable: false,
                modal: true,
    });

    $( "#dialog_reject" ).dialog({
        autoOpen: false,
        draggable: false,
        resizable: false,
                modal: true,
    });

    $( "#dialog_comments" ).dialog({
        autoOpen: false,
        draggable: false,
        resizable: false,
                modal: true,
    });

    $( "#dialog_help" ).dialog({
        autoOpen: false,
        draggable: false,
        resizable: false,
                modal: true,
    });

    $( "#opener_mark" ).click(function() {
        $( "#dialog_mark" ).dialog({ width: 500 });
        $( "#dialog_mark" ).dialog( "open");
        return false;
    });

    $( "#opener_reject" ).click(function() {
        $( "#dialog_reject" ).dialog( "open");
        return false;
    });

    $( "#opener_comments" ).click(function() {
        $( "#dialog_comments" ).dialog( "open");
        return false;
    });

    $( "#opener_help" ).click(function() {
        $( "#dialog_help" ).dialog( "open");
        return false;
    });

    var b1 = $('#validate_button');
    b1.unbind('click').click(function() {
        $(window).unbind('beforeunload');
        b1.unbind('click');
        $('#_MarkForm #id_status').val("4");
        $('#_MarkForm').submit();
    });

    var b2 = $('#reject_button');
    b2.unbind('click').click(function() {
        $(window).unbind('beforeunload');
        b2.unbind('click');
        $('#_RejectForm #id_status').val("0");
        $('#_RejectForm').submit();
    });

	// $("#box-iframe").contents().find("span.btn.text-btn.strikeout-btn").hide();


});

$( ".form-check-input" ).click(function() {
    console.log($(this).is(':checked'))
    var url = $(this).attr("data-target") + '?status=' + $(this).is(':checked')
    $.get(url);
});
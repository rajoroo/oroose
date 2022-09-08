$(document).ready(function(){
    // Load table on page ready
    $('#contenthere').load('/bengaluru/load-500/');

    // On button click load data
    $(".load-table").click(function(){
        $('#contenthere').load('/bengaluru/load-500/');
    });
});
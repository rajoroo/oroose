function reload_data() {
    fh_url = $('#show_fh').attr('trigger-url');
    $('#show_fh').load(fh_url);
    fhz_url = $('#show_fhz').attr('trigger-url');
    $('#show_fhz').load(fhz_url);
}

/* --------Start Auto reload--------- */

// Data reload every 60 seconds
setInterval(function(){
    reload_data()
}, 1000 * 60);

/* --------End Auto reload--------- */



/* --------Start Button action--------- */

// On button click load FH data
$("#load_data").click(function(){
    reload_data()
});

// On button click trigger url
$(".ser_act").click(function(){
    url = $(this).attr('trigger-url');
    $.get(url);
});

/* --------End Button action--------- */



$(document).ready(function(){

    // Load fh and fh zero table on page ready
    reload_data()

});

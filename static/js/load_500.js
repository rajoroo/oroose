function reload_fh_data() {
    url = $('#show_fh').attr('trigger-url');
    $('#show_fh').load(url);
}

function reload_fhz_data() {
    url = $('#show_fhz').attr('trigger-url');
    $('#show_fhz').load(url);
}


/* --------Start Auto reload--------- */

// Data reload every 60 seconds
setInterval(function(){
    reload_fh_data()
    reload_fhz_data()
}, 1000 * 60);

/* --------End Auto reload--------- */



/* --------Start Button action--------- */

// On button click load FH data
$("#load_fh").click(function(){
    reload_fh_data()
});

// On button click load FHZ data
$("#load_fhz").click(function(){
    reload_fhz_data()
});

// On button click trigger url
$(".ser_act").click(function(){
    url = $(this).attr('trigger-url');
    $.get(url);
});

/* --------End Button action--------- */



$(document).ready(function(){

    // Load fh and fh zero table on page ready
    reload_fh_data()
    reload_fhz_data()

});

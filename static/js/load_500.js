function reload_fh_data() {
    $('#show_fh').load('/bengaluru/load_five_hundred/');
}

function reload_fhz_data() {
    $('#show_fhz').load('/bengaluru/load_five_hundred_zero/');
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

// On button click pull FH data
$("#pull_fh").click(function(){
    $.get("/bengaluru/pull_five_hundred/");
});

// On button click load FHZ data
$("#load_fhz").click(function(){
    reload_fhz_data()
});

// On button click analyse FHZ data
$("#analyse_fhz").click(function(){
    $.get("/bengaluru/get_zero_value/");
});

/* --------End Button action--------- */



$(document).ready(function(){

    // Load fh and fh zero table on page ready
    reload_fh_data()
    reload_fhz_data()

});

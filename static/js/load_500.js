function reload_500_data() {
    $('#nifty_500').load('/bengaluru/load_five_hundred/');
}

function reload_fh_zero_data() {
    $('#fh_zero').load('/bengaluru/load_five_hundred_zero/');
}

$(document).ready(function(){

    // Load table on page ready
    reload_500_data()
    reload_fh_zero_data()

    // On button click load data
    $(".load_500").click(function(){
        reload_500_data()
    });

    $(".pull_500").click(function(){
        $.get("/bengaluru/pull_five_hundred/");
    });

    // On button click load data
    $(".load_fh_zero").click(function(){
        reload_fh_zero_data()
    });

    // On button click load data
    $(".get_zero").click(function(){
        $.get("/bengaluru/get_zero_value/");
    });

});

// Data reload every 60 seconds
setInterval(function(){
    reload_500_data()
    reload_fh_zero_data()
}, 1000 * 60);



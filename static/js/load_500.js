function reload_500_data() {
    $('#nifty_500').load('/bengaluru/load_five_hundred/');
}

$(document).ready(function(){

    // Load table on page ready
    reload_500_data()

    // On button click load data
    $(".load_500").click(function(){
        reload_500_data()
    });

    $(".pull_500").click(function(){
        $.get("/bengaluru/pull_five_hundred/");
    });

    // On button click load data
    $(".get_zero").click(function(){
        console.log("ip")
        $.get("/bengaluru/get_zero_value/");
    });

});

// Data reload every 60 seconds
setInterval(function(){
    reload_500_data()
}, 1000 * 60);



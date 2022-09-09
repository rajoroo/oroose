function reload_500_data() {
    $('#nifty_500').load('/bengaluru/load-500/');
}

$(document).ready(function(){

    // Load table on page ready
    reload_500_data()

    // On button click load data
    $(".load-500").click(function(){
        reload_500_data()
    });

    $(".nse-500").click(function(){
        $.get("/bengaluru/load-nse-500/", function(data, status){
            alert("Status: " + status);
         });
    });

});

// Data reload every 60 seconds
setInterval(function(){
    reload_500_data()
}, 1000 * 60);
function reload_data() {
    $.ajax({
      type: 'GET',
      url: $("#ajax-content").attr('trigger-url'),
      beforeSend: function( xhr ) {
        $('.loader').css('display', 'flex');
      },
      success: function(data){
        $("#show_content").empty().append(data);
      },
      complete: function(data){
        setTimeout(function(){
            $('.loader').css('display', 'none');
            console.log("fone")
        }, 1000 * 5)
      }
    })
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
    //url = $(this).attr('trigger-url');
    //$.get(url);

    $.ajax({
      type: 'GET',
      url: $(this).attr('trigger-url'),
      beforeSend: function( xhr ) {
        $('.ajax-loader').css("visibility", "show");
      },
      success: function(data){
        $("#resultarea").text(data);
      },
      complete: function(data){
        $('.ajax-loader').css("visibility", "hidden");
      }
    })



});

/* --------End Button action--------- */

$(document).ready(function(){

    // Load fh and fh zero table on page ready
    reload_data()

});

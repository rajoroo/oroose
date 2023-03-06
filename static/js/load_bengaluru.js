// On button click trigger url
$(".ser_act").click(function(){

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

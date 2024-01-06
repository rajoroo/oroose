//Modal for uploading files

$( ".modal_act" ).click(function () {
    $.ajax({
      type: 'GET',
      url: $(this).attr('trigger-url'),
      beforeSend: function( xhr ) {
        $('.ajax-loader').css("visibility", "show");
      },
      success: function(data){
        $("#modelresultarea").html(data);
      },
      complete: function(data){
        $('.ajax-loader').css("visibility", "hidden");
      }
    })
});

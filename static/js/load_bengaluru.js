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
        var message = data["responseJSON"]["message"];
        $('#alerts').empty();

        $('#alerts').append(
        '<div class="alert alert-success alert-dismissible fade" role="alert" id="buttonAlert">' +
            '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
            '<span aria-hidden="true">&times;</span>' +
            '</button>' + message + '</div>');
        $("#buttonAlert").addClass('show')
      }

    })

});

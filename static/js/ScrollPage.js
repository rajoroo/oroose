// On button click smooth scroll
$(".scroll_act").click(function(){
    var scroll_id = $(this).attr('scroll-div')
    var element = document.getElementById(scroll_id);
    element.scrollIntoView({behavior: "smooth"});
});


let to_top_btn = document.getElementById("to_top_btn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    to_top_btn.style.display = "block";
  } else {
    to_top_btn.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

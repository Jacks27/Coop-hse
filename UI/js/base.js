 // Back to top button
$(document).ready(function(){
 $(window).scroll(function() {  
    if ($(this).scrollTop() > 40 ) {
      $('.back-to-top').fadeIn('slow');
    } else {
      $('.back-to-top').fadeOut('slow');
    }
  });
  $('.back-to-top').click(function(){
    $('html, body').animate({scrollTop : 0},1500, 'easeInOutExpo');
    return false;
  });

  $('.counter').counterUp({
    delay: 10,
    time: 1000
});

// search questions
$("search-box").on("keyup", function() {
  var g = $(this).val();
  var gupp=g.toUppercase();
  $(".collapsible .content p").each( function() {
  var s = $(this).text();
  var supp=s.toUppercase();
  if (supp.indexOf(g!=-1)){
  $(this).parent().parent().show();
  }
  else {
  $(this).parent().parent().hide();
  }
  });
  });
});

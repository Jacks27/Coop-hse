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

});

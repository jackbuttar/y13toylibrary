$(document).ready(function(){
  $('.toggle').click(function(){
    $('#menu').toggleClass('open');
    $('.container').toggleClass('menu-open');
  });
});
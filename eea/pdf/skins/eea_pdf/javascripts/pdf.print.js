/*
FIX for How do I avoid a page break immediately after a header
http://stackoverflow.com/questions/9238868/how-do-i-avoid-a-page-break-immediately-after-a-header
*/

$(document).ready(function(){
    $('#content-core h2').each(function(i, e){
      $(e).nextUntil('h2').andSelf().wrapAll('<div class="nobreak">');
      $('h2 + .indicator-figure-plus-container').closest('.nobreak').addClass('break');
    });
    $('#content-core h3').each(function(i, e){
      if (!$(e).closest('.nobreak').length){
        $(e).nextUntil('h3').andSelf().wrapAll('<div class="nobreak">');
      }
    });
});

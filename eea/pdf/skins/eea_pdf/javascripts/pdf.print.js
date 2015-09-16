/*
FIX for How do I avoid a page break immediately after a header
http://stackoverflow.com/questions/9238868/how-do-i-avoid-a-page-break-immediately-after-a-header
*/

$(document).ready(function(){
    var $content_core = $('#content-core');
    $content_core.find('h2').each(function(i, e){
      if (!$(e).closest('.cover').length){
        $(e).nextUntil('h2').andSelf().wrapAll('<div class="nobreak">');
      }
    });
    $content_core.find('h3').each(function(i, e){
      if (!$(e).closest('.nobreak, .keyMessage').length){
        $(e).nextUntil('h3').andSelf().wrapAll('<div class="nobreak">');
      }
    });
});

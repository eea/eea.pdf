/*
 FIX for How do I avoid a page break immediately after a header
 http://stackoverflow.com/questions/9238868/how-do-i-avoid-a-page-break-immediately-after-a-header
 */

jQuery(document).ready(function($){
    var $content_core = $('#content-core');
    $content_core.find('h2').each(function(i, e){
        if (!$(e).closest('.cover').length){
            $(e).next().andSelf().wrapAll('<div class="nobreak">');
        }
    });
    $content_core.find('h3').each(function(i, e){
       if (!$(e).closest('.nobreak, .keyMessage').length){
         $(e).next().andSelf().wrapAll('<div class="nobreak">');
       }
    });

    // #77970 workaround content where Figure header should be on the same
    // page with the next figure iframe chart
   $content_core.find('strong').each(function(i, e){
       var $ptag;
        if (e.innerHTML.indexOf('Figure') === 0) {
           $ptag = $(e).closest('p');
           $ptag.next().andSelf().wrapAll('<div class="nobreak">');
       }
   });

      $content_core.find('.figureHeading').each(function(i, e){
        var $next_el = $(e).next();
        if ($next_el.length && $next_el[0].innerHTML === "&nbsp;") {
            $next_el.remove();
        }
        $(e).next().andSelf().wrapAll('<div class="nobreak">');
    });

    /* Fix #28298, empty div.pageBreak cause segmentation fault in wkhtmltopdf */
    $content_core.find('div.pageBreak').each(function(i, e){
        $(e).html("&nbsp;");
    });

    // within collection change h1 to h4 to increment one step
    var $folder_titles = $(".pdf-folder-title");
    $folder_titles.each(function(idx, el) {
        var $el = $(el);
        var content = el.textContent.trim().length;
        var $parent = $el.parent();
        var $h1 = $parent.find('h1:not(.pdf-folder-title)');
        var $h2 = $parent.find('h2');
        var $h3 = $parent.find('h3');
        var $h4 = $parent.find('h4');

        if (!content) {
            $el.remove();
        }
        $h1 = $h1.add($h2);
        $h1 = $h1.add($h3);
        $h1 = $h1.add($h4);
        $h1.each(function(idx, el) {
            var $el = $(el);

            var incremented_header = window.parseInt(el.tagName[1], 10);
            incremented_header += 1;
            var tagName = "<h" + incremented_header + " />";
            var $replacement = $(tagName, { text: $el.text()  });
            $el.replaceWith($replacement);
        });
    });
});

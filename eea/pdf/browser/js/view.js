if(window.EEA === undefined){
  var EEA = {
    who: 'eea.pdf',
    version: '1.1'
  };
}

EEA.Pdf = function(context, options){
 var self = this;
  self.context = context;

  self.settings = {
  };

  if(options){
    jQuery.extend(self.settings, options);
  }

  self.initialize();
};

EEA.Pdf.prototype = {
  initialize: function(){
    var self = this;
    self.async = self.context.data('async');

    if(self.async){
      self.init_async();
    }

  },

  init_async: function(){
    var self = this;
    self.links = jQuery('body').find('a[href$="download.pdf"]');

    self.links.prepOverlay({
      subtype: 'ajax',
      formselector: 'form',
      filter: '.eea-pdf-download',
      cssclass: 'eea-pdf-overlay'
    });
  }
};


jQuery.fn.EEAPdf = function(options){
  return this.each(function(){
    var context = jQuery(this);
    var adapter = new EEA.Pdf(context, options);
    context.data('EEAPdf', adapter);
  });
};

jQuery(document).ready(function($){

  var items = jQuery('.eea-pdf-viewlet');

  // #27958 take into consideration templates which fill main
  // thus not rendering the async data but still have the pdf download
  var $pdf_download_links, $body;
  if (!items.length) {
    $body = $('body');
    $pdf_download_links = $body.find('a[href$="download.pdf"]');
    if ($pdf_download_links.length) {
      $body.data("async", "true");
      items = $body;
    }
  }

  items.EEAPdf();

});

if(window.EEA === undefined){
  var EEA = {
    who: 'eea.pdf',
    version: '1.0'
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
      filter: '.eea-pdf-download'
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

jQuery(document).ready(function(){

  var items = jQuery('.eea-pdf-viewlet');
  items.EEAPdf();

});

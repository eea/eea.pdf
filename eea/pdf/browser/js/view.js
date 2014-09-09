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
    self.message = self.context.find('.portalMessage.info dd');
    self.message.addClass('eea-pdf-message');

    self.add_links();
  },

  add_links: function(){
    var self = this;
    if(!self.message.length){
      return;
    }

    var text = self.replaceURL(self.message.text());
    self.message.html(text);
  },

  replaceURL: function(inputText) {
    var replacePattern = /(\b(https?|ftp):\/\/[\-A-Z0-9+&@#\/%?=~_|!:,.;]*[\-A-Z0-9+&@#\/%=~_|])/gim;
    return inputText.replace(replacePattern, '<a href="$1" target="_blank">$1</a>');
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

  var items = jQuery('body');
  items.EEAPdf();

});


$(document).ready(function() {

  (function() {
    var $container = $('body');
    var $guide = $('<div></div>');
    var $button = $('<button></button>');

    $guide.attr({'id': 'guide'});

    $button.attr({
      'id': 'debug-activator',
      'title': 'Toggle debug guide'
    });

    $container.append($guide);
    $container.append($button);

    $button.on('click', function(e) {
      $guide.toggleClass('debug');
      $button.toggleClass('active');
    });

  })()

});


define(['jquery'], function($) {

  didLaunch = function() {
      console.log('hi, it launched!');
      $('#ok').show();
      $('#fail').hide();
  };

  return {
    didLaunch: didLaunch
  };
});

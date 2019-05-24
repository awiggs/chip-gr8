(function() {
  var index = window.location.href.indexOf('#');
  var destination = '';
  if (index < 0) {
    window.location = window.location + '#Introduction';
  }
})();

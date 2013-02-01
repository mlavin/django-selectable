(function() {
  // Get any jquery=___ param from the query string.
  var jqversion = location.search.match(/[?&]jquery=(.*?)(?=&|$)/);
  var uiversion = location.search.match(/[?&]ui=(.*?)(?=&|$)/);
  var path;
  window.jqversion = jqversion && jqversion[1] || '1.7.2';
  window.uiversion = uiversion && uiversion[1] || '1.8.24';
  jqpath = 'http://code.jquery.com/jquery-' + window.jqversion + '.js';
  uipath = 'http://code.jquery.com/ui/' + window.uiversion + '/jquery-ui.js';
  // This is the only time I'll ever use document.write, I promise!
  document.write('<script src="' + jqpath + '"></script>');
  document.write('<script src="' + uipath + '"></script>');
}());

var express = require('express');
var app = express();

app.get('/hello', function (req, res) {
  res.send('Hello World');
});

var server = app.listen(8080, function () {
  var host = server.address().address;
  var port = server.address().port;

  console.log('=== server listening on 127.0.0.1:%s ===', port);
  console.log('begin benchmark');
});

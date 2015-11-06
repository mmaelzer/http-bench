var http = require('http');

console.log('=== server listening on 127.0.0.1:8080 ===');

http.createServer(function(req, res) {
  // json post request
  if (req.url.indexOf('json') >= 0 && req.method === 'POST') {
    var body = '';
    req.on('data', function(data) {
      body += data;
    });
    req.on('end', function() {
      res.writeHead(200, {'Content-Type': 'application/json'});
      res.end(JSON.stringify(JSON.parse(body)));
    });
  }
  // hello world get request 
  else if (req.url.indexOf('hello') >= 0) {
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.end('Hello World\n');
  }
}).listen(8080, function() {
  console.log('begin benchmark');         
});

var http = require('http');

console.log('=== server listening on 127.0.0.1:7070 ===');

http.createServer(function(req, res) {
  if (req.method === 'POST') {
    var body = '';
    req.on('data', function(data) {
      body += data;
    });
    req.on('end', function() {
      res.writeHead(200, {'Content-Type': 'application/json'});
      res.end(JSON.stringify(JSON.parse(body)));
    });
  } else {
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.end('Hello World\n');
  }
}).listen(7070);

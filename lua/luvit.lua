local http = require('http')

http.createServer(function (req, res)
  local body = "Hello World\n"
  res:setHeader("Content-Type", "text/plain")
  res:setHeader("Content-Length", #body)
  res:finish(body)
end):listen(8080, '127.0.0.1')

print('Server running at http://127.0.0.1:8080/')
print('begin benchmark')

import 'dart:io';

main() async {
  var requestServer =
      await HttpServer.bind(InternetAddress.LOOPBACK_IP_V4, 8080);
  print('=== server listening on 127.0.0.1:${requestServer.port} ===');
  print('begin benchmark');

  await for (HttpRequest request in requestServer) {
    request.response..write('Hello World')
                    ..close();
  }
}

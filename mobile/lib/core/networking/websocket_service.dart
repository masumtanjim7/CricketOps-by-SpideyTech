import 'dart:convert';

import 'package:web_socket_channel/web_socket_channel.dart';

class WebSocketService {
  WebSocketChannel? _channel;

  Stream<Map<String, dynamic>> connect(
    String matchId, {
    String host = '127.0.0.1:8000',
  }) {
    final uri = Uri.parse('ws://$host/ws/matches/$matchId/');
    _channel = WebSocketChannel.connect(uri);
    return _channel!.stream.map(
      (event) => jsonDecode(event as String) as Map<String, dynamic>,
    );
  }

  void disconnect() {
    _channel?.sink.close();
  }
}

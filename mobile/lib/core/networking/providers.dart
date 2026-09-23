import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'api_client.dart';
import 'websocket_service.dart';

final apiClientProvider = Provider<ApiClient>((ref) {
  return ApiClient();
});

final webSocketServiceProvider = Provider<WebSocketService>((ref) {
  return WebSocketService();
});

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/networking/api_client.dart';
import '../../../../core/networking/websocket_service.dart';
import '../models/delivery_command.dart';

class MatchUIState {
  final int score;
  final double overs;
  final int version;
  final bool isSubmitting;
  final String? errorMessage;

  MatchUIState({
    required this.score,
    required this.overs,
    required this.version,
    this.isSubmitting = false,
    this.errorMessage,
  });

  MatchUIState copyWith({
    int? score,
    double? overs,
    int? version,
    bool? isSubmitting,
    String? errorMessage,
  }) {
    return MatchUIState(
      score: score ?? this.score,
      overs: overs ?? this.overs,
      version: version ?? this.version,
      isSubmitting: isSubmitting ?? this.isSubmitting,
      errorMessage: errorMessage,
    );
  }
}

// 1. Providers
final apiClientProvider = Provider((ref) => ApiClient());
final websocketServiceProvider = Provider((ref) => WebSocketService());

// 2. Store the Match ID here instead of passing it through a Family Provider
final activeMatchIdProvider = Provider<String>((ref) {
  return '014797c4-8e84-44fc-a2cf-f7271af87b80';
});

// 3. Standard Notifier (Guaranteed to work in all Riverpod 2.0+ versions)
class ScorerController extends Notifier<MatchUIState> {
  @override
  MatchUIState build() {
    final matchId = ref.read(activeMatchIdProvider);
    final wsService = ref.read(websocketServiceProvider);

    wsService.connect(matchId).listen((event) {
      if (event['type'] == 'delivery.committed') {
        final data = event['data'] as Map<String, dynamic>;
        state = state.copyWith(
          score: data['score'] as int,
          overs: (data['overs'] as num).toDouble(),
          version: event['version'] as int,
        );
      }
    });

    ref.onDispose(() {
      wsService.disconnect();
    });

    return MatchUIState(score: 0, overs: 0.0, version: 1);
  }

  Future<void> submitBall({
    required String inningsId,
    required String strikerId,
    required String nonStrikerId,
    required String bowlerId,
    int runs = 0,
    String? extraType,
    int extraRuns = 0,
  }) async {
    state = state.copyWith(isSubmitting: true, errorMessage: null);

    final command = DeliveryCommand(
      inningsId: inningsId,
      clientEventId: DateTime.now().toIso8601String(),
      expectedVersion: state.version,
      strikerId: strikerId,
      nonStrikerId: nonStrikerId,
      bowlerId: bowlerId,
      batRuns: runs,
      extraType: extraType,
      extraRuns: extraRuns,
    );

    try {
      final matchId = ref.read(activeMatchIdProvider);
      await ref
          .read(apiClientProvider)
          .commitDelivery(matchId, command.toJson());
      state = state.copyWith(isSubmitting: false);
    } catch (e) {
      state = state.copyWith(isSubmitting: false, errorMessage: e.toString());
    }
  }
}

final scorerControllerProvider =
    NotifierProvider<ScorerController, MatchUIState>(ScorerController.new);

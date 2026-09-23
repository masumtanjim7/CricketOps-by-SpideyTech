import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'features/scorer_console/presentation/scorer_controller.dart';

void main() {
  runApp(const ProviderScope(child: CricketOpsApp()));
}

class CricketOpsApp extends StatelessWidget {
  const CricketOpsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CricketOps',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF0D1B2A),
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      home: const ScorerScreen(),
    );
  }
}

class ScorerScreen extends ConsumerWidget {
  const ScorerScreen({super.key});

  // Target UUIDs from your seed script
  static const inningsId = 'fca1585e-ff8a-466d-bc40-55160ed8d4e1';
  static const strikerId = 'c22d05cd-e81a-4826-ad65-14293a0b3f63';
  static const nonStrikerId = '6e3b3d49-f359-4fe1-b29d-577659d6ca7e';
  static const bowlerId = '976a9064-9152-46a5-bcba-26f198d6da50';

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Look here: No more (matchId) passed into the provider!
    final state = ref.watch(scorerControllerProvider);
    final controller = ref.read(scorerControllerProvider.notifier);

    return Scaffold(
      appBar: AppBar(
        title: const Text('CricketOps Scorer Console'),
        centerTitle: true,
      ),
      body: Column(
        children: [
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(24),
            margin: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.grey.shade900,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: Colors.grey.shade800),
            ),
            child: Column(
              children: [
                Text(
                  '${state.score}',
                  style: const TextStyle(
                    fontSize: 64,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                Text(
                  'Overs: ${state.overs.toStringAsFixed(1)} | Ver: ${state.version}',
                  style: const TextStyle(fontSize: 18, color: Colors.grey),
                ),
                if (state.isSubmitting)
                  const Padding(
                    padding: EdgeInsets.only(top: 8),
                    child: LinearProgressIndicator(),
                  ),
                if (state.errorMessage != null)
                  Padding(
                    padding: const EdgeInsets.only(top: 8),
                    child: Text(
                      state.errorMessage!,
                      style: const TextStyle(color: Colors.redAccent),
                      textAlign: TextAlign.center,
                    ),
                  ),
              ],
            ),
          ),
          const Spacer(),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 24),
            child: Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [0, 1, 2, 3]
                      .map((r) => _actionButton(context, controller, runs: r))
                      .toList(),
                ),
                const SizedBox(height: 12),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    _actionButton(context, controller, runs: 4),
                    _actionButton(context, controller, runs: 6),
                    _extraButton(context, controller, 'WIDE'),
                    _extraButton(context, controller, 'NO_BALL'),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _actionButton(
    BuildContext context,
    ScorerController controller, {
    required int runs,
  }) {
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        minimumSize: const Size(70, 70),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
      onPressed: () => controller.submitBall(
        inningsId: inningsId,
        strikerId: strikerId,
        nonStrikerId: nonStrikerId,
        bowlerId: bowlerId,
        runs: runs,
      ),
      child: Text(
        '$runs',
        style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
      ),
    );
  }

  Widget _extraButton(
    BuildContext context,
    ScorerController controller,
    String type,
  ) {
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.amber.shade900,
        minimumSize: const Size(70, 70),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
      onPressed: () => controller.submitBall(
        inningsId: inningsId,
        strikerId: strikerId,
        nonStrikerId: nonStrikerId,
        bowlerId: bowlerId,
        extraType: type,
        extraRuns: 1,
      ),
      child: Text(
        type == 'WIDE' ? 'WD' : 'NB',
        style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
      ),
    );
  }
}

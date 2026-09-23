class DeliveryCommand {
  final String inningsId;
  final String clientEventId;
  final int expectedVersion;
  final String strikerId;
  final String nonStrikerId;
  final String bowlerId;
  final int batRuns;
  final String? extraType;
  final int extraRuns;

  DeliveryCommand({
    required this.inningsId,
    required this.clientEventId,
    required this.expectedVersion,
    required this.strikerId,
    required this.nonStrikerId,
    required this.bowlerId,
    this.batRuns = 0,
    this.extraType,
    this.extraRuns = 0,
  });

  Map<String, dynamic> toJson() {
    return {
      'innings_id': inningsId,
      'client_event_id': clientEventId,
      'expected_version': expectedVersion,
      'striker_id': strikerId,
      'non_striker_id': nonStrikerId,
      'bowler_id': bowlerId,
      'bat_runs': batRuns,
      'extra_type': extraType,
      'extra_runs': extraRuns,
    };
  }
}

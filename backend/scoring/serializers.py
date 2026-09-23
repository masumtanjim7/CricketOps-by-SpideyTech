from rest_framework import serializers

class WicketInputSerializer(serializers.Serializer):
    player_out_id = serializers.UUIDField()
    kind = serializers.CharField(max_length=50)
    bowler_credit = serializers.BooleanField(default=True)

class DeliveryCommandSerializer(serializers.Serializer):
    innings_id = serializers.UUIDField()
    client_event_id = serializers.CharField(max_length=100)
    expected_version = serializers.IntegerField()
    striker_id = serializers.UUIDField()
    non_striker_id = serializers.UUIDField()
    bowler_id = serializers.UUIDField()
    bat_runs = serializers.IntegerField(default=0, min_value=0)
    extra_type = serializers.ChoiceField(
        choices=['WIDE', 'NO_BALL', 'BYE', 'LEG_BYE', 'PENALTY'], 
        required=False, 
        allow_null=True
    )
    extra_runs = serializers.IntegerField(default=0, min_value=0)
    wicket = WicketInputSerializer(required=False, allow_null=True)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .serializers import DeliveryCommandSerializer
from .services import ScoringEngineService

class CommitDeliveryView(APIView):
    def post(self, request, match_id):
        serializer = DeliveryCommandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            delivery, snapshot = ScoringEngineService.process_delivery(
                match_id=match_id,
                innings_id=data['innings_id'],
                client_event_id=data['client_event_id'],
                expected_version=data['expected_version'],
                striker_id=data['striker_id'],
                non_striker_id=data['non_striker_id'],
                bowler_id=data['bowler_id'],
                bat_runs=data.get('bat_runs', 0),
                extra_type=data.get('extra_type'),
                extra_runs=data.get('extra_runs', 0),
                wicket_data=data.get('wicket')
            )
            return Response({
                "message": "Delivery committed successfully",
                "delivery_id": str(delivery.id),
                "snapshot": {
                    "score": snapshot.score,
                    "overs": snapshot.overs,
                    "version": snapshot.version
                }
            }, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
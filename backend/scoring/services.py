from django.db import transaction
from django.core.exceptions import ValidationError
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from matches.models import Match, Innings
from players.models import Player
from .models import Delivery, DeliveryExtra, Wicket, MatchSnapshot

class ScoringEngineService:
    @staticmethod
    @transaction.atomic
    def process_delivery(
        match_id: str,
        innings_id: str,
        client_event_id: str,
        expected_version: int,
        striker_id: str,
        non_striker_id: str,
        bowler_id: str,
        bat_runs: int = 0,
        extra_type: str = None,
        extra_runs: int = 0,
        wicket_data: dict = None
    ):
        # 1. Idempotency Check (Section 6.5)
        existing = Delivery.objects.filter(client_event_id=client_event_id).first()
        if existing:
            snapshot, _ = MatchSnapshot.objects.get_or_create(match_id=match_id)
            return existing, snapshot

        # 2. Row Lock & Version Check (Section 4.3 & 6.5)
        innings = Innings.objects.select_for_update().get(id=innings_id, match_id=match_id)
        if innings.version != expected_version:
            raise ValidationError(f"Version mismatch: expected {expected_version}, got {innings.version}")

        # 3. Rule Calculations: Legality & Runs (Section 5.3)
        is_legal = extra_type not in ['WIDE', 'NO_BALL']
        total_extras = extra_runs if extra_type else 0
        total_runs = bat_runs + total_extras

        # 4. Monotonic Sequence (Section 5.2)
        last_seq = Delivery.objects.filter(innings=innings).count()
        next_seq = last_seq + 1

        striker = Player.objects.get(id=striker_id)
        non_striker = Player.objects.get(id=non_striker_id)
        bowler = Player.objects.get(id=bowler_id)

        # 5. Persist Delivery Facts
        delivery = Delivery.objects.create(
            innings=innings,
            sequence=next_seq,
            striker=striker,
            non_striker=non_striker,
            bowler=bowler,
            bat_runs=bat_runs,
            extras_total=total_extras,
            legal_delivery=is_legal,
            client_event_id=client_event_id
        )

        if extra_type:
            DeliveryExtra.objects.create(
                delivery=delivery,
                type=extra_type,
                amount=extra_runs
            )

        if wicket_data:
            out_player = Player.objects.get(id=wicket_data['player_out_id'])
            Wicket.objects.create(
                delivery=delivery,
                player_out=out_player,
                kind=wicket_data['kind'],
                bowler_credit=wicket_data.get('bowler_credit', True)
            )

        # 6. Increment Version & Update Aggregates
        innings.version += 1
        innings.save()

        # Calculate current overs from legal balls
        legal_balls = Delivery.objects.filter(innings=innings, legal_delivery=True).count()
        completed_overs = legal_balls // 6
        remaining_balls = legal_balls % 6
        overs_display = float(f"{completed_overs}.{remaining_balls}")

        # Update or create fast snapshot
        snapshot, _ = MatchSnapshot.objects.get_or_create(match_id=match_id)
        snapshot.score += total_runs
        snapshot.overs = overs_display
        snapshot.version = innings.version
        snapshot.save()

        # 7. Post-Commit WebSocket Broadcast (Section 4.3 & 6.4)
        channel_layer = get_channel_layer()
        payload = {
            "type": "delivery.committed",
            "match_id": str(match_id),
            "version": snapshot.version,
            "data": {
                "score": snapshot.score,
                "overs": snapshot.overs,
                "sequence": delivery.sequence,
                "runs": total_runs,
                "is_legal": is_legal
            }
        }
        
        transaction.on_commit(lambda: async_to_sync(channel_layer.group_send)(
            f"match_{match_id}",
            {
                "type": "match.event",
                "payload": payload
            }
        ))

        return delivery, snapshot
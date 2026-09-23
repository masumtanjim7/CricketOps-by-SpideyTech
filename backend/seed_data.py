import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from organizations.models import Organization
from players.models import Player
from teams.models import Team, TeamMembership
from matches.models import Match, MatchTeam, Innings
from scoring.models import MatchSnapshot

def run():
    print("Seeding baseline CricketOps data...")
    user = User.objects.first()
    if not user:
        print("Please create a superuser first.")
        return

    # 1. Organization
    org, _ = Organization.objects.get_or_create(
        name="SpideyTech Premier League",
        defaults={"type": "Club", "verification_status": "verified", "owner": user}
    )

    # 2. Teams
    team_a, _ = Team.objects.get_or_create(name="Dhaka Warriors", organization=org)
    team_b, _ = Team.objects.get_or_create(name="Chittagong Strikers", organization=org)

    # 3. Players
    def create_roster(team, prefix):
        players = []
        for i in range(1, 12):
            pid = f"{prefix}-{i:02d}"
            p, _ = Player.objects.get_or_create(public_id=pid, defaults={"verification_status": "verified"})
            TeamMembership.objects.get_or_create(team=team, player=p, defaults={"role": "Player"})
            players.append(p)
        return players

    players_a = create_roster(team_a, "DW")
    players_b = create_roster(team_b, "CS")

    # 4. Match
    match, _ = Match.objects.get_or_create(status="live", version=1)
    MatchTeam.objects.get_or_create(match=match, team=team_a, defaults={"side": "team_a", "toss_choice": "bat"})
    MatchTeam.objects.get_or_create(match=match, team=team_b, defaults={"side": "team_b", "toss_choice": "bowl"})

    # 5. Innings
    innings, _ = Innings.objects.get_or_create(
        match=match,
        batting_team=team_a,
        number=1,
        defaults={"status": "live", "version": 1}
    )

    # 6. Snapshot
    snapshot, _ = MatchSnapshot.objects.get_or_create(match=match, defaults={"score": 0, "overs": 0.0, "version": 1})

    print(f"\n--- SEED SUCCESSFUL ---")
    print(f"Match ID: {match.id}")
    print(f"Innings ID: {innings.id}")
    print(f"Striker (DW-01) ID: {players_a[0].id}")
    print(f"Non-Striker (DW-02) ID: {players_a[1].id}")
    print(f"Bowler (CS-01) ID: {players_b[0].id}")

if __name__ == "__main__":
    run()
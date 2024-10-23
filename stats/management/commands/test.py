from django.core.management.base import BaseCommand
from stats.models import League, Season, User, Username, Matchup

class Command(BaseCommand):
    help = 'Add a new league to the database.'

    def add_arguments(self, parser):
        parser.add_argument("user",
                            help="Nickname of the league to add.", type=str)
        parser.add_argument("season",
                            help="Nickname of the league to add.", type=str)

    def handle(self, *args, **options):
        seasons = Season.objects.get(season_id=options['season'])
        print(User.objects.get(user_id=options['user'], seasons__in=seasons))



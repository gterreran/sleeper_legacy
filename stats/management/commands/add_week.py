from django.core.management.base import BaseCommand
from stats.bin.db_add import add_week

class Command(BaseCommand):
    help = 'Add a week of matchups to a league.'

    def add_arguments(self, parser):
        parser.add_argument("week_list", nargs='?',
                            help="Single week number or comma-separated list", type=str)
        parser.add_argument("--season",
                            help="League to add the season to.",
                            required=True, type=int)
        parser.add_argument("--all",
                            help="League to add the season to.", default=0, action='store_true')

    def handle(self, *args, **options):
        if options["week_list"] is None:
            if options['all']:
                options["week_list"] = ','.join([str(el) for el in range(1,19)])
            else:
                self.stdout.write(f'ERROR - A week, or a comma-separated list of weeks must be provided. Alternatively the flag --all must be used.')
                exit()
        
        
        add_week(week_list = options["week_list"].split(','), season_id = options["season"], output = self.stdout)
        

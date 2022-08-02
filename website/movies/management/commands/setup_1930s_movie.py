from django.core.management.base import BaseCommand, CommandError
from movies.models import Film, Decade

class Command(BaseCommand):
    help = 'Sets up the movies database.'

    def handle(self, *args, **options):

        Film.objects.get_or_create(
            title="",
            year="",
            rating="",
            description="",
            director="",
            writer="",
            cast="Gilbert M. 'Broncho Billy' Anderson, A.C. Abadie, George Barnes",
            studio="",
            country="",
            review='''
            
                    ''',
            image="",
            decade_fk=Decade.objects.get(decade="1930"),
        ),
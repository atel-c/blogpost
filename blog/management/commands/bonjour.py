from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Affiche un message de bienvenue personnalisé"

    def add_arguments(self, parser):
       parser.add_argument('name', type=str, help='Votre nom')
       parser.add_argument('--upper', action='store_true', help='Affiche en majuscules')

    def handle(self, *args, **options):
        name = options['name']
        message = f"Bonjour {name}, bienvenue dans le monde des commandes Django!"

        if options['upper']:
            message = message.upper()

        self.stdout.write(self.style.SUCCESS(message))

        
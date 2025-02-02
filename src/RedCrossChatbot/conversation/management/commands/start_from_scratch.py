from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand

from conversation.models import Conversation, ConversationLine


class Command(BaseCommand):
    help = 'Wipes the database, runs all migrations, and creates a superuser.'

    def handle(self, *args, **kwargs):
        # Run migrations
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS('Migrations applied successfully.'))

        # Create superuser
        username = 'admin'
        email = 'admin@example.com'
        try:
            User.objects.create_superuser(username=username, email=email, password='admin')
            self.stdout.write(
                self.style.SUCCESS(f'Superuser created successfully. Username: {username}, Email: {email}'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Superuser already exists. {e}'))

        # Create a dummy conversation
        convo, _ = Conversation.objects.get_or_create(user='Erwin')
        initial_prompt = 'Where can I sleep tonight?'
        initial_response = ('You can potentially stay at the night shelter; more information is available '
                            '[here](https://helpfulinformation.redcross.nl/den-haag/shelter/night-shelter).')
        ConversationLine.objects.bulk_create([
            ConversationLine(conversation=convo, speaker='user', text=initial_prompt),
            ConversationLine(conversation=convo, speaker='bot', text=initial_response),
        ])

        # Run the server
        call_command('runserver')

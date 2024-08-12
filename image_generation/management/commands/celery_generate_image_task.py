from django.core.management.base import BaseCommand
from ...task import generate_image_task

class Command(BaseCommand):
    help = 'Generate image'

    def handle(self, *args, **options):
        generate_image_task.delay()
        
        self.stdout.write(self.style.SUCCESS('successfully!'))

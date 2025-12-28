from django.core.management.base import BaseCommand
from django.db import transaction
from cv_app.models import CVTemplate, CV

class Command(BaseCommand):
    help = 'Fix template foreign key constraints and create default templates'

    def handle(self, *args, **options):
        with transaction.atomic():
            # 1. First create the default templates
            templates_data = [
                {
                    'id': 1,
                    'name': 'Modern Professional',
                    'description': 'Clean, modern design with balanced sections',
                    'primary_color': '#2c3e50',
                    'secondary_color': '#3498db',
                    'accent_color': '#e74c3c',
                    'font_family': 'Arial, sans-serif',
                    'layout_style': 'modern'
                },
                {
                    'id': 2,
                    'name': 'Classic Executive',
                    'description': 'Traditional layout for corporate roles',
                    'primary_color': '#1a1a1a',
                    'secondary_color': '#666666',
                    'accent_color': '#8b4513',
                    'font_family': 'Georgia, serif',
                    'layout_style': 'classic'
                },
                {
                    'id': 3,
                    'name': 'Creative Portfolio',
                    'description': 'Modern design for creative professionals',
                    'primary_color': '#2980b9',
                    'secondary_color': '#e67e22',
                    'accent_color': '#27ae60',
                    'font_family': 'Helvetica Neue, sans-serif',
                    'layout_style': 'creative'
                },
                {
                    'id': 4,
                    'name': 'Minimal Clean',
                    'description': 'Simple, clean design focused on content',
                    'primary_color': '#333333',
                    'secondary_color': '#666666',
                    'accent_color': '#999999',
                    'font_family': 'Arial, sans-serif',
                    'layout_style': 'minimal'
                }
            ]

            # Create templates with specific IDs
            for template_data in templates_data:
                template, created = CVTemplate.objects.get_or_create(
                    id=template_data['id'],
                    defaults=template_data
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created template: {template.name} (ID: {template.id})'))
                else:
                    self.stdout.write(self.style.WARNING(f'Template exists: {template.name} (ID: {template.id})'))

            # 2. Update existing CVs to use template 1
            updated_cvs = CV.objects.filter(template__isnull=True).update(template_id=1)
            self.stdout.write(self.style.SUCCESS(f'Updated {updated_cvs} CVs to use default template'))

        self.stdout.write(self.style.SUCCESS('Successfully fixed template constraints!'))
from django.core.management.base import BaseCommand
from cv_app.models import CVTemplate

class Command(BaseCommand):
    help = 'Create default CV templates'

    def handle(self, *args, **options):
        templates = [
            {
                'name': 'Modern Professional',
                'description': 'Clean, modern design with balanced sections',
                'primary_color': '#2c3e50',
                'secondary_color': '#3498db',
                'accent_color': '#e74c3c',
                'font_family': 'Arial, sans-serif',
                'layout_style': 'modern'
            },
            {
                'name': 'Classic Executive',
                'description': 'Traditional layout for corporate roles',
                'primary_color': '#1a1a1a',
                'secondary_color': '#666666',
                'accent_color': '#8b4513',
                'font_family': 'Georgia, serif',
                'layout_style': 'classic'
            },
            {
                'name': 'Creative Portfolio',
                'description': 'Modern design for creative professionals',
                'primary_color': '#2980b9',
                'secondary_color': '#e67e22',
                'accent_color': '#27ae60',
                'font_family': 'Helvetica Neue, sans-serif',
                'layout_style': 'creative'
            },
            {
                'name': 'Minimal Clean',
                'description': 'Simple, clean design focused on content',
                'primary_color': '#333333',
                'secondary_color': '#666666',
                'accent_color': '#999999',
                'font_family': 'Arial, sans-serif',
                'layout_style': 'minimal'
            }
        ]

        created_count = 0
        for template_data in templates:
            template, created = CVTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults=template_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created template: {template.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Template already exists: {template.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} templates')
        )
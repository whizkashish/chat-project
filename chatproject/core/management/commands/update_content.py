# your_app/management/commands/update_database.py
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from blog.models import Blog
from openai import OpenAI

class Command(BaseCommand):
    help = 'Updates database content using OpenAI script'

    def handle(self, *args, **options):
        client = OpenAI()
        client = OpenAI(
        organization='org-dNsTs2MVDj2qpdFukgX0NCdC',
        project='proj_g89lMJEW916GGeoiqKyecVwU',
        )
        blog_post = get_object_or_404(Blog,id=2)
        # Example prompt for OpenAI
        prompt = f"This is a chinese novel convert to indian characters with indian locations use indian history as well.{blog_post.content}"
        # Generate content using OpenAI
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ]
        )

        print(completion.choices[0].message)

import openai
import json
from django.conf import settings
from django.utils.text import slugify
from .models import ResumeTemplate

openai.api_key = settings.OPENAI_API_KEY


def generate_resume_template(name, category, description=None):
    """
    Generate a resume template using OpenAI's API
    """
    if not description:
        description = f"A {category} resume template"

    prompt = f"""
    Create a professional resume template with the following details:
    - Name: {name}
    - Category: {category}
    - Description: {description}

    Please provide:
    1. HTML structure with placeholders for dynamic content
    2. CSS styles that make the template look professional

    Return the result as a JSON object with the following structure:
    {{
        "html_structure": "...",
        "css_styles": "..."
    }}
    """

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=2000,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        result = json.loads(response.choices[0].text.strip())

        # Create the template
        template = ResumeTemplate(
            name=name,
            slug=slugify(name),
            description=description,
            category=category,
            html_structure=result['html_structure'],
            css_styles=result['css_styles']
        )

        # You would need to handle the preview image separately

        template.save()
        return template

    except Exception as e:
        print(f"Error generating template: {e}")
        return None
from pathlib import Path
from functools import cache
from importlib import import_module
from image_generator.base.base_image_generator import BaseImageGenerator


@cache
def create_image_generator(model, api_key):
    generator_package = f'image_generator.generators.{model}_image_generator'
    generator_class = f'{model.capitalize()}ImageGenerator'

    try:
        package = import_module(generator_package)
        generator = getattr(package, generator_class)
    except (ImportError, AttributeError):
        raise ValueError(f'Generator for model {model} not found.')

    return generator(model, api_key)


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()

    generator = create_image_generator(
        model='doubao',
        api_key=os.getenv('ARK_API_KEY'),
    )
    print(generator)
    
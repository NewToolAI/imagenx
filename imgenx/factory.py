from pathlib import Path
from functools import cache
from importlib import import_module
from imgenx.image_generator.base.base_image_generator import BaseImageGenerator


@cache
def create_image_generator(model: str, api_key: str) -> BaseImageGenerator:
    provider, model = model.split(':')

    if provider not in get_providers():
        raise ValueError(f'Provider {provider} not found.')

    generator_package = f'imgenx.image_generator.generators.{provider}_image_generator'
    generator_class = f'{provider.capitalize()}ImageGenerator'

    try:
        package = import_module(generator_package)
        generator = getattr(package, generator_class)
    except (ImportError, AttributeError):
        raise ValueError(f'Provider {provider} not found.')

    return generator(model, api_key)


@cache
def get_providers():
    providers = []
    for path in (Path(__file__).parent / 'image_generator/generators').glob('*_image_generator.py'):
        providers.append(path.stem.split('_')[0])

    return providers

from pathlib import Path
from functools import cache
from importlib import import_module


@cache
def create_text_to_image(model: str, api_key: str):
    return create_predictor(model, api_key, 'text_to_image')


@cache
def create_image_to_image(model: str, api_key: str):
    return create_predictor(model, api_key, 'image_to_image')


@cache
def create_text_to_video(model: str, api_key: str):
    return create_predictor(model, api_key, 'text_to_video')


@cache
def create_image_to_video(model: str, api_key: str):
    return create_predictor(model, api_key, 'image_to_video')


@cache
def create_image_inspector(model: str, api_key: str):
    return create_predictor(model, api_key, 'image_inspector')


def create_predictor(model: str, api_key: str, role: str):
    provider, model = model.split(':')
    provider = provider.lower()

    if provider not in get_providers():
        raise ValueError(f'Provider {provider} not found.')

    predictor_package = f'imagenx.predictor.generators.{provider}.{role.lower()}'
    role_parts = [p.capitalize() for p in role.split('_')]
    predictor_class = f'{provider.capitalize()}{"".join(role_parts)}'

    try:
        package = import_module(predictor_package)
        predictor = getattr(package, predictor_class)
    except (ImportError, AttributeError):
        raise ValueError(f'Provider {provider} not found.')

    return predictor(model, api_key)


@cache
def get_providers():
    root = Path(__file__).parent / 'predictor/generators'
    return [p.name for p in root.iterdir() if p.is_dir()]

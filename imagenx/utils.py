def get_provider_model_api_key(task, headers, env):
    task = task.strip()

    try:
        headers = {key.lower(): value for key, value in headers.items()}
        env = {key.lower(): value for key, value in env.items()}

        provider_model_name = f'imagenx_{task}'
        provider_model = headers.get(provider_model_name, env.get(provider_model_name))
        provider, model = provider_model.split(':')
    except Exception as e:
        provider = None
    
    api_key = headers.get(f'imagenx_{provider}_api_key', env.get(f'imagenx_{provider}_api_key'))

    return provider_model, api_key


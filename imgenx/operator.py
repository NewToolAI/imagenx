import re
from pathlib import Path
from io import BytesIO

import requests
from PIL import Image, ImageEnhance


def download_image(url: str, output: str):
    output = Path(output)
    if output.exists():
        raise FileExistsError(f'Path {output} already exists.')

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except Exception as e:
        raise requests.RequestException(f'Error: {e}')

    output.write_bytes(response.content)


def get_image_info(image: str) -> str:
    try:
        img = _load_image(image)
    except Exception as e:
        raise ValueError(f'Error loading image: {e}')

    info = {
        'format': str(img.format),
        'size': f"{img.width}x{img.height}",
        'mode': img.mode,
        'file_size': _format_file_size(len(img.tobytes()))
    }
    return info


def crop_image(image: str, box: str, output: str):
    try:
        x, y, w, h = map(int, box.split(','))
    except Exception:
        raise ValueError('box must be "x,y,width,height" integers')

    img = _load_image(image)

    x = max(0, x)
    y = max(0, y)
    w = max(1, w)
    h = max(1, h)
    right = min(img.width, x + w)
    bottom = min(img.height, y + h)
    cropped = img.crop((x, y, right, bottom))

    _save_image(cropped, output)


def resize_image(image: str, size: str, output: str, keep_aspect: bool = True):
    m = re.match(r'^(\d+)x(\d+)$', size)
    if not m:
        raise ValueError('size must be WIDTHxHEIGHT, e.g., "1024x768"')

    w, h = map(int, m.groups())

    img = _load_image(image)
    if keep_aspect:
        resized = img.copy()
        resized.thumbnail((w, h), Image.Resampling.LANCZOS)
    else:
        resized = img.resize((w, h), Image.Resampling.LANCZOS)

    _save_image(resized, output)


def convert_image(image: str, format: str, output: str, quality: int = 90):
    fmt = format.upper()
    if fmt not in ('PNG', 'JPEG', 'JPG', 'WEBP'):
        raise ValueError('format must be one of PNG/JPEG/JPG/WEBP')

    img = _load_image(image)
    _save_image(img, output, format_hint=fmt, quality=quality)


def adjust_image(image: str, output: str, brightness: float = 1.0, contrast: float = 1.0, saturation: float = 1.0):
    img = _load_image(image)
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Color(img).enhance(saturation)

    _save_image(img, output)


def _load_image(image: str) -> Image.Image:
    if re.match(r'^https?://', image):
        try:
            resp = requests.get(image, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise requests.RequestException(f'Error: {e}')
        return Image.open(BytesIO(resp.content)).convert('RGBA')

    path = Path(image)
    if not path.exists():
        raise FileNotFoundError(f'Image not found: {image}')
    return Image.open(path)


def _save_image(img: Image.Image, output: str, format_hint: str | None = None, quality: int = 90) -> None:
    out = Path(output)
    if out.exists():
        raise FileExistsError(f'Path {out} already exists.')
    out.parent.mkdir(parents=True, exist_ok=True)

    fmt = format_hint or (out.suffix[1:].upper() if out.suffix else 'PNG')
    
    if fmt.upper() == 'JPG':
        fmt = 'JPEG'
    
    save_kwargs = {}

    if fmt.upper() in ('JPEG', 'WEBP'):
        save_kwargs['quality'] = quality

    if fmt.upper() == 'JPEG':
        img = img.convert('RGB')

    img.save(out, format=fmt, **save_kwargs)


def _format_file_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

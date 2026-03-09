from googletrans import Translator
from config import lang

translator = Translator()
cache = {}
CACHE_LIMIT = 10000

def translate(text: str, language: str) -> str:
    if not text:
        return text

    if len(text) < 4:
        return text

    target_lang = language or lang

    if target_lang == "en":
        return text

    normalized = text.strip().lower()
    key = f"{target_lang}:{normalized}"

    cached = cache.get(key)
    if cached is not None:
        return cached

    try:
        translated = translator.translate(text, dest=target_lang).text
    except Exception:
        return text

    cache[key] = translated

    if len(cache) > CACHE_LIMIT:
        cache.clear()

    return translated
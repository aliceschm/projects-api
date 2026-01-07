# Detected language from api header to return data from selected language only
from fastapi import Header

SUPPORTED_LANGS = {"pt", "en", "es"}
DEFAULT_LANG = "pt"


def get_language(accept_language: str = Header(default=DEFAULT_LANG)):
    # Format accepted language in case is sent by browser in another format (pt-BR)
    lang = accept_language.split(",")[0].lower()
    lang = lang.split("-")[0]

    if lang not in SUPPORTED_LANGS:
        lang = DEFAULT_LANG

    return lang

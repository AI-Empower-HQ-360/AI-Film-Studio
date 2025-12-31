"""
Multi-language i18n Configuration for AI Film Studio

This module provides internationalization (i18n) support for the platform,
enabling content translation across 20+ languages.
"""

# Supported languages with their codes
SUPPORTED_LANGUAGES = {
    # European Languages
    "en": {"name": "English", "native": "English", "rtl": False},
    "es": {"name": "Spanish", "native": "Español", "rtl": False},
    "fr": {"name": "French", "native": "Français", "rtl": False},
    "de": {"name": "German", "native": "Deutsch", "rtl": False},
    "pt": {"name": "Portuguese", "native": "Português", "rtl": False},
    "it": {"name": "Italian", "native": "Italiano", "rtl": False},
    "ru": {"name": "Russian", "native": "Русский", "rtl": False},
    
    # Indian Languages
    "hi": {"name": "Hindi", "native": "हिन्दी", "rtl": False},
    "ta": {"name": "Tamil", "native": "தமிழ்", "rtl": False},
    "te": {"name": "Telugu", "native": "తెలుగు", "rtl": False},
    "bn": {"name": "Bengali", "native": "বাংলা", "rtl": False},
    "mr": {"name": "Marathi", "native": "मराठी", "rtl": False},
    "gu": {"name": "Gujarati", "native": "ગુજરાતી", "rtl": False},
    "kn": {"name": "Kannada", "native": "ಕನ್ನಡ", "rtl": False},
    "ml": {"name": "Malayalam", "native": "മലയാളം", "rtl": False},
    "pa": {"name": "Punjabi", "native": "ਪੰਜਾਬੀ", "rtl": False},
    
    # Asian Languages
    "ja": {"name": "Japanese", "native": "日本語", "rtl": False},
    "zh": {"name": "Chinese", "native": "中文", "rtl": False},
    "ko": {"name": "Korean", "native": "한국어", "rtl": False},
    
    # Middle Eastern
    "ar": {"name": "Arabic", "native": "العربية", "rtl": True},
}

# Voice synthesis language mappings
# Maps language codes to available voice providers and voice IDs
VOICE_LANGUAGE_MAPPING = {
    "en": {
        "provider": "elevenlabs",
        "voices": {
            "male": ["adam", "josh", "arnold"],
            "female": ["rachel", "domi", "bella"],
            "child": ["charlie"]
        }
    },
    "es": {
        "provider": "elevenlabs",
        "voices": {
            "male": ["diego", "carlos"],
            "female": ["sophia", "maria"]
        }
    },
    "hi": {
        "provider": "openai",
        "voices": {
            "male": ["alloy", "echo"],
            "female": ["nova", "shimmer"]
        }
    },
    "fr": {
        "provider": "elevenlabs",
        "voices": {
            "male": ["antoine"],
            "female": ["charlotte"]
        }
    },
    # Add more language mappings as needed
}

# Translation API configuration
TRANSLATION_CONFIG = {
    "primary_provider": "google_translate",
    "fallback_provider": "deepl",
    "cache_translations": True,
    "cache_ttl_seconds": 86400  # 24 hours
}

# Cultural content mapping
# Maps cultural contexts to appropriate content and styling
CULTURAL_CONTENT = {
    "hindu": {
        "music_styles": ["indian_classical", "devotional", "bhajan"],
        "visual_styles": ["traditional_indian", "temple_architecture"],
        "audio_library": ["vedic_chants", "slokas", "sahasranamas"],
        "clothing": ["traditional_indian", "silk_sarees", "dhoti"]
    },
    "western": {
        "music_styles": ["orchestral", "cinematic", "jazz"],
        "visual_styles": ["modern", "classical_european"],
        "audio_library": ["classical_music", "contemporary"],
        "clothing": ["modern_western", "formal"]
    },
    "buddhist": {
        "music_styles": ["meditation", "tibetan_chants"],
        "visual_styles": ["zen", "temple_architecture"],
        "audio_library": ["mantras", "meditation_bells"],
        "clothing": ["robes", "traditional"]
    },
    "islamic": {
        "music_styles": ["nasheed", "qawwali"],
        "visual_styles": ["islamic_architecture", "geometric_patterns"],
        "audio_library": ["quranic_recitation", "adhaan"],
        "clothing": ["traditional_islamic", "modest"]
    }
}

# Language-specific formatting
LANGUAGE_FORMATTING = {
    "date_format": {
        "en": "MM/DD/YYYY",
        "de": "DD.MM.YYYY",
        "ja": "YYYY/MM/DD",
        "hi": "DD/MM/YYYY"
    },
    "time_format": {
        "en": "12h",  # 12-hour format
        "de": "24h",  # 24-hour format
        "ja": "24h",
        "hi": "12h"
    },
    "number_format": {
        "en": {"decimal": ".", "thousands": ","},
        "de": {"decimal": ",", "thousands": "."},
        "hi": {"decimal": ".", "thousands": ","}
    }
}

# Default translations for common UI elements
DEFAULT_TRANSLATIONS = {
    "en": {
        "common": {
            "welcome": "Welcome to AI Film Studio",
            "login": "Login",
            "register": "Register",
            "logout": "Logout",
            "save": "Save",
            "cancel": "Cancel",
            "delete": "Delete",
            "edit": "Edit",
            "submit": "Submit"
        },
        "projects": {
            "create_project": "Create New Project",
            "my_projects": "My Projects",
            "project_title": "Project Title",
            "script": "Script",
            "generate_video": "Generate Video",
            "download": "Download Video"
        },
        "credits": {
            "credit_balance": "Credit Balance",
            "purchase_credits": "Purchase Credits",
            "subscription": "Subscription",
            "upgrade": "Upgrade Plan"
        }
    },
    "es": {
        "common": {
            "welcome": "Bienvenido a AI Film Studio",
            "login": "Iniciar sesión",
            "register": "Registrarse",
            "logout": "Cerrar sesión",
            "save": "Guardar",
            "cancel": "Cancelar",
            "delete": "Eliminar",
            "edit": "Editar",
            "submit": "Enviar"
        }
    },
    "hi": {
        "common": {
            "welcome": "एआई फिल्म स्टूडियो में आपका स्वागत है",
            "login": "लॉगिन करें",
            "register": "पंजीकरण करें",
            "logout": "लॉगआउट",
            "save": "सेव करें",
            "cancel": "रद्द करें",
            "delete": "हटाएं",
            "edit": "संपादित करें",
            "submit": "जमा करें"
        }
    }
    # Add more language translations as needed
}

def get_language_info(language_code: str) -> dict:
    """Get language information"""
    return SUPPORTED_LANGUAGES.get(language_code, SUPPORTED_LANGUAGES["en"])

def get_voice_config(language_code: str, gender: str = "male") -> dict:
    """Get voice configuration for language and gender"""
    lang_config = VOICE_LANGUAGE_MAPPING.get(language_code, VOICE_LANGUAGE_MAPPING["en"])
    voices = lang_config["voices"].get(gender, lang_config["voices"]["male"])
    
    return {
        "provider": lang_config["provider"],
        "voice_id": voices[0] if voices else "default",
        "language": language_code
    }

def get_cultural_content(cultural_context: str) -> dict:
    """Get cultural content configuration"""
    return CULTURAL_CONTENT.get(cultural_context, CULTURAL_CONTENT["western"])

def translate_text(text: str, target_language: str, source_language: str = "en") -> str:
    """
    Translate text to target language
    
    Args:
        text: Text to translate
        target_language: Target language code
        source_language: Source language code (default: en)
    
    Returns:
        Translated text
    """
    # TODO: Implement actual translation using Google Translate or DeepL API
    # For now, return original text
    return text

def get_translation(key: str, language: str = "en", category: str = "common") -> str:
    """
    Get translation for a key
    
    Args:
        key: Translation key
        language: Language code
        category: Translation category (common, projects, credits, etc.)
    
    Returns:
        Translated string
    """
    lang_translations = DEFAULT_TRANSLATIONS.get(language, DEFAULT_TRANSLATIONS["en"])
    category_translations = lang_translations.get(category, {})
    return category_translations.get(key, key)

def format_date(date_obj, language: str = "en") -> str:
    """Format date according to language preferences"""
    date_format = LANGUAGE_FORMATTING["date_format"].get(language, "MM/DD/YYYY")
    # TODO: Implement actual date formatting
    return str(date_obj)

def format_number(number: float, language: str = "en") -> str:
    """Format number according to language preferences"""
    formatting = LANGUAGE_FORMATTING["number_format"].get(language, {"decimal": ".", "thousands": ","})
    # TODO: Implement actual number formatting
    return str(number)

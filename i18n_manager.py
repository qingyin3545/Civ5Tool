from i18n import zh_CN, en_US
from utils.config_manager import config
import locale

def get_start_language():
    # 启动时：优先读配置，否则用系统语言
    lang = config.get("general", "language")
    if lang == 'zh_CN' or lang == 'en_US':
        print("Read language from ini: ", lang)
    else:
        # 中文系统使用'zh_CN', 其余使用'en_US'
        lang, _ = locale.getdefaultlocale()
        print("Read language from system: ", lang)
        if lang and lang.lower().startswith("zh"):
            lang = "zh_CN"
        else:
            lang = "en_US"
    config.set("general", "language", lang)
    return lang

class I18N:
    _languages = {
        "zh_CN": zh_CN.STRINGS,
        "en_US": en_US.STRINGS,
    }

    current = get_start_language()

    @classmethod
    def set_language(cls, lang):
        if lang in cls._languages:
            cls.current = lang

    @classmethod
    def toggle(cls):
        cls.current = "en_US" if cls.current == "zh_CN" else "zh_CN"
        config.set("general", "language", cls.current)

    @classmethod
    def t(cls, key, **kwargs):
        text = cls._languages[cls.current].get(key, key)
        if kwargs:
            return text.format(**kwargs)
        return text
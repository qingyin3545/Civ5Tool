from i18n import zh_CN, en_US


class I18N:
    _languages = {
        "zh_CN": zh_CN.STRINGS,
        "en_US": en_US.STRINGS,
    }

    current = "zh_CN"

    @classmethod
    def set_language(cls, lang):
        if lang in cls._languages:
            cls.current = lang

    @classmethod
    def toggle(cls):
        cls.current = "en_US" if cls.current == "zh_CN" else "zh_CN"

    @classmethod
    def t(cls, key, **kwargs):
        text = cls._languages[cls.current].get(key, key)
        if kwargs:
            return text.format(**kwargs)
        return text
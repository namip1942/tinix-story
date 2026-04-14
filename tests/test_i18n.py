from locales.i18n import set_language, t


def test_translation_returns_value_for_existing_key():
    set_language("VI")
    value = t("app.title")
    assert isinstance(value, str)
    assert value
    assert value != "app.title"


def test_translation_falls_back_to_key_for_missing_key():
    set_language("VI")
    missing = "this.key.does.not.exist"
    assert t(missing) == missing

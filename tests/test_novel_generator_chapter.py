from types import SimpleNamespace

from services.novel_generator import NovelGenerator


class DummyAPIClient:
    def __init__(self):
        self.last_messages = None

    def generate(self, messages, use_cache=False):
        self.last_messages = messages
        return True, "ok"

    def generate_stream(self, messages):
        self.last_messages = messages
        yield True, "chunk"


def _build_generator(monkeypatch):
    gen = NovelGenerator.__new__(NovelGenerator)
    gen.config = SimpleNamespace(generation=SimpleNamespace(chapter_target_words=1200))
    gen.api_client = DummyAPIClient()
    gen._build_style_description = lambda: "STYLE_BASE"

    monkeypatch.setattr(
        "services.novel_generator.GenreManager.get_genre_description",
        lambda genre: "GENRE_DESC" if genre == "Fantasy" else "",
    )
    monkeypatch.setattr(
        "services.novel_generator.SubGenreManager.get_sub_genre_description",
        lambda sub: "SUB_DESC" if sub == "Adventure" else "",
    )
    return gen


def test_generate_chapter_includes_genre_and_subgenre_guidance_in_prompt(monkeypatch):
    gen = _build_generator(monkeypatch)

    content, _ = gen.generate_chapter(
        chapter_num=1,
        chapter_title="Mở đầu",
        chapter_desc="Giới thiệu bối cảnh",
        novel_title="Truyện thử nghiệm",
        character_setting="Nhân vật A",
        world_setting="Thế giới B",
        plot_idea="Hành trình",
        genre="Fantasy",
        sub_genres=["Adventure", "Mystery"],
    )

    assert content == "ok"
    user_prompt = gen.api_client.last_messages[1]["content"]
    assert "STYLE_BASE" in user_prompt
    assert "Hướng dẫn viết riêng cho thể loại Fantasy: GENRE_DESC" in user_prompt
    assert "- Adventure: SUB_DESC" in user_prompt
    assert "- Mystery" in user_prompt


def test_generate_chapter_stream_uses_same_style_enrichment(monkeypatch):
    gen = _build_generator(monkeypatch)

    chunks = list(
        gen.generate_chapter_stream(
            chapter_num=2,
            chapter_title="Tiếp diễn",
            chapter_desc="Mở rộng xung đột",
            novel_title="Truyện thử nghiệm",
            character_setting="Nhân vật A",
            world_setting="Thế giới B",
            plot_idea="Hành trình",
            genre="Fantasy",
            sub_genres=["Adventure"],
        )
    )

    assert chunks == [(True, "chunk")]
    user_prompt = gen.api_client.last_messages[1]["content"]
    assert "Hướng dẫn viết riêng cho thể loại Fantasy: GENRE_DESC" in user_prompt
    assert "- Adventure: SUB_DESC" in user_prompt

import io

from utils.file_parser import FileType, get_file_type, parse_txt_file


def test_get_file_type_detects_known_extensions():
    assert get_file_type("novel.txt") == FileType.TXT
    assert get_file_type("book.PDF") == FileType.PDF
    assert get_file_type("story.epub") == FileType.EPUB
    assert get_file_type("notes.md") == FileType.MD
    assert get_file_type("draft.docx") == FileType.DOCX


def test_get_file_type_handles_unknown_and_empty():
    assert get_file_type("") == FileType.UNKNOWN
    assert get_file_type("archive.zip") == FileType.UNKNOWN


def test_parse_txt_file_splits_paragraphs_and_filters_short_ones():
    # MIN_PARAGRAPH_LENGTH = 20, nên đoạn "Ngắn" sẽ bị loại.
    content = (
        "Đây là đoạn văn đầu tiên đủ dài để được giữ lại.\n"
        "Nó có thêm dòng thứ hai để kiểm tra ghép đoạn.\n\n"
        "Ngắn\n\n"
        "Đây là đoạn thứ hai cũng đủ độ dài để nằm trong kết quả.\n"
    )

    paragraphs, message = parse_txt_file(io.StringIO(content))

    assert len(paragraphs) == 2
    assert "Đây là đoạn văn đầu tiên" in paragraphs[0]
    assert "Đây là đoạn thứ hai" in paragraphs[1]
    assert isinstance(message, str) and message
    assert "2" in message

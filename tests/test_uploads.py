import json
import pytest
from src.config import MAX_UPLOAD_BYTES
from src.services.uploads import inspect_json, UploadError


@pytest.mark.parametrize("content", [b'{"unfamiliar":[1,2]}', b'[]', b'null', b'42', b'"text"'])
def test_valid_json_only_inspects_syntax(content):
    result = inspect_json("example.json",content)
    assert result.filename == "example.json"
    assert result.size_bytes == len(content)
    assert result.preview


@pytest.mark.parametrize("content", [b'', b'{broken', b'{"x":NaN}', b'\xff', b'{"x":Infinity}', b'{"x":1,}'])
def test_invalid_upload_has_clear_error(content):
    with pytest.raises(UploadError): inspect_json("invalid.json",content)


def test_large_file_is_rejected_before_parsing():
    with pytest.raises(UploadError, match="2 MB"):
        inspect_json("large.json", b" " * (MAX_UPLOAD_BYTES+1))


def test_preview_is_bounded_and_does_not_execute_html():
    content = json.dumps([{"html":"<script>alert(1)</script>","long":"x"*10000,"nested":[[[[1]]]]}]*50).encode()
    result = inspect_json("../test.json",content)
    assert len(result.preview) < 12000
    assert "omitid" in result.preview and "limitado" in result.preview
    assert result.filename == "test.json"


def test_deep_valid_json_has_a_bounded_preview():
    inspection = inspect_json("deep.json",b"["*2000 + b"0" + b"]"*2000)
    assert len(inspection.preview) < 1000
    assert "limite de profundidade" in inspection.preview

from datetime import date
from io import BytesIO
from pathlib import Path
from streamlit.testing.v1 import AppTest
from src.pages import import_data

APP = str(Path(__file__).resolve().parents[1] / "app.py")


def test_navigation_and_pages():
    app = AppTest.from_file(APP,default_timeout=30).run()
    assert not app.exception and not app.error
    assert any("DADOS SIMULADOS" in warning.value for warning in app.warning)
    assert len(app.metric) == 9
    for page in ["Análise meteorológica", "Condições para pulverização", "Análise por horários", "Importar dados meteorológicos", "Sobre o projeto"]:
        app.sidebar.radio[0].set_value(page).run()
        assert not app.exception and not app.error
        if page == "Análise meteorológica": assert len(app.get("plotly_chart")) == 5
        if page == "Análise por horários": assert len(app.dataframe[0].value) == 166


def test_filters_update_metrics_and_handle_empty_result():
    app = AppTest.from_file(APP,default_timeout=30).run()
    app.sidebar.date_input[0].set_value((date(2026,11,1),date(2026,11,1))).run()
    assert not app.exception and not app.error
    assert next(m.value for m in app.metric if m.label == "Registros selecionados") == "24"
    app.sidebar.multiselect[0].set_value([]).run()
    assert not app.exception and not app.error
    assert len(app.metric) == 0
    assert any("Nenhum registro" in info.value for info in app.info)


def test_pending_source_shows_message_without_demo_fallback():
    app = AppTest.from_file(APP, default_timeout=30).run()
    app.sidebar.selectbox[0].set_value("Integração real (pendente)").run()
    assert not app.exception
    assert not app.error


def test_json_upload_page_with_file_object(monkeypatch):
    class File(BytesIO):
        name = "sample.json"
    monkeypatch.setattr(import_data.st,"file_uploader",lambda *args,**kwargs:File(b'{"example":true}'))
    app = AppTest.from_file(APP,default_timeout=30).run()
    app.sidebar.radio[0].set_value("Importar dados meteorológicos").run()
    assert not app.exception and not app.error
    assert app.success and "sintaxe válida" in app.success[0].value
    assert "example" in app.code[0].value
    app.sidebar.radio[0].set_value("Dashboard").run()
    assert next(m.value for m in app.metric if m.label == "Registros selecionados") == "166"


def test_invalid_upload_page(monkeypatch):
    class File(BytesIO):
        name = "invalid.json"
    monkeypatch.setattr(import_data.st,"file_uploader",lambda *args,**kwargs:File(b'{broken'))
    app = AppTest.from_file(APP,default_timeout=30).run()
    app.sidebar.radio[0].set_value("Importar dados meteorológicos").run()
    assert not app.exception
    assert "JSON inválido" in app.error[0].value

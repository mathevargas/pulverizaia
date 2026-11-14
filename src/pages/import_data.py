import streamlit as st
from src.services.uploads import inspect_json, UploadError


def render():
    st.subheader("Importar dados meteorológicos")
    st.write("Verifique a estrutura e a sintaxe de um arquivo meteorológico em formato JSON.")
    st.info("Integração real indisponível nesta versão. O upload não altera o dashboard, não limpa dados e não presume os campos da empresa.")
    file = st.file_uploader("Selecione ou arraste um arquivo JSON", type=["json"], max_upload_size=2)
    st.caption("Até 2 MB · UTF-8 · Inspeção em memória nesta sessão · Nenhum arquivo é salvo no projeto")
    if file is None:
        return
    try:
        inspection = inspect_json(file.name, file.getvalue())
    except UploadError as exc:
        st.error(str(exc))
        return
    st.success("JSON com sintaxe válida. Isso não significa que o arquivo já é compatível com a aplicação.")
    a,b,c = st.columns(3)
    a.metric("Arquivo", inspection.filename)
    b.metric("Tamanho", f"{inspection.size_bytes:,} bytes")
    c.metric("Estrutura raiz", inspection.root_type)
    st.markdown("#### Prévia limitada")
    st.caption("Até 5 itens por nível, 3 níveis e 160 caracteres por texto. Campos e conteúdo podem ser omitidos da prévia.")
    st.code(inspection.preview, language="json")
    st.warning("Inspeção concluída. O arquivo não foi incorporado ao painel; essa etapa requer uma integração compatível com sua estrutura e unidades.")

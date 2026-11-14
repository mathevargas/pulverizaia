"""Inspeção sintática limitada. Não adapta, limpa, salva ou integra o JSON."""
import json
from dataclasses import dataclass
from pathlib import PureWindowsPath
from src.config import MAX_UPLOAD_BYTES


class UploadError(ValueError):
    pass


@dataclass(frozen=True)
class UploadInspection:
    filename: str
    size_bytes: int
    root_type: str
    preview: str


def _reject_constant(value):
    raise ValueError("Constante fora da sintaxe JSON: " + value)


def _bounded(value, depth=0):
    if depth >= 3 and isinstance(value, (dict, list)):
        return "[conteúdo omitido: limite de profundidade]"
    if isinstance(value, dict):
        entries = list(value.items())[:5]
        result = {str(k)[:100]: _bounded(v, depth + 1) for k, v in entries}
        if len(value) > 5:
            result["…"] = f"{len(value) - 5} campos omitidos"
        return result
    if isinstance(value, list):
        result = [_bounded(item, depth + 1) for item in value[:5]]
        if len(value) > 5:
            result.append(f"… {len(value) - 5} itens omitidos")
        return result
    if isinstance(value, str) and len(value) > 160:
        return value[:160] + "… [texto limitado]"
    return value


def inspect_json(filename: str, content: bytes):
    if not content:
        raise UploadError("O arquivo está vazio. Selecione um JSON com conteúdo.")
    if len(content) > MAX_UPLOAD_BYTES:
        raise UploadError("Arquivo maior que 2 MB. Selecione uma amostra menor para inspeção.")
    try:
        parsed = json.loads(content.decode("utf-8-sig"), parse_constant=_reject_constant)
    except UnicodeDecodeError as exc:
        raise UploadError("Codificação inválida. Utilize um arquivo JSON em UTF-8.") from exc
    except json.JSONDecodeError as exc:
        raise UploadError(f"JSON inválido: verifique a linha {exc.lineno}, coluna {exc.colno}.") from exc
    except (ValueError, RecursionError) as exc:
        raise UploadError("JSON inválido ou complexo demais para esta inspeção.") from exc
    root = "objeto" if isinstance(parsed, dict) else "lista" if isinstance(parsed, list) else "valor simples"
    return UploadInspection(
        filename=PureWindowsPath(filename).name[:200], size_bytes=len(content), root_type=root,
        preview=json.dumps(_bounded(parsed), ensure_ascii=False, indent=2)[:12000],
    )

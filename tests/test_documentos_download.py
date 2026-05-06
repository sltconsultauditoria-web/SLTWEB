from pathlib import Path
import tempfile

from bson import ObjectId

import backend.main_enterprise as app_module


def test_download_existing_document_returns_file_headers(client, admin_headers):
    response = client.get("/api/documentos/123/download", headers=admin_headers, follow_redirects=False)

    assert response.status_code == 200, response.text
    assert response.status_code not in {405, 500}
    assert response.headers["content-type"].startswith("application/pdf")
    assert "content-disposition" in response.headers
    assert "Documento 1.pdf" in response.headers["content-disposition"]
    assert response.content.startswith(b"%PDF")


def test_download_missing_document_returns_controlled_404(client, admin_headers):
    response = client.get(f"/api/documentos/{ObjectId()}/download", headers=admin_headers, follow_redirects=False)

    assert response.status_code == 404, response.text
    assert response.status_code not in {405, 500}


def test_download_document_without_content_type_does_not_500(client, app_db, admin_headers):
    base_tmp = Path(tempfile.gettempdir()) / "sltweb-tests"
    base_tmp.mkdir(parents=True, exist_ok=True)
    arquivo = base_tmp / "sem-content-type.bin"
    arquivo.write_bytes(b"conteudo sem content type")
    item_id = str(ObjectId())
    app_module.db["documentos"].insert_one(
        {
            "_id": ObjectId(item_id),
            "id": item_id,
            "nome_arquivo": "sem-content-type.bin",
            "caminho_arquivo": str(arquivo),
            "content_type": None,
            "tipo": None,
        }
    )

    response = client.get(f"/api/documentos/{item_id}/download", headers=admin_headers, follow_redirects=False)

    assert response.status_code == 200, response.text
    assert response.status_code != 500
    assert response.headers["content-type"].startswith("application/octet-stream")
    assert "content-disposition" in response.headers


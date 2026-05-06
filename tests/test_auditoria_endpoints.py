from pathlib import Path
import tempfile

from bson import ObjectId


def test_auditoria_list_stats_and_detail_are_serializable(client, admin_headers):
    list_response = client.get("/api/auditoria", headers=admin_headers, follow_redirects=False)
    assert list_response.status_code == 200, list_response.text
    assert list_response.status_code != 405
    assert isinstance(list_response.json()["data"], list)

    stats_response = client.get("/api/auditoria/estatisticas", headers=admin_headers, follow_redirects=False)
    assert stats_response.status_code == 200, stats_response.text
    assert stats_response.status_code != 405
    assert isinstance(stats_response.json()["data"], dict)

    detail_response = client.get("/api/auditoria/123", headers=admin_headers, follow_redirects=False)
    assert detail_response.status_code == 200, detail_response.text
    assert detail_response.status_code != 405
    assert isinstance(detail_response.json()["data"]["id"], str)


def test_missing_auditoria_returns_controlled_404(client, admin_headers):
    response = client.get(f"/api/auditoria/{ObjectId()}", headers=admin_headers, follow_redirects=False)
    assert response.status_code == 404, response.text
    assert response.status_code not in {405, 500}


def test_execute_auditoria_with_fake_db_never_returns_405_or_500(client, admin_headers):
    base_tmp = Path(tempfile.gettempdir()) / "sltweb-tests"
    base_tmp.mkdir(parents=True, exist_ok=True)
    arquivo = base_tmp / "auditoria_sped_teste.txt"
    arquivo.write_text("0000|1|SPED FISCAL|20260501|20260531|Empresa Teste|12345678000100\n9999|1", encoding="utf-8")

    with arquivo.open("rb") as handle:
        response = client.post(
            "/api/auditoria/executar",
            data={"cnpj": "12345678000100", "periodo": "2026-05", "tipo": "sped_fiscal"},
            files={"arquivo": (arquivo.name, handle, "text/plain")},
            headers=admin_headers,
            follow_redirects=False,
        )

    assert response.status_code == 200, response.text
    assert response.status_code not in {405, 500}
    payload = response.json()["data"]
    assert isinstance(payload["id"], str)
    assert "score_conformidade" in payload


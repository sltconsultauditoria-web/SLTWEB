import pytest


@pytest.mark.parametrize(
    "path",
    [
        "/api/obrigacoes",
        "/api/obrigacoes/dashboard",
        "/api/obrigacoes/calendario",
        "/api/obrigacoes/catalogo",
    ],
)
def test_obrigacoes_endpoints_return_json_200(client, admin_headers, path):
    response = client.get(path, headers=admin_headers, follow_redirects=False)

    assert response.status_code == 200, response.text
    assert response.status_code not in {404, 405}
    assert response.headers["content-type"].startswith("application/json")
    assert isinstance(response.json(), dict)


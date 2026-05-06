def test_admin_login_returns_token_and_me(client):
    login = client.post(
        "/api/auth/login",
        json={"email": "admin@empresa.com", "password": "admin123"},
        follow_redirects=False,
    )
    assert login.status_code == 200, login.text
    token = login.json()["data"]["token"]
    assert token

    me = client.get("/api/me", headers={"Authorization": f"Bearer {token}"}, follow_redirects=False)
    assert me.status_code == 200, me.text
    assert me.json()["data"]["role"] == "admin"


def test_protected_route_rejects_missing_token(client):
    response = client.get("/api/usuarios/viewers", follow_redirects=False)
    assert response.status_code == 401


def test_viewer_token_is_forbidden_on_admin_only_route(client, viewer_headers):
    response = client.get("/api/usuarios/viewers", headers=viewer_headers, follow_redirects=False)
    assert response.status_code == 403


def test_admin_token_can_access_admin_only_route(client, admin_headers):
    response = client.get("/api/usuarios/viewers", headers=admin_headers, follow_redirects=False)
    assert response.status_code == 200, response.text


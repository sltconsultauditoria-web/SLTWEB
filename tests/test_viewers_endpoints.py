from bson import ObjectId

import backend.main_enterprise as app_module


def test_get_viewers_auth_matrix(client, admin_headers, viewer_headers):
    cases = [
        ({}, 401),
        (viewer_headers, 403),
        (admin_headers, 200),
    ]

    for headers, expected in cases:
        response = client.get("/api/usuarios/viewers", headers=headers, follow_redirects=False)
        assert response.status_code == expected, response.text
        assert response.status_code != 405


def test_create_viewer_auth_matrix(client, admin_headers, viewer_headers):
    payload = {"email": "novo.viewer@empresa.com", "nome": "Novo Viewer", "password": "Viewer@2026"}

    no_token = client.post("/api/usuarios/viewers", json=payload, follow_redirects=False)
    assert no_token.status_code == 401
    assert no_token.status_code != 405

    forbidden = client.post(
        "/api/usuarios/viewers",
        json={**payload, "email": "blocked.viewer@empresa.com"},
        headers=viewer_headers,
        follow_redirects=False,
    )
    assert forbidden.status_code == 403
    assert forbidden.status_code != 405

    created = client.post("/api/usuarios/viewers", json=payload, headers=admin_headers, follow_redirects=False)
    assert created.status_code in {200, 201}, created.text
    assert created.status_code != 405
    assert created.json()["data"]["role"] == "viewer"


def test_update_and_delete_viewer_with_admin(client, admin_headers):
    created = client.post(
        "/api/usuarios/viewers",
        json={"email": "edicao.viewer@empresa.com", "nome": "Viewer", "password": "Viewer@2026"},
        headers=admin_headers,
        follow_redirects=False,
    )
    assert created.status_code in {200, 201}, created.text
    item_id = created.json()["data"]["id"]

    updated = client.put(
        f"/api/usuarios/viewers/{item_id}",
        json={"nome": "Viewer Editado"},
        headers=admin_headers,
        follow_redirects=False,
    )
    assert updated.status_code == 200, updated.text
    assert updated.status_code != 405
    assert updated.json()["data"]["nome"] == "Viewer Editado"

    deleted = client.delete(f"/api/usuarios/viewers/{item_id}", headers=admin_headers, follow_redirects=False)
    assert deleted.status_code in {200, 204}, deleted.text
    assert deleted.status_code != 405


def test_update_and_delete_missing_viewer_return_controlled_404(client, admin_headers):
    missing_id = str(ObjectId())

    updated = client.put(
        f"/api/usuarios/viewers/{missing_id}",
        json={"nome": "Inexistente"},
        headers=admin_headers,
        follow_redirects=False,
    )
    assert updated.status_code == 404, updated.text
    assert updated.status_code != 405

    deleted = client.delete(f"/api/usuarios/viewers/{missing_id}", headers=admin_headers, follow_redirects=False)
    assert deleted.status_code == 404, deleted.text
    assert deleted.status_code != 405


def test_viewer_endpoint_refuses_non_viewer_items_without_405(client, app_db, admin_headers):
    admin_id = str(ObjectId())
    app_module.db["usuarios"].insert_one(
        {
            "_id": ObjectId(admin_id),
            "email": "admin.item@empresa.com",
            "nome": "Admin Item",
            "role": "admin",
            "perfil": "admin",
            "senha_hash": "hash",
        }
    )

    response = client.put(
        f"/api/usuarios/viewers/{admin_id}",
        json={"nome": "Nao viewer"},
        headers=admin_headers,
        follow_redirects=False,
    )
    assert response.status_code == 409
    assert response.status_code != 405


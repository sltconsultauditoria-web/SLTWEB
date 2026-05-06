# SharePoint Graph Setup

## Variáveis necessárias

- `AZURE_TENANT_ID`
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`
- `SHAREPOINT_SITE_URL`
- `SHAREPOINT_SITE_ID`
- `SHAREPOINT_DRIVE_ID`
- `SHAREPOINT_LIBRARY_NAME`
- `SHAREPOINT_FOLDER_PATH`

## Comportamento

- `GET /api/sharepoint/status` informa se está configurado.
- `POST /api/sharepoint/sync` entra em `log_only` quando não configurado.
- `GET /api/sharepoint/files` e `GET /api/sharepoint/logs` exibem a trilha persistida.


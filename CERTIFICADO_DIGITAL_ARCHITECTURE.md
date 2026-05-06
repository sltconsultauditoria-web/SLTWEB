# Certificate Digital Architecture

## Diretriz

- A1 é o modelo viável para cloud.
- A3 não é recomendado para Render ou automação remota.
- Nunca salvar senha em texto puro.
- Nunca logar material de certificado.

## Providers

- `EnvCertificateProvider`
- `FileCertificateProvider`
- `VaultCertificateProvider`

## Requisitos

- Criptografia em repouso.
- Rotação.
- Auditoria.
- Acesso restrito por RBAC.


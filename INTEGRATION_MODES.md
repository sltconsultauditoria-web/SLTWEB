# Integration Modes

## Contract

```json
{
  "success": true,
  "provider": "ecac",
  "mode": "real|simulado|log_only|not_configured|not_implemented",
  "configured": true,
  "status": "ok|not_configured|error|simulado|log_only|not_implemented",
  "message": "...",
  "data": {},
  "missing_env_vars": [],
  "next_action": "..."
}
```

## Regras

- `401` sem token.
- `403` para ações sensíveis sem perfil adequado.
- `200` para consultas permitidas.
- Nunca apresentar simulação como se fosse integração real.


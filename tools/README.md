# tools/

Herramientas de desarrollo para este repositorio. No forman parte de la web publicada
(el sitio estático sigue siendo los `.html`/`.css`/`.js`/`data/` de la raíz).

## agent-reach

CLI de terceros ([Agent Reach](https://github.com/Panniantong/Agent-Reach)) que permite a un
agente de IA leer contenido de internet (web, RSS, YouTube, GitHub, etc.) para ayudar a
investigar o actualizar contenido de las rutas.

Instalación local (no se versiona el entorno virtual):

```bash
cd tools/agent-reach
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/agent-reach doctor
```

Por defecto no modifica el sistema ni sube credenciales a ningún sitio; solo tras
`agent-reach install --system` instala dependencias externas, y las cookies/tokens
quedan siempre en local (`~/.agent-reach/config.yaml`).

#!/usr/bin/env bash
set -euo pipefail

REPO_NAME="${1:-qgis_cpostal_tuga}"
VISIBILITY="${2:---public}"
DESCRIPTION="QGIS Processing plugin for Portuguese postal-code geocoding with cttcodigopostal.pt"

if ! command -v gh >/dev/null 2>&1; then
  echo "Erro: instale o GitHub CLI (gh) antes de publicar o repositório." >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "Erro: autentique o GitHub CLI com 'gh auth login' ou defina GH_TOKEN." >&2
  exit 1
fi

gh repo create "${REPO_NAME}" \
  "${VISIBILITY}" \
  --source "$(dirname "${BASH_SOURCE[0]}")" \
  --push \
  --description "${DESCRIPTION}"

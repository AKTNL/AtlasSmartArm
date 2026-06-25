#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../frontend"

if [ ! -d "node_modules" ]; then
  npm install
fi

export VITE_API_BASE_URL="${VITE_API_BASE_URL:-http://192.168.137.100:8080}"

npm run dev

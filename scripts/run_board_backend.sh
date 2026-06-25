#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -x ".venv/bin/python" ]; then
  python3 -m venv .venv
fi

.venv/bin/python -m pip install -r requirements.txt

export PROGRAM_MODE="${PROGRAM_MODE:-board}"
export ROBOT_ARM_ROOT="${ROBOT_ARM_ROOT:-/home/HwHiAiUser/E2ESamples/src/E2E-Sample/ros2_robot_arm}"

.venv/bin/python -m uvicorn src.backend.main:app --host 0.0.0.0 --port "${APP_PORT:-8080}"

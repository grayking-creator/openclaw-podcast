#!/bin/bash
set -e

echo "=== Bootstrapping M4 Max ==="
ssh m4max bash -s << 'EOF'
  set -e
  VENV_PATH="$HOME/.openclaw/workspace/video-workspace/crossfire-series/.venv"
  if [ ! -d "$VENV_PATH" ]; then
    echo "Error: M4 crossfire venv not found at $VENV_PATH"
    exit 1
  fi
  source "$VENV_PATH/bin/activate"
  echo "Installing moviepy, mlx-whisper, soundfile on M4 Max..."
  pip install --upgrade pip
  pip install moviepy mlx-whisper soundfile
  python -c "import moviepy; import mlx_whisper; import soundfile; print('M4 Max packages OK')"
EOF

echo "=== Bootstrapping DGX Spark ==="
ssh dgxspark bash -s << 'EOF'
  set -e
  VENV_PATH="$HOME/.venv_shorts"
  if [ ! -d "$VENV_PATH" ]; then
    echo "Creating new venv on DGX at $VENV_PATH..."
    python3 -m venv "$VENV_PATH"
  fi
  source "$VENV_PATH/bin/activate"
  echo "Installing dependencies on DGX Spark..."
  pip install --upgrade pip
  pip install moviepy openai-whisper soundfile Pillow numpy
  python -c "import moviepy; import whisper; import soundfile; import PIL; print('DGX Spark packages OK')"
EOF

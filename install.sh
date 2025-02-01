#!/bin/bash

# Create virtual environment
python3 -m venv ~/.ai-terminal

# Activate virtual environment
source ~/.ai-terminal/bin/activate

# Install the package
pip install -e .

# Create default config if it doesn't exist
mkdir -p ~/.config/ai-terminal
if [ ! -f ~/.config/ai-terminal/config.yaml ]; then
    cat > ~/.config/ai-terminal/config.yaml << EOL
llm:
  provider: "ollama"
  model: "deepseek-r1:8b"
  url: "http://localhost:11434/api/generate"
  api_key: ""
EOL
fi

# Create symlink to make it available system-wide
sudo ln -sf ~/.ai-terminal/bin/ait /usr/local/bin/ait

echo "Installation complete! You can now use the 'ait' command."
echo "Example: ait 'show system memory usage'" 
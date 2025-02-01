# AI Command Line Helper

A simple command-line tool that uses AI to suggest and execute shell commands based on natural language requests. You can choose to use either a local Ollama server or OpenAI's API.

## Description

This tool allows you to:
- Ask for commands in plain English
- Get AI-suggested commands based on your system
- Review the command before execution
- Execute commands safely with confirmation
- Choose between local Ollama or OpenAI's API

## Prerequisites

For Ollama (Local) option:
- Python 3.6 or higher
- Ollama installed and running locally

For OpenAI (Remote) option:
- Python 3.6 or higher
- OpenAI API key

## Installation

1. Clone the repository:
```
git clone <repository-url>
cd ai-command-helper
```

2. Run the installation script:
```
./install.sh
```

This will:
- Create a Python virtual environment at `~/.ai-terminal`
- Install required packages
- Create a default config file at `~/.config/ai-terminal/config.yaml`
- Make the `ait` command available system-wide

3. If using Ollama locally:
```
curl https://ollama.ai/install.sh | sh
ollama serve
```

4. Pull the model you want to use (in another terminal)
```
ollama pull deepseek-r1:8b
```

## Usage

1. Run the command:
```
ait "your request here"
```

For example:
```
ait "show me system memory usage"
```

2. Review the suggested command and its explanation

3. Confirm whether you want to execute the command (y/n)

4. Type 'exit' to quit the program

## Examples

Here are some example requests you can try:
- "show me system memory usage"
- "find all python files in current directory"
- "list files larger than 100MB"
- "check disk space usage"

## Configuration

You can modify config.yaml to:
- Choose the LLM provider (ollama or openai)
- Use a different model
- Change the API endpoint
- Add your OpenAI API key (if using OpenAI)

## Troubleshooting

For Ollama:
1. If Ollama isn't running:
```
ollama serve
```

2. If the model isn't installed:
```
ollama pull deepseek-r1:8b
```

3. If you get connection errors, check if Ollama is running and accessible at http://localhost:11434

For OpenAI:
1. Make sure your API key is correct in config.yaml
2. Check your internet connection
3. Verify your OpenAI account has available credits

## Safety Note

Always review commands before executing them, especially when they:
- Modify files or directories
- Require elevated privileges (sudo)
- Affect system settings

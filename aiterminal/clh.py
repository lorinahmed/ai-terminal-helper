#!/usr/bin/env python3

import os
import requests
import json
import subprocess
import platform
import psutil
from pathlib import Path
from importlib.metadata import distributions  
from datetime import datetime
import yaml
import sys

def get_system_info():
    """Gather relevant system information"""
    return {
        "os": platform.system(),
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "current_dir": os.getcwd(),
        "home_dir": str(Path.home()),
        "memory": {
            "total": psutil.virtual_memory().total // (1024 * 1024 * 1024),  # GB
            "available": psutil.virtual_memory().available // (1024 * 1024 * 1024)  # GB
        },
        "cpu_count": psutil.cpu_count()
    }


def load_config():
    """Load configuration from yaml file"""
    # Try user's config directory first
    config_path = Path.home() / '.config' / 'ai-terminal' / 'config.yaml'
    if not config_path.exists():
        # Try package directory
        config_path = Path(__file__).parent / 'config.yaml'
        if not config_path.exists():
            raise FileNotFoundError(
                "\n❌ Configuration file not found!"
                "\nPlease create a config file at either:"
                f"\n  - {Path.home() / '.config' / 'ai-terminal' / 'config.yaml'}"
                f"\n  - {Path(__file__).parent / 'config.yaml'}"
                "\n\nExample config.yaml content:"
                "\nllm:"
                '\n  provider: "ollama"'
                '\n  model: "deepseek-r1:8b"'
                '\n  url: "http://localhost:11434/api/generate"'
                '\n  api_key: ""'
            )
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            
            
        return config
            
    except yaml.YAMLError as e:
        raise ValueError(f"\n❌ Error parsing config file: {str(e)}")

def get_command(user_request, config):
    """Get command suggestion from LLM"""
    system_info = get_system_info()
    
    prompt = f"""
You are a helpful command-line assistant. Based on the following system information and user request, 
suggest a single command that would help accomplish the task.

System Information:
{json.dumps(system_info, indent=2)}

User Request: {user_request}

Provide your response in this format:
1. Brief explanation of what needs to be done
2. The exact command to run. The command should be ready to run. It should not require any additional input.
3. What the command will do

Be concise and direct.
"""
    if config['provider'] == 'ollama':
        response = requests.post(
            config['ollama']['url'],
            json={"model": config['ollama']['model'], "prompt": prompt, "stream": False, "format": {
                "type": "object",
                "properties": {
                    "command": {"type": "string"},
                    "explanation": {"type": "string"},
                    "type": {"type": "string"}
                },
                "required": ["command", "explanation", "type"]
            }}
        )

    #print("Response: ", response.json()['response'])
        try:
            command_data = json.loads(response.json()['response'])
            return command_data.get('command', '')
        except (json.JSONDecodeError, KeyError):
            return "Error: Failed to parse command from response"
    elif config['provider'] == 'openai':
        response = requests.post(
            config['openai']['url'],
            headers={"Authorization": f"Bearer {config['openai']['api_key']}"},
            json={
                "model": config['openai']['model'],
                "messages": [{"role": "user", "content": prompt}],
                "response_format": { 
                    "type": "json_schema", 
                    "json_schema": {
                      "name": "command_data",
                      "strict": True,
                      "schema": {
                        "type": "object",
                        "properties": {
                            "command": {"type": "string"},
                            "explanation": {"type": "string"},
                            "type": {"type": "string"}
                        },
                        "required": ["command", "explanation", "type"],
                        "additionalProperties": False
                      }
                    }
                }
                }

        )
        print("Response: ", response.json())
        content = response.json()['choices'][0]['message']['content']
        command_data = json.loads(content)
        return command_data['command']
    
    else:
        raise ValueError(f"Unsupported LLM provider: {config['provider']}")


def execute_command(command):
    """Execute the command and return result"""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def main():
    # Check if a request was provided
    if len(sys.argv) < 2:
        print("Usage: python clh.py 'your request here'")
        print("Example: python clh.py 'show me large files in current directory'")
        sys.exit(1)
    
    # Get the request from command line arguments
    user_request = ' '.join(sys.argv[1:])
    
    try:
        config = load_config()
        
        # Prepare prompt with system info
        prompt = f"""
You are a helpful command-line assistant. Based on the following system information and user request, 
suggest a single command that would help accomplish the task.

System Information:
{json.dumps(get_system_info(), indent=2)}

User Request: {user_request}

Provide your response in this format:
1. Brief explanation of what needs to be done
2. The exact command to run (starting with $ or >)
3. What the command will do

Be concise and direct.
"""
        
        # Get command suggestion
        print("\n🤔 Let me suggest a command...")
        suggestion = get_command(user_request, config)
        print(f"\n{suggestion}")
        
        # Ask for confirmation
        confirm = input("\n❓ Would you like me to run this command? (y/n): ").lower().strip()
        if confirm == 'y':
            # Extract the command from the suggestion
            for line in suggestion.split('\n'):
                command = line.strip()
                if line.strip().startswith(('$', '>')):
                    command = line.strip()[1:].strip()
                print(f"\n🚀 Running command: {command}")
                result = execute_command(command)
                
                if result["success"]:
                    print("\n✅ Command executed successfully!")
                    if result["output"]:
                        print("\nOutput:")
                        print(result["output"])
                else:
                    print("\n❌ Command failed!")
                    print(f"Error: {result['error']}")
                break
        else:
            print("\n⏭️  Command execution cancelled.")
                
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please check your configuration and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()

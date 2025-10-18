# DeepSeek CLI

A terminal-based client for the DeepSeek API that allows you to have conversations directly from your terminal.

## Features

- Real-time streaming responses
- Conversation history management
- Command support (clear, reset, history, exit)
- Readline support for better input editing
- Persistent conversation history between sessions

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/deepseek_cli.git
   cd deepseek_cli
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your DeepSeek API key as an environment variable:
   ```bash
   export DEEPSEEK_API_KEY='your-api-key'
   ```

## Usage

Run the client:
```bash
python src/deepseek_cli.py
```

Or if installed as a package:
```bash
deepseek-cli
```

### Commands

- `exit` or `quit`: Exit the program
- `clear` or `reset`: Clear conversation history
- `history`: View current conversation history

## Requirements

- Python 3.8 or higher
- openai Python package
- readline (usually included with Python)

## License

This project is licensed under the MIT License.
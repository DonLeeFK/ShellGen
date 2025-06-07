# ShellGen: Your CLI Command Helper
Tired of guessing shell commands? ShellGen turns your English descriptions into ready-to-run terminal commands!
## What it does
1. Describe what you want to do:
   `"find large image files modified last week"`
2. Get a generated command:
   `find . -name "*.jpg" -size +1M -mtime -7`
3. Automatically copied to your clipboard 📋
## Get Started
1. fork and clone the repository
2. Install requirements
   ```bash
   pip install openai python-dotenv
   ```
3. Get an OpenAI API key, or any other LLM provider of your liking
4. Create .env file:

```<ENV>
API_KEY="your-api-key-here"
BASE_URL="api.openai.com"
MODEL="model_of_your_choice"
```
## How I would use it
1. Open your shell config

```<BASH>
# For Bash users:
nano ~/.bashrc

# For Zsh users:
nano ~/.zshrc
```
2. Add this line to the file
```
alias cmd="python3 /path/to/shellgen.py"
```
3. Refrensh your shell
```<BASH>
# For Bash users:
source ~/.bashrc

# For Zsh users:
source ~/.zshrc
```

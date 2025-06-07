#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
from pathlib import Path
import openai
from dotenv import load_dotenv  # Add this import

def get_os_version():
    system = platform.system()
    if system == 'Darwin':  # macOS
        # Format as "macOS 12.6"
        return f"Darwin/macOS{platform.mac_ver()[0]}"

    elif system == 'Windows':
        # For Windows 10/11 detection
        release = platform.release()
        version = platform.version()

        if release == '10':
            if int(version.split('.')[2]) >= 22000:
                return "Windows 11"
            else:
                return "Windows 10"
        return f"Windows {release}"

    elif system == 'Linux':
        # For common Linux distributions
        dist = platform.freedesktop_os_release()
        return f"Linux/{dist['NAME']}{dist['VERSION_ID']}"

    return platform.platform()  # Fallback for other systems


def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard using platform-specific methods"""
    system = platform.system()

    try:
        if system == "Darwin":  # macOS
            subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
            return True
        elif system == "Windows":
            subprocess.run(["clip.exe"], input=text.encode("utf-16"), check=True)
            return True
        elif system == "Linux":
            # Try xclip first, then xsel
            try:
                subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode("utf-8"), check=True)
                return True
            except (FileNotFoundError, subprocess.CalledProcessError):
                subprocess.run(["xsel", "--clipboard"], input=text.encode("utf-8"), check=True)
                return True
        else:
            print(f"\n⚠️ Unsupported platform: {system}", file=sys.stderr)
            return False
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"\n⚠️ Clipboard error: {str(e)}", file=sys.stderr)
        return False

def generate_shell_command(description: str) -> str:
    """
    Generates shell command from natural language description using OpenAI API
    """
    # Load environment variables from .env file
    env_path = Path(__file__).parent / ".env"
    load_dotenv(dotenv_path=env_path)

    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")
    model = os.getenv("MODEL")
    if not api_key:
        raise ValueError("API_KEY not found in .env file")
    if not base_url:
        raise ValueError("BASE_URL not found in .env file")
    if not model:
        raise ValueError("MODEL not found in .env file")
    os_version = get_os_version()

    client = openai.OpenAI(api_key=api_key, base_url=base_url)


    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Shell Command Generator "
                    f"Provide only zsh commands for {os_version}."
                    "Output ONLY the command itself without any explanations, quotes"
                    "If the request is impossible or unclear, return 'ERROR: ' followed by a brief reason."
                )
            },
            {"role": "user", "content": description}
        ],
        temperature=0,
        stream=True,

        #max_tokens=100
    )
    full_response = ""
    print("Generating command: ", end="\n\n", flush=True)

    try:
        # Process streaming response
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                # Print each token as it arrives
                print(content, end="", flush=True)
                full_response += content
    except KeyboardInterrupt:
        print("\n\nGeneration interrupted by user", file=sys.stderr)
        sys.exit(1)

    print("\n", end="", flush=True)  # Final newline after stream
    return full_response.strip()

if __name__ == "__main__":
    description = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None

    if not description:
        print("Usage: shellgen <command description>")
        print("Example: shellgen list all files larger than 1MB in current directory")

        sys.exit(1)

    try:
        command = generate_shell_command(description)
        #print(command)

        # Copy to clipboard on macOS
        if copy_to_clipboard(command):
            print("\n✅ Command copied to clipboard!", file=sys.stderr)
        else:
            print("\n⚠️ Failed to copy to clipboard (pbcopy not available)", file=sys.stderr)

    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

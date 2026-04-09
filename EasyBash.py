#!/usr/bin/env python3

import subprocess
import shlex
import sys
from pathlib import Path

# Constants
EASY_BASH_COMMANDS = {"for", "rush", "exit"}

def parse_command(text):
    """Parse and validate command from user input"""
    if not text or not text.strip():
        return None, []
    
    # Use shlex for proper tokenization (handles quotes)
    try:
        cmd_parts = shlex.split(text)
    except ValueError as e:
        print(f"Error parsing command: {e}")
        return None, []
    
    if not cmd_parts:
        return None, []
    
    command = cmd_parts[0]
    return command if command in EASY_BASH_COMMANDS else None, cmd_parts

def validate_paths(paths_str):
    """Validate and return list of existing paths"""
    paths = [p.strip() for p in paths_str.split('|') if p.strip()]
    valid_paths = []
    
    for path in paths:
        path_obj = Path(path).expanduser().resolve()
        if path_obj.exists() and path_obj.is_dir():
            valid_paths.append(str(path_obj))
        else:
            print(f"Warning: Path '{path}' does not exist or is not a directory")
    
    return valid_paths

def execute_bash_command(bash_command):
    """Execute bash command safely"""
    try:
        print(f"Generated: {bash_command}")
        result = subprocess.run(
            bash_command, 
            shell=True, 
            executable='/bin/bash',
            text=True,
            capture_output=False
        )
        return result.returncode
    except Exception as e:
        print(f"Error executing command: {e}")
        return 1

def for_easy_bash_command(cmd_parts):
    """
    Syntax: for (file) in (path1|path2|path3) (bash command)
    Example: for test.txt in /tmp|/home "ls -la"
    """
    if len(cmd_parts) < 5:
        print("Error: Invalid syntax")
        print("Usage: for (filename) in (path1|path2|path3) (bash command)")
        print("Example: for test.txt in /tmp|/home 'ls -la'")
        return
    
    file_name = cmd_parts[1]
    paths_str = cmd_parts[3]
    bash_cmd = ' '.join(cmd_parts[4:])  # Allow multi-word commands
    
    valid_paths = validate_paths(paths_str)
    if not valid_paths:
        print("Error: No valid paths provided")
        return
    
    # Build command
    bash_command = ""
    for path in valid_paths:
        bash_command += f"cd '{path}' && "
    bash_command += f"{bash_cmd} '{file_name}'"
    
    execute_bash_command(bash_command)

def rush_easy_bash_command(cmd_parts):
    """
    Syntax: rush (path1|path2|path3) (bash command)
    Example: rush /tmp|/home "ls -la"
    """
    if len(cmd_parts) < 3:
        print("Error: Invalid syntax")
        print("Usage: rush (path1|path2|path3) (bash command)")
        print("Example: rush /tmp|/home 'ls -la'")
        return
    
    paths_str = cmd_parts[1]
    bash_cmd = ' '.join(cmd_parts[2:])  # Allow multi-word commands
    
    valid_paths = validate_paths(paths_str)
    if not valid_paths:
        print("Error: No valid paths provided")
        return
    
    # Build command
    bash_command = ""
    for path in valid_paths:
        bash_command += f"cd '{path}' && "
    bash_command += f"{bash_cmd}"
    
    execute_bash_command(bash_command)

def show_help():
    """Display help information"""
    help_text = """
EasyBash Commands:
-----------------
for (filename) in (path1|path2|path3) (bash command)
    Execute command on filename in multiple directories
    Example: for test.txt in /tmp|/home 'ls -la'

rush (path1|path2|path3) (bash command)  
    Execute command in multiple directories
    Example: rush /tmp|/home 'pwd'

exit
    Exit EasyBash

Note: Use quotes for commands with spaces
"""
    print(help_text)

def main():
    """Main program loop"""
    print("EasyBash Shell (type 'help' for commands)")
    
    while True:
        try:
            text = input("easybash> ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break
        
        if text.lower() == 'help':
            show_help()
            continue
        
        command, cmd_parts = parse_command(text)
        
        if command == "for":
            for_easy_bash_command(cmd_parts)
        elif command == "rush":
            rush_easy_bash_command(cmd_parts)
        elif command == "exit":
            print("Goodbye!")
            break
        elif command is None and text.strip():
            print(f"Unknown command: '{cmd_parts[0] if cmd_parts else ''}'")
            print("Type 'help' for available commands")

if __name__ == "__main__":
    main()

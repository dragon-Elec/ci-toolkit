#!/usr/bin/env python3
#
# action_compress.py: Non-interactive script for GitHub Actions.
# This script takes file paths and a JSON config, then runs ffmpeg.
#

import sys
import json
import subprocess
from pathlib import Path

# We reuse the exact same logic from your TUI application!
from ffmpeg_utils import build_ffmpeg_args

def main():
    """Main execution for the action."""
    if len(sys.argv) != 4:
        print("Usage: python3 action_compress.py <input_file> <output_file> '<json_config>'")
        sys.exit(1)

    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    
    try:
        # The configuration is passed as a single JSON string
        parsed_config = json.loads(sys.argv[3])
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON configuration provided. {e}")
        sys.exit(1)

    if not in_path.exists():
        print(f"Error: Input file does not exist: {in_path}")
        sys.exit(1)
        
    print("--- Configuration Received ---")
    print(json.dumps(parsed_config, indent=2))
    print("----------------------------")
    print(f"Input file: {in_path}")
    print(f"Output file: {out_path}")

    # Use the existing utility function to build the command
    ffmpeg_command = build_ffmpeg_args(str(in_path), str(out_path), parsed_config)
    
    # Prepend the main 'ffmpeg' executable
    full_command = ['ffmpeg', *ffmpeg_command]
    
    print("\nExecuting FFmpeg command:")
    # We use a space to join arguments for printing, making it easy to copy-paste and debug.
    print(' '.join(full_command))
    print("\n--- FFmpeg Output ---")

    try:
        # We use subprocess.run to execute and wait for completion.
        # check=True will automatically raise an error if ffmpeg returns a non-zero exit code.
        # text=True decodes stdout/stderr as text.
        subprocess.run(full_command, check=True, text=True, stdout=sys.stdout, stderr=sys.stderr)
        print("--- FFmpeg Processing Succeeded ---")
        
    except FileNotFoundError:
        print("Error: 'ffmpeg' command not found. Is it installed in the runner environment?")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"\nError: FFmpeg failed with exit code {e.returncode}.")
        # The stdout/stderr is already piped to the action's log, so no need to print e.stdout/e.stderr here.
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

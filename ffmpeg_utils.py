# ffui-python: ffmpeg_utils.py
# Handles all subprocess calls to ffmpeg and ffprobe.

import subprocess
import re
import json
from config import SUPPORTED_VIDEO_ENCODERS, SUPPORTED_AUDIO_ENCODERS

def get_available_encoders():
    """Queries ffmpeg to find installed and supported encoders."""
    video_encoders = ["copy"]
    audio_encoders = ["None", "copy"]
    try:
        result = subprocess.run(['ffmpeg', '-encoders'], capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()
        
        # Find the start of the encoder list
        start_index = 0
        for i, line in enumerate(lines):
            if '-------' in line:
                start_index = i + 1
                break
        
        for line in lines[start_index:]:
            if not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) > 1:
                encoder_name = parts[1]
                if encoder_name in SUPPORTED_VIDEO_ENCODERS:
                    video_encoders.append(encoder_name)
                elif encoder_name in SUPPORTED_AUDIO_ENCODERS:
                    audio_encoders.append(encoder_name)

    except (subprocess.CalledProcessError, FileNotFoundError):
        # ffmpeg not found or returned an error
        return None, None
        
    return sorted(list(set(video_encoders))), sorted(list(set(audio_encoders)))


def get_video_duration(file_path):
    """Runs ffprobe to get the duration of a video file in seconds."""
    command = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        file_path
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        return 0.0

def build_ffmpeg_args(in_path, out_path, parsed_config):
    """Constructs the list of arguments for the ffmpeg command."""
    args = ['-i', in_path]

    # Video
    args.extend(['-c:v', parsed_config['video_encoder']])
    if parsed_config['video_encoder'] in ['libx264', 'libx265']:
        args.extend(['-crf', parsed_config['crf'], '-preset', parsed_config['preset']])
    elif parsed_config['video_encoder'] in ['libvpx-vp9', 'libsvtav1']:
         args.extend(['-crf', parsed_config['crf']])

    # Audio
    if parsed_config['audio_encoder'] == 'None':
        args.append('-an')
    else:
        args.extend(['-c:a', parsed_config['audio_encoder']])

    # Add metadata flag if requested
    if parsed_config.get('preserve_metadata') == 'Yes':
        args.extend(['-map_metadata', '0'])

    # Overwrite flag
    if parsed_config['on_conflict'] == 'Overwrite':
        args.append('-y')
    else: # For 'Skip' or 'Rename', we need -n to prevent accidental overwrites
        args.append('-n')
        
    args.append(out_path)
    return args

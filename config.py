# ffui-python: config.py
# Holds all configuration data for the application.

# List of video encoders ffui will look for when scanning ffmpeg's output.
SUPPORTED_VIDEO_ENCODERS = [
    "libx264", "libx265", "libvpx-vp9", "librav1e", "libsvtav1"
]

# List of audio encoders ffui will look for.
SUPPORTED_AUDIO_ENCODERS = [
    "aac", "libopus", "libvorbis"
]

# The main configuration structure, mirroring the Go version.
# Each dictionary represents one setting in the TUI.
CONFIGS = [
    {
        "name": "Delete old video(s)?",
        "opts": ["No", "Yes"],
        "focused_option": 1,
        "key": "delete_old"
    },
    {
        "name": "Preserve Metadata?",
        "opts": ["Yes", "No"],
        "focused_option": 0,
        "key": "preserve_metadata"
    },
    {
        "name": "On name conflict?",
        "opts": ["Skip", "Overwrite", "Rename"],
        "focused_option": 0,
        "key": "on_conflict"
    },
    {
        "name": "Video Encoder",
        "opts": ["copy"],  # This will be populated dynamically
        "focused_option": 0,
        "key": "video_encoder"
    },
    {
        "name": "Audio Encoder",
        "opts": ["None", "copy"],  # This will be populated dynamically
        "focused_option": 1,
        "key": "audio_encoder"
    },
    {
        "name": "Preset",
        "opts": ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"],
        "focused_option": 4,
        "key": "preset"
    },
    {
        "name": "Constant Rate Factor (CRF)",
        "opts": ["10", "15", "20", "25", "30", "35", "40", "45", "50"],
        "focused_option": 4,
        "key": "crf"
    },
]

def get_visible_configs(configs):
    """
    Filters the config list to hide options that are not applicable
    based on the currently selected video encoder.
    """
    video_encoder_cfg = next(c for c in configs if c['name'] == "Video Encoder")
    selected_video_encoder = video_encoder_cfg['opts'][video_encoder_cfg['focused_option']]

    hidden_options = []
    if selected_video_encoder in ["copy", "librav1e"]:
        hidden_options.extend(["Preset", "Constant Rate Factor (CRF)"])
    elif selected_video_encoder in ["libvpx-vp9", "libsvtav1"]:
        hidden_options.append("Preset")

    return [c for c in configs if c['name'] not in hidden_options]

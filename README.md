# BadApple-Python-Module

Python Module: Play the video in the console as ASCII art.

Where there is light, there is [Bad Apple!!][ba]

**Install**: 

```sh
python -m pip install badapple
```

**Recommended optional dependencies**: 

Only wav audio or no audio: Python module **simpleaudio**.

Multiple audio & video formats supported: command-line tool **FFmpeg**.

**Run**:

```sh
python -m badapple
```

**Help message**:

```markdown
usage: badapple [options] ... 

BadApple-Python-OS-ISA-v0.0.2

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        video file (use _BADAPPLE_MP4 or _BADAPPLE_BADAPPLE to load built-in video)
  -o OUTPUT, --output OUTPUT
                        preload output file
  --font FONT           font data file
  --audio AUDIO         audio file (use _BADAPPLE_MP3 or _BADAPPLE_WAV to load built-in audio)
  --audio_player AUDIO_PLAYER
                        audio player [auto ffplay avplay mpv vlc mpg123 cmus simpleaudio pyaudio playsound pydub]
  -s SCALE, --scale SCALE
                        width:height
  -r RATE, --rate RATE  frame rate
  --not_clear           not clear screen (with ANSI) before each frame
  --not_check_player    not check if player is available before playing
  --contrast            contrast enhancement
  --preload             preload video (not play)
  --avaliable_player    show avaliable players
  --debug               debug
```

[ba]: https://www.youtube.com/watch?v=FtutLA63Cp8

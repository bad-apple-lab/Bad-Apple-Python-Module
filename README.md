## BadApple-Python-Module

Python Module: Play the video in the console as ASCII art.

Where there is light, there is [Bad Apple!!](https://www.youtube.com/watch?v=FtutLA63Cp8)

##### Installation

```sh
python -m pip install badapple
```

with audio:

```sh
python -m pip install badapple[audio]
```

with any supported player:

```sh
python -m pip install badapple[dev]
```

##### Run

```sh
python -m badapple
```

##### Help Message

```markdown
usage: badapple [options] ... 

BadApple-Python-OS-ISA-Version

options:
  -h, --help            show this help message and exit
  --help_audio          show avaliable players (default: False)
  -i INPUT, --input INPUT
                        video file (use _BA_MP4 or _BA_BA to load built-in video) (default: _BA_MP4)
  -o OUTPUT, --output OUTPUT
                        preload output file (default: )
  --font FONT           font data file (default: )
  --audio AUDIO         audio file (use _BA_WAV, _BA_MP3 or _BA_MP4 to load built-in audio) (default: )
  --audio_player AUDIO_PLAYER
                        audio player [ffplay mpv vlc mpg123 cmus simpleaudio pyaudio playsound auto] (default: )
  -s SCALE, --scale SCALE
                        width:height (0 means auto) (default: 0:0)
  -r RATE, --rate RATE  frame rate (default: 1024.0)
  --colorful            RGB with ANSI (Experimental) (default: False)
  --not_clear           not clear screen (with ANSI) before each frame (default: False)
  --contrast            contrast enhancement (default: False)
  --preload             preload video (not play) (default: False)
  --debug               debug (default: False)
```

##### To Do

fill with fullwidth or halfwidth char

start and end time

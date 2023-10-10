BadApple
========

Python Module: Play the video in the console as ASCII art.

Where there is light, there is `Bad Apple!! <https://www.youtube.com/watch?v=FtutLA63Cp8>`

Install
-------

.. code-block:: shell

    python -m pip install badapple

Run
---

.. code-block:: shell

    python -m badapple

Help Message
------------

.. code-block:: md

    usage: badapple [options] ... 

    BadApple-Python-OS-ISA-v0.0.4

    options:
      -h, --help            show this help message and exit
      --help_audio          show avaliable players
      -i INPUT, --input INPUT
                            video file (use _BA_MP4 or _BA_BA to load built-in video)
      -o OUTPUT, --output OUTPUT
                            preload output file
      --font FONT           font data file
      --audio AUDIO         audio file (use _BA_WAV, _BA_MP3 or _BA_MP4 to load built-in audio)
      --audio_player AUDIO_PLAYER
                            audio player [ffplay mpv vlc mpg123 cmus simpleaudio pyaudio playsound pydub auto]
      -s SCALE, --scale SCALE
                            width:height
      -r RATE, --rate RATE  frame rate
      --not_clear           not clear screen (with ANSI) before each frame
      --contrast            contrast enhancement
      --preload             preload video (not play)
      --debug               debug

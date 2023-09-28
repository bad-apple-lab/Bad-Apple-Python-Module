py -m build
twine check dist/*
py1 -m pip install dist/*.whl
py1 -m badapple --help
py1 -m badapple --help_audio
py1 -m badapple
py1 -m badapple -i aaaa
py1 -m badapple -i _BA_BA --audio archive/your_everything.mp3
py1 -m badapple --audio_player mpv
py1 -m badapple --audio_player aaaa
py1 -m badapple --audio _BA_WAV --audio_player vlc
py1 -m badapple --audio _BA_MP3 --audio_player mpg123
py1 -m badapple --audio _BA_MP3 --audio_player cmus
py1 -m badapple --audio _BA_WAV --audio_player simpleaudio
py1 -m badapple --audio _BA_WAV --audio_player playsound
py1 -m badapple --audio _BA_MP4 --audio_player pydub
py1 -m badapple -i archive/87011701_p0.jpg -s 85:98
py1 -m badapple -i archive/87011701_p0.jpg -s 85:98 --contrast
py1 -m badapple -i archive/Elysia1.mp4 -o archive/ely.badapple -s 128:72 -r 10
py1 -m badapple -i archive/ely.badapple --audio archive/addiction.flac
py1 -m badapple -i archive/NCOP.mkv -s 96:54 --contrast --audio_player auto
twine upload dist/*

py1 -m pip uninstall anyplayer
py1 -m src.badapple --help
py1 -m src.badapple --help_audio
py1 -m src.badapple
py1 -m src.badapple --colorful
py1 -m src.badapple -i _BA_BA --audio archive/your_everything.mp3
py1 -m src.badapple --audio_player mpv
py1 -m src.badapple -i archive/87011701_p0.jpg -s 85:98 --contrast
py1 -m src.badapple -i archive/Elysia1.mp4 -o archive/ely.badapple -s 320:0 --colorful
py1 -m src.badapple -i archive/ely.badapple
py1 -m src.badapple -i archive/NCOP.mkv -s 192:108 -r 10 --colorful

p_i install anyplayer
py1 -m src.badapple --help
py1 -m src.badapple --help_audio
py1 -m src.badapple
py1 -m src.badapple -i aaaa
py1 -m src.badapple -i _BA_BA --audio archive/your_everything.mp3
py1 -m src.badapple --audio_player mpv --colorful
py1 -m src.badapple --audio_player aaaa
py1 -m src.badapple --audio _BA_WAV --audio_player vlc
py1 -m src.badapple --audio _BA_MP3 --audio_player mpg123
py1 -m src.badapple --audio _BA_MP3 --audio_player cmus
py1 -m src.badapple --audio _BA_WAV --audio_player simpleaudio
py1 -m src.badapple --audio _BA_WAV --audio_player pyaudio
py1 -m src.badapple --audio _BA_WAV --audio_player playsound
py1 -m src.badapple -i archive/ely.badapple --audio archive/addiction.flac
py1 -m src.badapple -i archive/NCOP.mkv -s 192:108 -r 10 --colorful --audio_player auto

py -m build
twine check dist/*
py1 -m pip install dist/*.whl --force-reinstall
py1 -m badapple --help
py1 -m badapple --help_audio
py1 -m badapple
py1 -m badapple -i aaaa
py1 -m badapple -i _BA_BA --audio archive/your_everything.mp3
py1 -m badapple --audio_player mpv --colorful
py1 -m badapple --audio_player aaaa
py1 -m badapple --audio _BA_WAV --audio_player vlc
py1 -m badapple --audio _BA_MP3 --audio_player mpg123
py1 -m badapple --audio _BA_MP3 --audio_player cmus
py1 -m badapple --audio _BA_WAV --audio_player simpleaudio
py1 -m badapple --audio _BA_WAV --audio_player playsound
py1 -m badapple -i archive/87011701_p0.jpg -s 85:98 --contrast
py1 -m badapple -i archive/Elysia1.mp4 -o archive/ely.badapple -s 320:0 --colorful
py1 -m badapple -i archive/ely.badapple --audio archive/addiction.flac
py1 -m badapple -i archive/NCOP.mkv -s 192:108 -r 10 --colorful --audio_player auto
twine upload dist/*

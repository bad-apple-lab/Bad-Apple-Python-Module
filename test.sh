# Set-Alias -Name py1 -Value py

py1 -m pip uninstall anyplayer badapple
py1 -m src.badapple --help
py1 -m src.badapple --help_audio

py1 -m pip install anyplayer
py1 -m src.badapple --help
py1 -m src.badapple --help_audio
py1 -m src.badapple
py1 -m src.badapple -i aaaa
py1 -m src.badapple -i _BA_BA --audio archive/your_everything.mp3
py1 -m src.badapple -c rgb24 --audio_player mpv
py1 -m src.badapple --audio_player aaaa
py1 -m src.badapple --audio _BA_WAV --audio_player vlc
py1 -m src.badapple --audio _BA_MP3 --audio_player mpg123
py1 -m src.badapple --audio _BA_MP3 --audio_player cmus
py1 -m src.badapple --audio _BA_WAV --audio_player simpleaudio
py1 -m src.badapple --audio _BA_WAV --audio_player pyaudio
py1 -m src.badapple --audio _BA_WAV --audio_player playsound
py1 -m src.badapple -i archive/87011701_p0.jpg -s 85:98 -c ascii --contrast
py1 -m src.badapple -i archive/Elysia1.mp4 -o archive/ely.badapple -s 160:0 -c rgb24
py1 -m src.badapple -i archive/ely.badapple --audio archive/addiction.flac
py1 -m src.badapple -i archive/NCOP.mkv -s 120:0 -r 10 -c x232w --audio_player auto
py1 -m src.badapple -i archive/NCOP.mkv -s 192:108 -r 10 -c rgb24 --audio_player auto
py1 -m src.badapple -i archive/1.mp4 -s 192:108 -r 10 -c rgb24 --audio_player auto
py -m src.badapple -i archive/e.mp4 -r 10 -c fullwidth -m "爱莉希雅死了" --audio_player auto
py1 -m src.badapple -i archive/Elysia6.mp4 -s 240:0 -r 5 -c halfwidth -m "Elysia" --audio_player auto

py -m build
twine check dist/*
py1 -m pip install dist/*.whl --force-reinstall
py1 -m badapple --help
py1 -m badapple --help_audio
py1 -m badapple
py1 -m badapple -i aaaa
py1 -m badapple -i _BA_BA --audio archive/your_everything.mp3
py1 -m badapple -c rgb24 --audio_player mpv
py1 -m badapple --audio_player aaaa
py1 -m badapple --audio _BA_WAV --audio_player vlc
py1 -m badapple --audio _BA_MP3 --audio_player mpg123
py1 -m badapple --audio _BA_MP3 --audio_player cmus
py1 -m badapple --audio _BA_WAV --audio_player simpleaudio
py1 -m badapple --audio _BA_WAV --audio_player pyaudio
py1 -m badapple --audio _BA_WAV --audio_player playsound
py1 -m badapple -i archive/87011701_p0.jpg -s 85:98 -c ascii --contrast
py1 -m badapple -i archive/Elysia1.mp4 -o archive/ely.badapple -s 160:0 -c rgb24
py1 -m badapple -i archive/ely.badapple --audio archive/addiction.flac
py1 -m badapple -i archive/NCOP.mkv -s 120:0 -r 10 -c x232w --audio_player auto
py1 -m badapple -i archive/NCOP.mkv -s 192:108 -r 10 -c rgb24 --audio_player auto
py1 -m badapple -i archive/1.mp4 -s 192:108 -r 10 -c rgb24 --audio_player auto
py1 -m badapple -i archive/Elysia6.mp4 -s 240:0 -r 5 -c fullwidth -m "爱莉希雅死了" --audio_player auto
py1 -m badapple -i archive/Elysia6.mp4 -s 240:0 -r 5 -c halfwidth -m "Elysia" --audio_player auto
twine upload dist/*

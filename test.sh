cd src
py -m badapple --help
py -m badapple --help_audio
py -m badapple
py -m badapple -i aaaa
py -m badapple -i _BA_BA --audio ../archive/your_everything.mp3
py -m badapple --audio_player mpv
py -m badapple --audio_player aaaa
py -m badapple --audio_player avplay
py -m badapple --audio _BA_WAV --audio_player vlc
py -m badapple --audio _BA_MP3 --audio_player mpg123
py -m badapple --audio _BA_MP3 --audio_player cmus
py -m badapple --audio _BA_WAV --audio_player simpleaudio
py -m badapple --audio _BA_WAV --audio_player playsound
py -m badapple --audio _BA_MP4 --audio_player pydub
py -m badapple -i ../archive/87011701_p0.jpg -s 85:98
py -m badapple -i ../archive/87011701_p0.jpg -s 85:98 --contrast
py -m badapple -i ../archive/Elysia1.mp4 -o ../archive/ely.badapple -s 128:72 -r 10
py -m badapple -i ../archive/ely.badapple --audio ../archive/addiction.flac
py -m badapple -i ../archive/NCOP.mkv -s 96:54 --contrast --audio_player auto

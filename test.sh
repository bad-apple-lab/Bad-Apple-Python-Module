cd src
python -m badapple --help
python -m badapple --audio_player auto
python -m badapple --audio badapple/badapple.wav
python -m badapple --audio badapple/badapple.wav --audio_player avplay
python -m badapple --audio badapple/badapple.wav --audio_player simpleaudio
python -m badapple --audio badapple/badapple.wav --audio_player pyaudio
python -m badapple --audio badapple/badapple.wav --audio_player playsound
python -m badapple -i ../archive/87011701_p0.jpg -s 85:98
python -m badapple -i ../archive/87011701_p0.jpg -s 85:98 --contrast
python -m badapple -i ../archive/Elysia1.mp4 -o ../archive/ely.badapple -s 128:72 -r 10
python -m badapple -i ../archive/ely.badapple --audio badapple/badapple.wav
python -m badapple -i ../archive/NCOP.mkv -s 96:54 --contrast --audio_player auto

import os

BA_DIR = os.path.dirname(__file__)
BA_MP3 = '_BA_MP3'
BA_MP4 = '_BA_MP4'
BA_WAV = '_BA_WAV'
BA_BA = '_BA_BA'
BA_FONT = '_BA_CONSOLA'

__FILES = {
    BA_MP3: os.path.join(BA_DIR, 'badapple.mp3'),
    BA_MP4: os.path.join(BA_DIR, 'badapple.mp4'),
    BA_WAV: os.path.join(BA_DIR, 'badapple.wav'),
    BA_BA: os.path.join(BA_DIR, 'badapple.badapple'),
    BA_FONT: os.path.join(BA_DIR, 'consola_ascii_0_ff.data')
}


def ba_get(x: str) -> str:
    return __FILES.get(x, x)

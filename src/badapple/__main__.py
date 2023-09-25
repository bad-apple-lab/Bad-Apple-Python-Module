import os
import sys
import argparse
from multiprocessing import Process

from .play import play
from .audio import help_audio
from .players import get_names
from .util import get_info

if __name__ == "__main__":
    D_DIR = os.path.dirname(__file__)
    D_MP3 = '_BA_MP3'
    D_MP4 = '_BA_MP4'
    D_WAV = '_BA_WAV'
    D_BA = '_BA_BA'
    D_FILES = {
        D_MP3: os.path.join(D_DIR, 'badapple.mp3'),
        D_MP4: os.path.join(D_DIR, 'badapple.mp4'),
        D_WAV: os.path.join(D_DIR, 'badapple.wav'),
        D_BA: os.path.join(D_DIR, 'badapple.badapple'),
    }

    parser = argparse.ArgumentParser(
        'badapple',
        'badapple [options] ... ',
        get_info(),
    )

    parser.add_argument(
        '--avaliable_player',
        help='show avaliable players',
        action='store_true'
    )

    parser.add_argument(
        '-i', '--input',
        help='video file (use %s or %s to load built-in video)' % (
            D_MP4,
            D_BA,
        ),
        default=D_MP4
    )
    parser.add_argument(
        '-o', '--output',
        help='preload output file',
        default=''
    )

    parser.add_argument(
        '--font',
        help='font data file',
        default=''
    )
    parser.add_argument(
        '--audio',
        help='audio file (use %s or %s to load built-in audio)' % (
            D_WAV,
            D_MP3,
        ),
        default=''
    )
    parser.add_argument(
        '--audio_player',
        help='audio player [%s]' % ' '.join(get_names()),
        default=''
    )

    parser.add_argument(
        '-s', '--scale',
        help='width:height',
        default='72:54'
    )
    parser.add_argument(
        '-r', '--rate',
        help='frame rate',
        default=1024.0,
        type=float
    )

    parser.add_argument(
        '--not_clear',
        help='not clear screen (with ANSI) before each frame',
        action='store_true'
    )
    parser.add_argument(
        '--contrast',
        help='contrast enhancement',
        action='store_true'
    )
    parser.add_argument(
        '--preload',
        help='preload video (not play)',
        action='store_true'
    )

    parser.add_argument(
        '--debug',
        help='debug',
        action='store_true'
    )

    a = parser.parse_args()

    if a.avaliable_player:
        help_audio()
        sys.exit(0)

    x, y = a.scale.split(':')
    x = int(x)
    y = int(y)
    need_clear = not a.not_clear

    p_list: list[Process] = list()

    video = D_FILES.get(a.input, a.input)
    audio = D_FILES.get(a.audio, a.audio)

    try:
        play(
            p_list=p_list,
            video=video, output=a.output,
            font=a.font, audio=audio, player=a.audio_player,
            x=x, y=y, fps=a.rate,
            need_clear=need_clear, contrast=a.contrast, preload=a.preload,
            debug=a.debug
        )
    except KeyboardInterrupt:
        pass
    finally:
        for i in p_list:
            if i.is_alive():
                i.terminate()

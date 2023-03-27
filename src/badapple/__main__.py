import os
import argparse
import platform

from .play import play

VERSION = 'v0.0.1'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        'badapple',
        'badapple [options] ... ',
        'BadApple-python-%s-%s-%s' % (
            platform.system().lower(),
            platform.machine().lower(),
            VERSION
        )
    )

    parser.add_argument(
        '-i', '--input',
        help='video file',
        default=os.path.join(os.path.dirname(__file__), 'badapple.mp4')
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
        help='audio file',
        default=''
    )
    parser.add_argument(
        '--audio_player',
        help='audio player [playsound, ]',
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
        help='not clear screen (with ANSI) before a frame',
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

    x, y = a.scale.split(':')
    x = int(x)
    y = int(y)

    play(
        video=a.input, output=a.output,
        font=a.font, audio=a.audio, player=a.audio_player,
        x=x, y=y, fps=a.rate,
        not_clear=a.not_clear, contrast=a.contrast, preload=a.preload,
        debug=a.debug
    )

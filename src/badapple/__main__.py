import os
import sys
import argparse
from multiprocessing import Process

from .play import play
from .audio import help_audio
from .players import get_players
from .util import get_info

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        'badapple',
        'badapple [options] ... ',
        get_info(),
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
        help='audio player [%s]' % ' '.join(get_players()),
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
        '--not_check_player',
        help='not check if player is available before playing',
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
        '--avaliable_player',
        help='show avaliable players',
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
    check_player = not a.not_check_player

    p_list: list[Process] = list()

    try:
        play(
            p_list=p_list,
            video=a.input, output=a.output,
            font=a.font, audio=a.audio, player=a.audio_player,
            x=x, y=y, fps=a.rate,
            need_clear=need_clear, check_player=check_player,
            contrast=a.contrast, preload=a.preload,
            debug=a.debug
        )
    except KeyboardInterrupt:
        for i in p_list:
            i.terminate()
        sys.exit(0)

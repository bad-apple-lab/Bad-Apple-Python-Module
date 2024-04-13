import sys
import argparse

from .play import play
from .audio import help_audio, with_anyplayer
from .util import get_info
from .builtin_files import BA_BA, BA_MP4, BA_MP3, BA_WAV, ba_get

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        'badapple',
        'badapple [options] ... ',
        get_info(),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '--help_audio',
        help='show avaliable players',
        action='store_true'
    )

    parser.add_argument(
        '-i', '--input',
        help='video file (use %s or %s to load built-in video)' % (
            BA_MP4,
            BA_BA,
        ),
        default=BA_MP4
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

    if with_anyplayer:
        from anyplayer import get_names
        parser.add_argument(
            '--audio',
            help='audio file (use %s, %s or %s to load built-in audio)' % (
                BA_WAV,
                BA_MP3,
                BA_MP4,
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
        help='width:height (0 means auto)',
        default='0:0'
    )
    parser.add_argument(
        '-r', '--rate',
        help='frame rate',
        default=1024.0,
        type=float
    )

    parser.add_argument(
        '--colorful',
        help='RGB with ANSI (Experimental)',
        action='store_true'
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

    if a.help_audio:
        help_audio()
        sys.exit(0)

    x, y = a.scale.split(':')
    x = int(x)
    y = int(y)
    need_clear = not a.not_clear

    p_list = list()

    video = ba_get(a.input)
    audio = None
    player = None
    if with_anyplayer:
        audio = ba_get(a.audio)
        player = a.audio_player

    try:
        play(
            p_list=p_list,
            video=video, output=a.output,
            font=a.font, audio=audio, player=player,
            x=x, y=y, fps=a.rate, colorful=a.colorful,
            need_clear=need_clear, contrast=a.contrast, preload=a.preload,
            debug=a.debug
        )
    except KeyboardInterrupt:
        pass
    finally:
        for i in p_list:
            if i.is_alive():
                i.terminate()

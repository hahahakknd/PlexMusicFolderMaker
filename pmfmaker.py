# Standard Library
import os        # OS 관련 기능을 제공하는 라이브러리, 여기서는 파일 및 디렉토리 작업을 위해 사용
import sys       # System 관련 기능을 제공하는 라이브러리
import shutil    # 파일 및 디렉토리 작업을 위해 고수준 인터페이스를 제공하는 라이브러리 (cpoy, move 등등)
import argparse  # 명령행 인자를 처리하기 위한 고수준 인터페이스를 제공하는 라이브러리

# 3rd Party Library
import eyed3     # mp3 파일의 Tag 정보를 사용하기 위한 라이브러리


def is_exist_music_files(source):
    return False


def make_music_folder(source, destination):
    """ Returns the sum of two numbers

        Args:
            source (str): Second number to add
            destination (str): Second number to add

        Returns:
            N/A
    """
    print('source: ' + source)
    print('destination: ' + destination)


if __name__ == '__main__':
    RECOMMAND_VERSION = 3.0
    current_version = float(
        str(sys.version_info[0]) + '.' + str(sys.version_info[1]))

    if current_version < RECOMMAND_VERSION:
        print('Error: This program run by python version 3.0 higher.')
        sys.exit()

    HELP_DOC = (
        'Make the plex music folder from music file.\n'
        '\n'
        'Making Rule:\n'
        '   /Album Artist\n'
        '       /Albulm Name\n'
        '           /Musics'
    )

    parser = argparse.ArgumentParser(
        prog='top', description=HELP_DOC, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('path', nargs=2, type=str,
                        help='need two path (1st: source, 2nd: dest)')
    args = parser.parse_args()

    # Change to absolute path
    make_music_folder(
        os.path.abspath(args.path[0]), os.path.abspath(args.path[1]))

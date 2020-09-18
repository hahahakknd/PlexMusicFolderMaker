""" Plex Music Folder Maker

    Created by hahahakknd(hahahakknd@gmail.com)
"""

# Standard Library
import os        # OS 관련 기능을 제공하는 라이브러리, 여기서는 파일 및 디렉토리 작업을 위해 사용
import pathlib   # 파일 시스템을 객체 기반으로 다루기위한 라이브러리
import sys       # System 관련 기능을 제공하는 라이브러리
import argparse  # 명령행 인자를 처리하기 위한 고수준 인터페이스를 제공하는 라이브러리

# 3rd Party Library
import eyed3     # mp3 파일의 Tag 정보를 사용하기 위한 라이브러리

def remove_invalid_char_for_windows(path_part):
    """ Checking music fils

        \ / : * ? " < > |

        Args:
            source (str): Second number to add
            destination (str): Second number to add

        Returns:
            N/A
    """
    return False


def make_music_folder(src, dest):
    """ Make music folder

        Args:
            src (str): dir absolute path for original music file
            dest (str): dir absolute path for copy music file

        Returns:
            N/A
    """

    mp3_filename_pattern = '*.mp3'
    mp3_suffix = '.mp3'

    src_path = pathlib.Path(src)
    dest_path = pathlib.Path(dest)

    # Checking whether directory or not to src path
    if not src_path.is_dir():
        print('src path for original music file is not directory, ' + src)
        return

    # # Checking whether directory or not to dest path
    # if not dest_path.is_dir():
    #     print('dest path for copy music file is not directory, ' + dest)
    #     return

    # Make dest directory
    dest_path.mkdir(parents=True, exist_ok=True)

    # Scan mp3 files
    for iter_item in src_path.iterdir():
        if iter_item.is_file() and iter_item.match(path_pattern=mp3_filename_pattern):
            try:
                # Load audio file
                audio_file = eyed3.load(path=iter_item)
                if audio_file is None:
                    print(
                        'Load mp3 file error: the file type is not recognized. (' + str(iter_item.absolute()) + ')')
                    continue

                # Copy dest path object
                temp_path = pathlib.Path(dest_path)

                # Make parent dir path and create directory
                temp_path = temp_path / audio_file.tag.album_artist / audio_file.tag.album
                print(temp_path)
                # temp_path.mkdir(parents=True, exist_ok=True)

                # Make audio file path and copy audio file
                temp_path = temp_path / (str(audio_file.tag.track_num[0]) + ' - ' + audio_file.tag.title + mp3_suffix)
                print(temp_path)
                # temp_path.write_bytes(data=iter_item.read_bytes())

            except IOError as err:
                print('Load mp3 file error: ' + err.strerror + '. (' + str(iter_item.absolute()) + ')')
                continue


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

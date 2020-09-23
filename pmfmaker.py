""" Plex Music Folder Maker

    Created by hahahakknd(hahahakknd@gmail.com)
"""

# Standard Library
import os        # OS 관련 기능을 제공하는 라이브러리, 여기서는 파일 및 디렉토리 작업을 위해 사용
import pathlib   # 파일 시스템을 객체 기반으로 다루기위한 라이브러리
import sys       # System 관련 기능을 제공하는 라이브러리
import argparse  # 명령행 인자를 처리하기 위한 고수준 인터페이스를 제공하는 라이브러리
import platform  # OS 타입을 확인하기 위한 라이브러리

# Import variable type
from pathlib import Path
from typing import Any

# 3rd Party Library
import eyed3     # mp3 파일의 Tag 정보를 사용하기 위한 라이브러리

MP3_FILENAME_PATTERN: str = '*.mp3'
MP3_SUFFIX: str = '.mp3'
OS_TYPE: str = platform.system()


def clean_name(name: str) -> str:
    """ Remove invalid char and apply trim

        Invalid char: \\ / : * ? " < > |

        Args:
            string (str): string for cleaning

        Returns:
            Modified string
    """

    # Copy name
    modified_name: str = name

    # Remove invalid char
    if OS_TYPE == 'Windows':
        modified_name = modified_name.translate(
            str.maketrans('', '', '\\/:*?"<>|'))

    # Remove string that not exist character behind '.' character
    # Except only space case
    is_finished: bool = False
    start_index: int = 0
    while True:
        size: int = len(modified_name)
        if size == 0:
            break

        index: int = modified_name.find('.', start_index)
        if index == -1:
            break

        next_index: int = index + 1
        while True:
            # Last position
            if next_index == size:
                # Check size
                if (next_index - index) == size:
                    raise Exception(
                        'Do not make file or directory, invalid name: ' + modified_name)

                modified_name = modified_name.replace(
                    modified_name[index:next_index], '')
                is_finished = True
                break

            if is_finished:
                break

            if modified_name[next_index] == ' ':
                modified_name = modified_name.replace(
                    modified_name[index:next_index], '')
                break

            if modified_name[next_index] == '.':
                next_index = next_index + 1
                continue

            start_index = next_index + 1
            break

        if is_finished:
            break

    # Both trim
    modified_name = modified_name.strip()

    return modified_name


def make_music_folder(src: str, dest: str) -> None:
    """ Make music folder

        Args:
            src (str): dir absolute path for original music file
            dest (str): dir absolute path for copy music file

        Returns:
            N/A
    """

    src_path = pathlib.Path(src)
    dest_path = pathlib.Path(dest)

    # Checking whether directory or not to src path
    if not src_path.is_dir():
        print('src path for original music file is not directory, ' + src)
        return

    # Make dest directory
    dest_path.mkdir(parents=True, exist_ok=True)

    # Scan mp3 files
    for iter_item in src_path.iterdir():
        if iter_item.is_file() and iter_item.match(path_pattern=MP3_FILENAME_PATTERN):
            try:
                # Load audio file
                audio_file: Any = eyed3.load(path=iter_item)
                if audio_file is None:
                    print('Load mp3 file error: the file type is not recognized. (' +
                          str(iter_item.absolute()) + ')')
                    continue

                print('Title: ' + audio_file.tag.title)

                # Copy dest path object
                temp_path: Path = dest_path

                # Make parent dir path and create directory
                temp_path = temp_path / \
                    clean_name(audio_file.tag.album_artist) / \
                    clean_name(audio_file.tag.album)
                temp_path.mkdir(parents=True, exist_ok=True)
                # print(audio_file.tag.album_artist + ' : ' + clean_name(audio_file.tag.album_artist))
                # print(audio_file.tag.album + ' : ' + clean_name(audio_file.tag.album))

                # Make audio file path and copy audio file
                temp_path = temp_path / \
                    (str(audio_file.tag.track_num[0]) + ' - ' +
                     clean_name(audio_file.tag.title) + MP3_SUFFIX)
                temp_path.write_bytes(data=iter_item.read_bytes())
                # print(audio_file.tag.title + ' : ' + clean_name(audio_file.tag.title))

            except IOError as err:
                print('Load mp3 file error: ' + err.strerror +
                      '. (' + str(iter_item.absolute()) + ')')
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

import os
import argparse
import hashlib
import re


def get_sorting_option() -> '1 or 2':
    print('Size sorting options:')
    print('1. Descending')
    print('2. Ascending')
    while True:
        command = input()
        if command not in '12':
            print('Wrong option')
        else:
            return int(command)


def get_yes_or_no_option(question: str) -> 'yes or no':
    while True:
        command = input(question)
        if command in ['yes', 'no']:
            return command
        print('Wrong option')


def get_delete_list() -> map:
    while True:
        command = input('Delete files?\n')
        if re.match(r'\d+( \d+)*$', command):
            for num in command.split():
                if int(num) not in file_nums:
                    break
            else:
                return map(int, command.split())
        print('Wrong option')


def get_hash(path) -> str:
    with open(path, 'rb') as f:
        md5 = hashlib.md5()
        md5.update(f.read())
    return md5.hexdigest()


def remove_files(file_list, numbers) -> int:
    total_size = 0
    for num in numbers():
        total_size += os.path.getsize(file_list[num])
        os.remove(file_list[num])
    return total_size


def get_files(path, format_) -> list[str]:
    result = []
    for root, folders, files in os.walk(path):
        for f in files:
            if f.endswith(f'.{format_}') or format_ == '':
                result.append(os.path.join(root, f))
    return result


def get_duplicate_files_dict(size_and_files: dict):
    result = {}
    for size in size_and_files:
        hash_dict = {}
        for f in size_and_files[size]:
            h = get_hash(f)
            hash_dict[h] = hash_dict.get(h, []) + [f]
        result[size] = hash_dict
    return result


def get_file_nums(duplicate_files: dict):
    result = {}
    count = 1
    for size in duplicate_files:
        for h in duplicate_files[size]:
            if len(duplicate_files[size][h]) > 1:
                for f in duplicate_files[size][h]:
                    result[count] = f
                    count += 1
    return result


def print_duplicate_list():
    count = 1
    for size in duplicate_files_dict:
        print('\n' + str(size) + ' bytes')
        for hash_ in duplicate_files_dict[size]:
            if len(duplicate_files_dict[size][hash_]) > 1:
                print('Hash:', hash_)
                for f in duplicate_files_dict[size][hash_]:
                    print(f'{count}. {f}')
                    count += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', nargs="?", default=False)
    args = parser.parse_args()

    if args.folder:
        form = input('Enter file format:\n')
        list_of_files = get_files(args.folder, form)
        match get_sorting_option():
            case 1:
                list_of_files.sort(key=os.path.getsize, reverse=True)
            case 2:
                list_of_files.sort(key=os.path.getsize)
        file_sizes = {}
        for file in list_of_files:
            file_sizes[os.path.getsize(file)] = file_sizes.get(os.path.getsize(file), []) + [file]
        for i in file_sizes:
            print(i, 'bytes')
            print(*file_sizes[i], sep='\n', end='\n\n')

        if get_yes_or_no_option('Check for duplicates?\n') == 'yes':
            duplicate_files_dict = get_duplicate_files_dict(file_sizes)
            file_nums = get_file_nums(duplicate_files_dict)
            print_duplicate_list()
            if get_yes_or_no_option('Delete files?\n') == 'yes':
                print(f'Total freed up space: {remove_files(file_nums, get_delete_list)} bytes')
    else:
        print('Directory is not specified')

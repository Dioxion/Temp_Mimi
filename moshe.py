#!/usr/bin/env python3
import subprocess
import argparse
supported_versions_to_bytes = {
		'17': [b"\x00\x00\x0F\x85\x7F\x01\x00\x00", b"\x00\x00\x0F\x84\x84\x01\x00\x00"],																									
        '18': [b"\x00\x00\x0F\x85\x7C\x01\x00\x00", b"\x00\x00\x0f\x84\x7c\x01\x00\x00"],
		'19': [b"\x00\x00\x0F\x85\x7B\x01\x00\x00", b"\x00\x00\x0f\x84\x7c\x01\x00\x00"],
		'20': [b"\x00\x00\x0F\x85\x84\x01\x00\x00", b"\x00\x00\x0F\x84\x84\x01\x00\x00"],
		
}
def replace_file_bytes(file_path, old_bytes, new_bytes):
    with open(file_path, 'rb') as f:
        data = f.read()
        position = data.find(old_bytes)
    if(-1 == position):
        raise Exception("cannot find bytes, maybe the program is already patched?")
    with open(file_path, 'rb+') as file:
        file.seek(position)
        existing_bytes = file.read(len(old_bytes))
        if existing_bytes == old_bytes:
            file.seek(position)
            file.write(new_bytes)
			
def get_go_bin_version(filename):
    command = f"strings {filename} | grep '^go1' | head -n 1"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()
    if "" == output:
        command =  f"strings {filename} | grep 'Go cmd/compile'  | head -n 1 | cut -d' ' -f 3"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout.strip()
    return output
def get_args():
    parser = argparse.ArgumentParser(description='Get a filename and patches it ssl verification check')
    parser.add_argument("-f", "--filename", help='File to patch')
    return parser.parse_args()
def main():
    args = get_args()
	
    version = get_go_bin_version(args.filename).split('.')[1]
    old_bytes = supported_versions_to_bytes[version][0]
    new_bytes = supported_versions_to_bytes[version][1]
    replace_file_bytes(args.filename, old_bytes, new_bytes)
if "__main__" == __name__:
    main()
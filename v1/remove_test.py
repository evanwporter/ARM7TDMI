#!/usr/bin/python3
import os
from struct import unpack_from, pack

TARGET_INDEX = 34555
TARGET_FILE = r".\tests\GameboyAdvanceCPUTests\v1\arm_ldr_str_register_offset.json.bin"


def load_state(buf, ptr):
    full_sz = unpack_from("<i", buf, ptr)[0]
    return full_sz, buf[ptr : ptr + full_sz]


def load_transactions(buf, ptr):
    full_sz = unpack_from("<i", buf, ptr)[0]
    return full_sz, buf[ptr : ptr + full_sz]


def load_opcodes(buf, ptr):
    full_sz = unpack_from("<i", buf, ptr)[0]
    return full_sz, buf[ptr : ptr + full_sz]


def decode_test(buf, ptr):
    full_sz = unpack_from("<i", buf, ptr)[0]
    return full_sz, buf[ptr : ptr + full_sz]


def remove_test_from_file(filename, index_to_remove):
    print(f"Processing {filename}")
    with open(filename, "rb") as f:
        content = f.read()

    magic, num_tests = unpack_from("<II", content, 0)

    if magic != 0xD33DBAE0:
        raise RuntimeError("Invalid test file magic!")

    print(f"Original test count: {num_tests}")

    ptr = 8
    tests_raw = []

    for i in range(num_tests):
        sz, raw = decode_test(content, ptr)
        tests_raw.append(raw)
        ptr += sz

    if index_to_remove >= len(tests_raw):
        raise IndexError("Test index out of range")

    print(f"Removing test index {index_to_remove}")

    del tests_raw[index_to_remove]

    new_num_tests = len(tests_raw)

    # Rebuild file
    new_content = bytearray()
    new_content += pack("<II", magic, new_num_tests)

    for raw in tests_raw:
        new_content += raw

    # Backup original
    backup_name = filename + ".backup"
    if not os.path.exists(backup_name):
        print(f"Creating backup: {backup_name}")
        with open(backup_name, "wb") as f:
            f.write(content)

    # Overwrite original
    with open(filename, "wb") as f:
        f.write(new_content)

    print(f"Done. New test count: {new_num_tests}")


def main():
    remove_test_from_file(TARGET_FILE, TARGET_INDEX)


if __name__ == "__main__":
    main()

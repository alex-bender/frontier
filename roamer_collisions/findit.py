#!/usr/bin/env python3
"""Generates sha224 hashes from all files in file system.
Gets first 12 chars from it digest and counts duplicates."""
import os
import sys
import hashlib
import collections

visited_paths = []
visited_items = 0
counter = collections.Counter()
DEBUG = False


def get_hash(text):
    text_hash = hashlib.sha224(text.encode()).hexdigest()
    if DEBUG:
        print(text_hash, visited_items)
    return text_hash

def walk(path):
    global visited_items
    for root, dirs, files in os.walk(path):
        if root not in visited_paths:
            count = root.count('/')
            if files:
                for file_name in files:
                    abs_path = os.path.join(root, file_name)
                    if not os.path.exists(abs_path):
                        continue
                    visited_items += 1
                    hash_seed = abs_path + str(os.path.getmtime(abs_path))
                    digest = get_hash(hash_seed)
                    counter.update([digest[0:12]])
            if dirs:
                for dir_name in dirs:
                    visited_items += 1
                    abs_path = os.path.join(root, dir_name)
                    hash_seed = abs_path + str(os.path.getmtime(abs_path))
                    digest = get_hash(hash_seed)
                    counter.update([digest[0:12]])
                    walk(abs_path)
                    visited_paths.append(abs_path)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('[!] pass the directory to walk as an argument')
        sys.exit(1)
    walk(sys.argv[1])
    print('Visited items:', visited_items)
    print('Hash, count')
    for dup_hash, count in counter.most_common(10):
        print(dup_hash, count)

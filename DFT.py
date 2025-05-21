import os
import hashlib
import exifread
import argparse

def extract_metadata(file_path):
    print(f"\n[+] Metadata for: {file_path}")
    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f, stop_tag="UNDEF", details=False)
        for tag in tags.keys():
            print(f"{tag}: {tags[tag]}")

def generate_hash(file_path):
    print(f"\n[+] Hashes for: {file_path}")
    with open(file_path, 'rb') as f:
        content = f.read()
        md5_hash = hashlib.md5(content).hexdigest()
        sha256_hash = hashlib.sha256(content).hexdigest()
        print(f"MD5: {md5_hash}")
        print(f"SHA256: {sha256_hash}")

def search_keywords(file_path, keywords):
    print(f"\n[+] Keyword scan in: {file_path}")
    with open(file_path, 'r', errors='ignore') as f:
        content = f.read()
        for keyword in keywords:
            if keyword.lower() in content.lower():
                print(f"[-] Found keyword: {keyword}")

def main():
    parser = argparse.ArgumentParser(description="Digital Forensics Toolkit")
    parser.add_argument('--metadata', help='Extract metadata from image')
    parser.add_argument('--hash', help='Generate MD5 and SHA256 hash of file')
    parser.add_argument('--search', nargs=2, metavar=('FILE', 'KEYWORDS'),
                        help='Search keywords in text file (comma-separated)')

    args = parser.parse_args()

    if args.metadata:
        extract_metadata(args.metadata)

    if args.hash:
        generate_hash(args.hash)

    if args.search:
        file_path = args.search[0]
        keywords = args.search[1].split(',')
        search_keywords(file_path, keywords)

if __name__ == '__main__':
    main()

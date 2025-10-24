from PIL import Image
import os

# Embed file into image with file size prefix
def hide_file_in_image(cover_image_path, file_to_hide_path, output_image_path):
    with open(file_to_hide_path, 'rb') as f:
        data = f.read()

    size_prefix = len(data).to_bytes(4, 'big')  # 4 bytes for size
    full_data = size_prefix + data
    binary_data = ''.join(format(byte, '08b') for byte in full_data)
    data_len = len(binary_data)

    img = Image.open(cover_image_path)
    img = img.convert('RGBA') if img.mode != 'RGBA' else img
    pixels = list(img.getdata())

    if data_len > len(pixels) * 3:
        raise ValueError("Cover image not large enough to hold the file.")

    new_pixels = []
    data_index = 0

    for pixel in pixels:
        r, g, b, *a = pixel
        channels = [r, g, b]
        new_channels = []

        for channel in channels:
            if data_index < data_len:
                bit = int(binary_data[data_index])
                new_channel = (channel & ~1) | bit
                data_index += 1
            else:
                new_channel = channel
            new_channels.append(new_channel)

        if a:
            new_pixels.append((*new_channels, a[0]))
        else:
            new_pixels.append(tuple(new_channels))

    img.putdata(new_pixels)
    img.save(output_image_path)
    print(f"[+] File hidden in: {output_image_path}")


# Extract file from image with size prefix
def extract_data(image_path, output_path):
    img = Image.open(image_path)
    binary_data = ""

    for pixel in img.getdata():
        for channel in pixel[:3]:  # Use RGB only
            binary_data += bin(channel)[-1]

    # First 32 bits = size (4 bytes)
    size_bits = binary_data[:32]
    file_size = int(size_bits, 2)
    data_bits = binary_data[32:32 + file_size * 8]

    all_bytes = [data_bits[i:i+8] for i in range(0, len(data_bits), 8)]
    data = bytearray(int(byte, 2) for byte in all_bytes)

    with open(output_path, 'wb') as f:
        f.write(data)


# Detect file type based on magic number
def detect_magic_type(file_path):
    MAGIC_SIGNATURES = {
        b'\x50\x4B\x03\x04': '.zip/.docx/.xlsx',
        b'\x25\x50\x44\x46': '.pdf',
        b'\xFF\xD8\xFF': '.jpg',
        b'\x89\x50\x4E\x47': '.png',
        b'\x42\x4D': '.bmp',
        b'\x52\x61\x72\x21': '.rar',
        b'\x7F\x45\x4C\x46': '.elf',
        b'\x49\x44\x33': '.mp3',
        b'\x00\x00\x01\xBA': '.mpg',
        b'\x00\x00\x01\xB3': '.mpg',
        b'\x25\x21': '.ps',
        b'\xD0\xCF\x11\xE0': '.doc/.xls/.ppt',
        b'\x1F\x8B': '.gz',
    }

    try:
        with open(file_path, 'rb') as f:
            file_start = f.read(8)

        for magic, ext in MAGIC_SIGNATURES.items():
            if file_start.startswith(magic):
                return ext
        return 'Unknown or no file found'
    except Exception as e:
        return f'Error: {str(e)}'


# Main menu
if __name__ == "__main__":
    print("Steganography Tool")
    print("==================")
    print("1. Hide file in image")
    print("2. Extract and detect file from image")
    choice = input("Select (1/2): ")

    if choice == "1":
        cover = input("Enter path to cover image (PNG): ").strip()
        secret = input("Enter path to file to hide: ").strip()
        output = input("Enter output image name (e.g., stego.png): ").strip()
        hide_file_in_image(cover, secret, output)

    elif choice == "2":
        image = input("Enter path to stego image: ").strip()
        extracted = "extracted_output.bin"
        extract_data(image, extracted)
        file_type = detect_magic_type(extracted)
        print(f"[+] Detected file type: {file_type}")
        suggested_ext = file_type.split("/")[-1].replace(".", "").strip()
        if "Unknown" not in file_type and "Error" not in file_type:
            new_name = f"extracted_file.{suggested_ext}"
            os.rename(extracted, new_name)
            print(f"[+] Saved as: {new_name}")
        else:
            print(f"[!] Could not determine extension. Saved as: {extracted}")
    else:
        print("Invalid choice.")

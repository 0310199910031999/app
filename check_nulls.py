import sys

def check_for_null_bytes(filepath):
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
            if b'\x00' in content:
                print(f"Null bytes found in {filepath}")
                sys.exit(1)
            else:
                print(f"No null bytes found in {filepath}")
                sys.exit(0)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        sys.exit(2)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_nulls.py <file_path>")
        sys.exit(3)
    
    file_to_check = sys.argv[1]
    check_for_null_bytes(file_to_check)
import os
import pickle
import sys
from typing import cast


def main() -> None:
    program_name: str = sys.argv[0]

    if len(sys.argv) <= 1:
        print(f"Usage: {program_name} <input.bpe>")
        print("ERROR: no input provided")
        sys.exit(1)

    input_file_path: str = sys.argv[1]
    pairs: list[tuple[int, int]] = load_pairs(file_path=input_file_path)

    for token in range(1, len(pairs)):
        print(f"{token} => |", end="")
        s: str = render_token(pairs, token)

        for c in s:
            if 0x20 <= ord(c) <= 0x7E:
                print(c, end="")
            else:
                print(f"x{ord(c):02X}", end="")
        print("|")


def render_token(pairs: list[tuple[int, int]], token: int) -> str:
    if token == pairs[token][0]:
        return chr(token)
    left_char: str = render_token(pairs=pairs, token=pairs[token][0])
    right_char: str = render_token(pairs=pairs, token=pairs[token][1])
    return left_char + right_char


def load_pairs(file_path: str) -> list[tuple[int, int]]:
    if not os.path.exists(path=file_path):
        print("ERROR: file_path does not exist")
        sys.exit(1)

    try:
        with open(file=file_path, mode="rb") as binary:
            return cast(list[tuple[int, int]], pickle.load(file=binary))
    except:
        print("ERROR: failed to load pairs")
        sys.exit(1)


if __name__ == "__main__":
    main()

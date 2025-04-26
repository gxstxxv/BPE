import os
import pickle
import sys
from typing import cast


def main() -> None:
    program_name: str = sys.argv[0]

    if len(sys.argv) <= 1:
        print(f"Usage: {program_name} <input.bpe> <output.dot>")
        print("ERROR: no input provided")
        sys.exit(1)

    input_file_path: str = sys.argv[1]
    pairs: list[tuple[int, int]] = load_pairs(file_path=input_file_path)

    if len(sys.argv) <= 2:
        print(f"Usage: {program_name} <input.bpe> <output.dot>")
        print("ERROR: no output provided")
        sys.exit(1)
    output_file_path: str = sys.argv[2]

    dot: str = generate_dot(pairs)
    write_dot(output_file_path, dot)


def generate_dot(pairs: list[tuple[int, int]]) -> str:
    dot: str = ""
    dot += "digraph pairs {\n"
    for i, pair in enumerate(pairs):
        if i != pair[0]:
            dot += f" {i} -> {pair[0]}\n"
            dot += f" {i} -> {pair[1]}\n"
    dot += "}\n"
    return dot


def write_dot(output_file_path: str, dot: str) -> None:
    try:
        with open(file=output_file_path, mode="w") as file:
            _ = file.write(dot)
            print(f"INFO: generated {output_file_path}")
    except:
        print(f"ERROR: failed generate {output_file_path}")
        sys.exit(1)


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

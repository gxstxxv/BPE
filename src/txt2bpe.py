import os
import pickle
import sys


def main() -> None:
    program_name: str = sys.argv[0]

    if len(sys.argv) <= 1:
        print(f"Usage: {program_name} <input.txt> <output.bpe>")
        print("ERROR: no input provided")
        sys.exit(1)
    input_file_path: str = sys.argv[1]

    if len(sys.argv) <= 2:
        print(f"Usage: {program_name} <input.txt> <output.bpe>")
        print("ERROR: no output provided")
        sys.exit(1)
    output_file_path: str = sys.argv[2]

    bpe(input_file_path, output_file_path)


def bpe(input_file_path: str, output_file_path: str) -> None:
    text: str = read_text(file_path=input_file_path)

    freqs: dict[tuple[int, int], int] = {}
    tokens_in: list[int] = [ord(c) for c in text]
    tokens_out: list[int] = []
    pairs: list[tuple[int, int]] = [(i, 0) for i in range(256)]

    while True:
        freqs.clear()
        for i in range(len(tokens_in) - 1):
            pair: tuple[int, int] = (tokens_in[i], tokens_in[i + 1])
            freqs[pair] = freqs.get(pair, 0) + 1

        max_pair: tuple[int, int] = max(freqs.items(), key=lambda item: item[1])[0]

        if freqs[max_pair] <= 1:
            break

        pairs.append(max_pair)

        tokens_out.clear()
        i = 0
        while i < len(tokens_in):
            if i + 1 >= len(tokens_in):
                tokens_out.append(tokens_in[i])
                i += 1
            else:
                current_pair: tuple[int, int] = (tokens_in[i], tokens_in[i + 1])
                if current_pair == max_pair:
                    tokens_out.append(len(pairs) - 1)
                    i += 2
                else:
                    tokens_out.append(tokens_in[i])
                    i += 1

        tokens_in, tokens_out = tokens_out, tokens_in

    dumb_pairs(file_path=output_file_path, pairs=pairs)


def render_tokens(pairs: list[tuple[int, int]], tokens: list[int]) -> None:
    for i in range(len(tokens)):
        token: int = tokens[i]
        assert token < len(pairs)
        if pairs[token][0] == token:
            print(chr(token), end="")
        else:
            print(f"[{token}]", end="")
    print("\n")


def dumb_pairs(file_path: str, pairs: list[tuple[int, int]]) -> None:
    try:
        with open(file=file_path, mode="wb") as binary:
            pickle.dump(obj=pairs, file=binary)
        print(f"INFO: generated {file_path}")
    except:
        print("ERROR: failed to dump pairs")
        sys.exit(1)


def read_text(file_path: str) -> str:
    if not os.path.exists(path=file_path):
        print("ERROR: file_path does not exist")
        sys.exit(1)

    try:
        with open(file=file_path, mode="r") as file:
            return file.read()
    except:
        print("ERROR: failed to read text")
        sys.exit(1)


if __name__ == "__main__":
    main()

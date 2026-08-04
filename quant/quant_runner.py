import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from reasoning.llm_parser import QuantLLMParser

def main():

    if len(sys.argv) < 2:
        print("No quant request provided.")
        return

    command = sys.argv[1]

    parser = QuantLLMParser()

    request = parser.parse(command)

    print(request.summary())


if __name__ == "__main__":
    print("QUANT RUNNER STARTED")
    main()
import sys
from pathlib import Path
from quant.quant_executor import execute_quant_request
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

    result = execute_quant_request(request)

    print(result)


if __name__ == "__main__":
    print("QUANT RUNNER STARTED")
    main()
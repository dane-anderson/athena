import sys

from reasoning.llm_parser import QuantLLMParser


if len(sys.argv) < 2:
    print("No quant request provided.")
else:
    parser = QuantLLMParser()
    request = parser.parse(sys.argv[1])
    print(request.summary())

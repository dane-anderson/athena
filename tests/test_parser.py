from reasoning.parser import parse_quant_request


questions = [

    "Athena, analyze AAPL risk",

    "Run a Monte Carlo simulation on AAPL MSFT NVDA",

    "What happens to my portfolio during a 2008 crisis?",

]


for question in questions:

    print("\nUSER:")
    print(question)


    result = parse_quant_request(question)


    print("\nATHENA REQUEST:")
    print(result.summary())
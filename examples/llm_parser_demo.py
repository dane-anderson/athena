from reasoning.llm_parser import QuantLLMParser


parser = QuantLLMParser()


questions = [

    "Athena analyze my Apple risk",

    "Run a Monte Carlo simulation on Nvidia and Microsoft",

    "What happens to my portfolio during another 2008 crisis?"

]


for q in questions:

    print("\nUSER:")
    print(q)


    request = parser.parse(q)


    print("\nATHENA:")
    print(request.summary())
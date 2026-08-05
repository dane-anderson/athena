from memory.retrieval import retrieve


question = """
What happens to a portfolio during
a 2008 financial crisis?
"""


results = retrieve(question)


print("ATHENA LIBRARY RESULTS")
print("======================")


for result in results:

    print("\nFILE:")
    print(result["file"])

    print("\nPREVIEW:")
    print(
        result["content"][:250]
    )
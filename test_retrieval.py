from retriever import search_repo

query = "What does app.py do?"

results = search_repo(query, k=5)

for res in results:

    print("\n")
    print("=" * 80)

    print(f"CHUNK #{res['chunk']}")

    print(f"SOURCE: {res['source']}")

    print("-" * 80)

    print(res["content"][:1000])
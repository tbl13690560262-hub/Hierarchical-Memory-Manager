
import csv
import memory_manager

# 1. Fixed experimental dataset

test_memories = {
    "Skills": {
        "Programming": [
            "I use Python for data analysis",
            "I am learning C++",
            "I write Python scripts",
            "I practice Java programming",
            "I use Git for version control"
        ],
        "Machine Learning": [
            "I study neural networks",
            "I use Python to train models",
            "I study supervised learning",
            "I am learning PyTorch",
            "I build machine learning projects"
        ]
    },
    "Interests": {
        "Research": [
            "I am interested in long-term AI memory",
            "I enjoy reading research papers",
            "I study information retrieval",
            "I read papers about AI agents",
            "I am interested in memory systems"
        ]
    },
    "Activities": {
        "Education": [
            "I am a university student",
            "I study data structures",
            "I work on group projects",
            "I practice coding every week",
            "I am preparing for research"
        ]
    }
}


test_queries = {
    "learning C++": [
        "I am learning C++"
    ],
    "weekly coding": [
        "I practice coding every week"
    ],
    "university education": [
        "I am a university student"
    ],
    "AI agent papers": [
        "I read papers about AI agents",
        "I enjoy reading research papers"
    ],
    "Git version control": [
        "I use Git for version control"
    ]
}
K=3
memory_manager.memories = test_memories


def evaluate(retrieved_items, relevant_items):
    retrieved_items = retrieved_items[:K]

    relevant_count = sum(
        item in relevant_items for item in retrieved_items
    )

    precision = relevant_count / len(retrieved_items) if retrieved_items else 0
    recall = relevant_count / len(relevant_items) if relevant_items else 0

    if precision + recall > 0:
        f1 = 2 * precision * recall / (precision + recall)
    else:
        f1 = 0

    return precision, recall, f1


# 3. Run evaluation
rows = []

for query, relevant_items in test_queries.items():

    baseline_results = memory_manager.search_memory_baseline(query)
    ranked_results = memory_manager.search_memory_ranked(query)
    token_results = memory_manager.search_memory_token(query)
    strict_results = memory_manager.search_memory_strict(query)
    expanded_results = memory_manager.search_memory_expanded(query)

    baseline_items = [item for category, subcategory, item in baseline_results]
    ranked_items = [item for score, category, subcategory, item in ranked_results]
    token_items = [item for score, category, subcategory, item in token_results]
    strict_items = [item for score, category, subcategory, item in strict_results]
    expanded_items = [item for score, category, subcategory, item in expanded_results]


    for method, retrieved in [
        ("Baseline", baseline_items),
        ("Ranked", ranked_items),
        ("Token", token_items),
        ("Strict Token", strict_items),
        ("Concept Expansion", expanded_items)
    ]:
        precision, recall, f1 = evaluate(retrieved, relevant_items)

        rows.append({
            "Query": query,
            "Method": method,
            "Precision": round(precision, 3),
            "Recall": round(recall, 3),
            "F1": round(f1, 3)
        })

        print(f"{query} | {method}")
        print(f"  Precision: {precision:.3f}")
        print(f"  Recall:    {recall:.3f}")
        print(f"  F1:        {f1:.3f}")


# 4. Save results
with open("independent_results.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["Query", "Method", "Precision", "Recall", "F1"]
    )

    writer.writeheader()
    writer.writerows(rows)


print("\n=== Average Performance ===")

for method in [
    "Baseline",
    "Ranked",
    "Token",
    "Strict Token",
    "Concept Expansion"
]:
    method_rows = [
        row for row in rows
        if row["Method"] == method
    ]

    avg_precision = sum(
        row["Precision"] for row in method_rows
    ) / len(method_rows)

    avg_recall = sum(
        row["Recall"] for row in method_rows
    ) / len(method_rows)

    avg_f1 = sum(
        row["F1"] for row in method_rows
    ) / len(method_rows)

    print(f"\n{method}")
    print(f"Precision: {avg_precision:.3f}")
    print(f"Recall:    {avg_recall:.3f}")
    print(f"F1:        {avg_f1:.3f}")

print("\n=== Error Analysis ===")

for query, relevant_items in test_queries.items():
    print(f"\nQuery: {query}")

    results = memory_manager.search_memory_token(query)

    for score, category, subcategory, item in results[:K]:
        if item in relevant_items:
            label = "Relevant"
        else:
            label = "Not Relevant"

        print(f"[Score {score}] [{label}] {item}")
        

print("\n=== Concept Expansion Test ===")

for query in ["deep learning", "source control"]:
    print(f"\nQuery: {query}")

    results = memory_manager.search_memory_expanded(query)

    for score, category, subcategory, item in results[:K]:
        print(f"[Score {score}] {item}")
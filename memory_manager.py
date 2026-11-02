
import json
import re

CONCEPT_MAP = {
    "deep learning": ["neural networks", "pytorch"],
    "source control": ["version control", "git"],
    "machine learning": ["neural networks", "pytorch"]
}

FILE_NAME = "memories.json"


def load_memory():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


memories = load_memory()


def save_memory():
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(memories, file, indent=4, ensure_ascii=False)



def add_memory(category, subcategory, item):
    if category not in memories:
        memories[category] = {}

    if subcategory not in memories[category]:
        memories[category][subcategory] = []

    if item not in memories[category][subcategory]:
        memories[category][subcategory].append(item)
        save_memory()
        print("Memory added!")
    else:
        print("Memory already exists!")


def search_memory_baseline(keyword):
    results = []

    for category, subcategories in memories.items():
        for subcategory, items in subcategories.items():
            for item in items:
                if keyword.lower() in item.lower():
                    results.append((category, subcategory, item))

    return results

def search_memory_ranked(query):
    keywords = query.lower().split()
    results = []

    if not keywords:
        return results

    for category, subcategories in memories.items():
        for subcategory, items in subcategories.items():
            for item in items:

                text = f"{category} {subcategory} {item}".lower()

                score = 0

                for keyword in keywords:
                    if keyword in text:
                        score += 1

                if score > 0:
                    results.append((score, category, subcategory, item))

    results.sort(reverse=True)

    return results

def search_memory_token(query):
    keywords = re.findall(r"\b\w+\b", query.lower())

    if not keywords:
        return []

    results = []

    for category, subcategories in memories.items():
        for subcategory, items in subcategories.items():
            for item in items:

                text = f"{category} {subcategory} {item}".lower()
                words = set(re.findall(r"\b\w+\b", text))

                score = sum(
                    keyword in words for keyword in keywords
                )

                if score > 0:
                    results.append(
                        (score, category, subcategory, item)
                    )

    results.sort(reverse=True)
    return results
def search_memory_strict(query):
    keywords = re.findall(r"\b\w+\b", query.lower())

    if not keywords:
        return []

    results = []

    for category, subcategories in memories.items():
        for subcategory, items in subcategories.items():
            for item in items:

                text = f"{category} {subcategory} {item}".lower()
                words = set(re.findall(r"\b\w+\b", text))

                if all(keyword in words for keyword in keywords):
                    score = len(keywords)
                    results.append(
                        (score, category, subcategory, item)
                    )

    return results
def search_memory_expanded(query):
    query = query.lower().strip()

    if not query:
        return []

    search_terms = [query]

    if query in CONCEPT_MAP:
        search_terms.extend(CONCEPT_MAP[query])

    results = []

    for category, subcategories in memories.items():
        for subcategory, items in subcategories.items():
            for item in items:
                text = f"{category} {subcategory} {item}".lower()

                score = 0
                for term in search_terms:
                    if term in text:
                        score += 1

                if score > 0:
                    results.append(
                        (score, category, subcategory, item)
                    )

    results.sort(reverse=True)
    return results

def update_memory(category, subcategory, old_item, new_item):
    if (category in memories
            and subcategory in memories[category]
            and old_item in memories[category][subcategory]):

        position = memories[category][subcategory].index(old_item)
        memories[category][subcategory][position] = new_item

        save_memory()
        print("Memory updated!")
    else:
        print("Memory not found!")
        
def delete_memory(category, subcategory, item):
    if (category in memories
            and subcategory in memories[category]
            and item in memories[category][subcategory]):

        memories[category][subcategory].remove(item)

        save_memory()
        print("Memory deleted!")
    else:
        print("Memory not found!")


# Main program



if __name__ == "__main__":

    while True:
        print("\n=== Hierarchical Memory Manager ===")
        print("1. Add Memory")
        print("2. Search Memory")
        print("3. View All Memories")
        print("4. Update Memory")
        print("5. Delete Memory")
        print("6. Exit")

        choice = input("Choose an option (1-4): ")

        if choice == "1":
            category = input("Enter category: ")
            subcategory = input("Enter subcategory: ")
            item = input("Enter memory: ")

            add_memory(category, subcategory, item)


        elif choice == "2":
            keyword = input("Enter search query: ")

            print("\nBaseline Results:")
            baseline = search_memory_baseline(keyword)

            for category, subcategory, item in baseline:
                print(category, "->", subcategory, "->", item)

            print("\nRanked Results:")
            ranked = search_memory_ranked(keyword)

            for score, category, subcategory, item in ranked:
                print(f"[Score: {score}] {category} -> {subcategory} -> {item}")

        elif choice == "3":
            print("\nAll Memories:")
            for category, subcategories in memories.items():
                print(category)

                for subcategory, items in subcategories.items():
                    print("  ", subcategory)

                    for item in items:
                        print("    -", item)


        elif choice == "4":
            category = input("Enter category: ")
            subcategory = input("Enter subcategory: ")
            old_item = input("Enter old memory: ")
            new_item = input("Enter new memory: ")

            update_memory(category, subcategory, old_item, new_item)

        elif choice == "5":
            category = input("Enter category: ")
            subcategory = input("Enter subcategory: ")
            item = input("Enter memory to delete: ")

            delete_memory(category, subcategory, item)

        elif choice == "6":
            print("Goodbye!")
            break

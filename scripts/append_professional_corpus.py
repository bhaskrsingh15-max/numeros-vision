import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def main():
    rules_path = BASE_DIR / "data" / "knowledge_base" / "professional_numerology_rules.json"
    corpus_path = BASE_DIR / "data" / "knowledge_base" / "numeros_vision_corpus.json"

    with open(rules_path, "r", encoding="utf-8") as f:
        rules_data = json.load(f)

    with open(corpus_path, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    # Check if already added
    if any("Professional Numerology Pro Syllabus" in p.get("source", "") for p in corpus["passages"]):
        print("Professional Pro syllabus passages already in corpus. Skipping addition.")
        return

    new_passages = []
    for topic in rules_data["topics"]:
        tid = topic["topic_id"]
        title = topic["title"]
        keywords = ", ".join(topic["keywords"])
        rules_str = json.dumps(topic["rules"], ensure_ascii=False)
        remedy_str = topic.get("remedies", "")
        qa_str = f"Q: {topic['sample_qa']['q']} A: {topic['sample_qa']['a']}"

        full_content = (
            f"Topic {tid}: {title}. Keywords: {keywords}. "
            f"Deterministic Rules & Matrices: {rules_str}. "
            f"Master Numerologist Remedies: {remedy_str}. "
            f"Clinical Consultation Dialogue: {qa_str}."
        )

        new_passages.append({
            "source": "Professional Numerology Pro Syllabus (Master Notes)",
            "location": f"Topic {tid}: {title}",
            "provenance": "verified_numeros_vision_pro",
            "content": full_content
        })

    corpus["passages"].extend(new_passages)

    with open(corpus_path, "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)

    print(f"Added {len(new_passages)} Professional Pro topics to corpus. Total passages: {len(corpus['passages'])}")

if __name__ == "__main__":
    main()

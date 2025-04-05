import json
import os
import random
from sentence_transformers import SentenceTransformer, util

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load intents
with open("C:/Users/Admin/Desktop/SinHack/SinHack/ai/intents.json", "r", encoding="utf-8") as file:
    intents = json.load(file)["intents"]

# Prepare corpus
corpus = []
tags = []
tag_to_responses = {}

for intent in intents:
    for pattern in intent["patterns"]:
        corpus.append(pattern)
        tags.append(intent["tag"])
    tag_to_responses[intent["tag"]] = intent["responses"]

# Encode all patterns
corpus_embeddings = model.encode(corpus)

# Load additional knowledge (e.g., .txt or .md files)
def load_additional_knowledge(folder=None):
    if folder is None:
        folder = os.path.join(os.path.dirname(__file__), "data")

    docs = []
    names = []
    if not os.path.exists(folder):
        print(f"[!] Data folder not found: {folder}")
        return docs, names

    for file in os.listdir(folder):
        if file.endswith(".txt") or file.endswith(".md"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                content = f.read()
                docs.append(content)
                names.append(file)
    return docs, names


extra_docs, doc_names = load_additional_knowledge()

# Get best matching intent
def get_intent(user_input):
    input_embedding = model.encode(user_input)
    scores = util.cos_sim(input_embedding, corpus_embeddings)[0]
    best_score_idx = scores.argmax().item()
    return tags[best_score_idx], scores[best_score_idx].item()

# Search knowledge base if intent confidence is low
def get_extra_knowledge(user_input):
    input_embedding = model.encode(user_input)
    best_score = 0
    best_content = ""
    best_doc = ""

    for i, doc in enumerate(extra_docs):
        doc_embedding = model.encode(doc)
        score = util.cos_sim(input_embedding, doc_embedding).item()
        if score > best_score:
            best_score = score
            best_content = doc[:500] + "..." if len(doc) > 500 else doc
            best_doc = doc_names[i]

    if best_score > 0.4:
        return f"📄 Based on {best_doc} (score={best_score:.2f}):\n{best_content}"
    else:
        return None

# Main chat loop
def chat():
    print("🤖 Smart NLP Bot is ready! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        tag, score = get_intent(user_input)

        if score > 0.65:  # high confidence from intents.json
            response = random.choice(tag_to_responses[tag])
            print(f"Bot ({tag}): {response} [score={score:.2f}]")
        else:
            fallback = get_extra_knowledge(user_input)
            if fallback:
                print(f"Bot (external): {fallback}")
            else:
                print("Bot: Sorry, I couldn't understand that clearly. Please try again!")

if __name__ == "__main__":
    chat()

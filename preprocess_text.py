import re
import json

def preprocess_text(text):
    """Clean and split text into structured Q&A format."""
    text = re.sub(r"\n{2,}", "\n", text)  # Remove excessive newlines
    text = re.sub(r"Page \d+", "", text)  # Remove page numbers
    sentences = text.split(". ")

    qa_pairs = []
    for i in range(len(sentences) - 1):
        question = "What is " + sentences[i].strip() + "?"
        answer = sentences[i + 1].strip()
        qa_pairs.append({"question": question, "answer": answer})

    return qa_pairs

# Load extracted text
with open("medical_text.json", "r", encoding="utf-8") as f:
    raw_text = json.load(f)["content"]

# Process the text
qa_data = preprocess_text(raw_text)

# Save the structured Q&A dataset
with open("medical_qa.json", "w", encoding="utf-8") as f:
    json.dump(qa_data, f, indent=4)

print("✅ Medical Q&A dataset saved as 'medical_qa.json'!")

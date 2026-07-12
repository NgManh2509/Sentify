from transformers import BertTokenizer
from model import BertForMultiLabelClassification
from multilabel_pipeline import MultiLabelPipeline

tokenizer = BertTokenizer.from_pretrained("monologg/bert-base-cased-goemotions-original")
model = BertForMultiLabelClassification.from_pretrained("monologg/bert-base-cased-goemotions-original")

goemotions = MultiLabelPipeline(
    model=model,
    tokenizer=tokenizer,
    threshold=0.15
)

EMOJI = {
    "admiration":    "🤩",
    "amusement":     "😄",
    "anger":         "😡",
    "annoyance":     "😤",
    "approval":      "👍",
    "caring":        "🥰",
    "confusion":     "😕",
    "curiosity":     "🤔",
    "desire":        "😍",
    "disappointment":"😞",
    "disapproval":   "👎",
    "disgust":       "🤢",
    "embarrassment": "😳",
    "excitement":    "🤩",
    "fear":          "😨",
    "gratitude":     "🙏",
    "grief":         "😭",
    "joy":           "😄",
    "love":          "❤️",
    "nervousness":   "😰",
    "optimism":      "🌟",
    "pride":         "🦁",
    "realization":   "💡",
    "relief":        "😮‍💨",
    "remorse":       "😔",
    "sadness":       "😢",
    "surprise":      "😲",
    "neutral":       "😐",
}


def detect(text: str) -> dict:
    """
    Nhận vào một đoạn văn bản tiếng Anh.
    Trả về dict: {"labels": [...], "scores": [...]}
    """
    results = goemotions([text])
    return results[0]


def print_result(result: dict) -> None:
    """In kết quả cảm xúc ra màn hình theo định dạng đẹp."""
    labels = result.get("labels", [])
    scores = result.get("scores", [])

    if not labels:
        print("💬 Cảm xúc  : Không xác định")
        return

    print("💬 Cảm xúc  :")
    for label, score in zip(labels, scores):
        emoji = EMOJI.get(label, "❓")
        bar   = "█" * int(score * 20)
        print(f"   {emoji}  {label:<14}  {score:.2%}  {bar}")


if __name__ == "__main__":
    from pprint import pprint

    texts = [
        "Hey that's a thought! Maybe we need [NAME] to be the celebrity vaccine endorsement!",
        "it's happened before?! love my hometown of beautiful new ken 😂😂",
        "I love you, brother.",
        "Troll, bro. They know they're saying stupid shit. The motherfucker does nothing but stink up libertarian subs talking shit",
    ]

    pprint(goemotions(texts))

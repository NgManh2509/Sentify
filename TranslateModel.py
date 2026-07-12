
import torch
import re

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "facebook/nllb-200-1.3B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

SLANG_DICT = {
    "vãi": "rất",
    "vkl": "rất",
    "vl": "rất",
    "ảo ma": "điên rồ",
    "ảo ma canada": "vô cùng điên rồ",
    "củ chuối": "tồi tệ",
    "phèn": "xấu",
    "ngon vãi": "rất đẹp",
    "cay thế": "tức giận quá",
    "trầm cảm mẹ luôn": "vô cùng tuyệt vọng",
    "gacha": "quay thưởng",
    "tạch": "thất bại",
    "cháy quá": "rất tuyệt vời",
    "đỉnh chóp": "hoàn hảo",
    "mê xỉu": "rất thích",
    "hãm": "tồi tệ",
    "toang": "hỏng bét"
}

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Define translation function
def translate(text, src_lang="vie_Latn", tgt_lang="eng_Latn"):
    tokenizer.src_lang = src_lang
    inputs = tokenizer(text, return_tensors="pt").to(device)
    forced_bos_token_id = tokenizer.convert_tokens_to_ids(tgt_lang)

    generated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=forced_bos_token_id,
        max_length=100
    )
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

def sanitize_vietnamese(text: str) -> str:
    """
    Hàm quét và thay thế từ lóng thành từ chuẩn mực.
    Sử dụng Regex để đảm bảo chỉ thay thế đúng từ độc lập (tránh lỗi thay thế cụm từ dính liền).
    """
    clean_text = text

    sorted_slangs = sorted(SLANG_DICT.keys(), key=len, reverse=True)

    for slang in sorted_slangs:
        formal_word = SLANG_DICT[slang] 
        pattern = re.compile(r'(?i)\b' + re.escape(slang) + r'\b')
        clean_text = pattern.sub(formal_word, clean_text)

    return clean_text


def translateToEng(text: str) -> str:
    sanitized_text = sanitize_vietnamese(text)
    result = translate(sanitized_text, src_lang="vie_Latn", tgt_lang="eng_Latn")    
    return result


if __name__ == "__main__":
    print(translateToEng("Trời nóng quá"))
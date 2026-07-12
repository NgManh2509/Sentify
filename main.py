import sys
sys.stdout.reconfigure(encoding="utf-8")

from TranslateModel import translateToEng
from EmotionDetect import detect, print_result, EMOJI

print("=" * 50)
print("  Sentify — Phát hiện cảm xúc từ tiếng Việt")
print("=" * 50)
print("Nhập văn bản tiếng Việt (Enter trống để thoát)\n")

while True:
    try:
        user_input = input("🇻🇳 Nhập > ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nTạm biệt!")
        break

    if not user_input:
        print("Tạm biệt!")
        break

    # Bước 1: Dịch sang tiếng Anh
    print("🔄 Đang dịch...", end="\r")
    translated = translateToEng(user_input)
    print(f"🇬🇧 Dịch    : {translated}")

    # Bước 2: Phát hiện cảm xúc
    result = detect(translated)
    print_result(result)
    print()

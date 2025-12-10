import re

def safe_int(prompt, min_val=None, max_val = None):
    while True:
        val = input(prompt).strip()
        if not val.isdigit():
            print("Потрібно ввести число.")
            continue

        val = int(val)
        if min_val is not  None and val < min_val:
            print(f"Число має бути ≥ {min_val}")
            continue
        if max_val is not None and val > max_val:
            print(f"Число має бути ≤ {max_val}")
            continue

        return val


def safe_mode_choice():
    valid = {
        "1": "random",
        "random": "random",

        "2": "most_common",
        "most_common": "most_common",

        "3": "manual",
        "manual":"manual",

        "4": "exit",
        "exit": "exit",
        "quit": "exit",
        "q": "exit",
        
        "5": "chat",
        "chat": "chat"
    }

    while True:
        mode = input("Оберіть режим (1=random / 2=most_common / 3=manual / 4=exit / 5=chat): ").strip().lower()
        if mode in valid:
            return valid[mode]
        print("Невідомий режим. Спробуй ще раз.")


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^0-9A-Za-z\u0400-\u04FF\.\,\!\?\;\:\s\-']", " ", text)
    text = re.sub(r"\s+", " ", text)
    return  text.strip()

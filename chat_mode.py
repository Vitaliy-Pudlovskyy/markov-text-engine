import random

def run_chat(markov):
    print("\n=== Режим чату запущено ===")
    print("Напиши будь-яку фразу і модель відповість у стилі навчального тексту.")
    print("Команди: exit — вийти, reset — очистити контекст.\n")

    context = []


    while True:
        user_input = input("Ти: ").strip()

        if user_input.lower() in ("exit", "quit", "q"):
            print()
            break

        if user_input.lower() == "reset":
            context = []
            print("Контекст очищено.")
            continue

        user_words = user_input.split()
        context.extend(user_words)


        n = markov.n
        if len(context) < n:
            start = markov.get_random_start()
        else:
            start = tuple(context[-n:])

            if start not in markov.model:
                start = markov.get_random_start()

        reply = markov.generate_text(start , length = random.randint(5,15))

        print("Модель:", reply)






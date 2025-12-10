import random
from markov_chain import MarkovChain
from utility import safe_mode_choice, safe_int, clean_text


def main():
    try:
        with open("text.txt", "r", encoding="utf-8") as f:
            raw = f.read()
    except FileNotFoundError:
        print("Файл text.txt не знайдено.")
        return

    text = clean_text(raw)
    if not text:
        print("Після очищення тексту корпус пустий. Перевірте text.txt.")
        return

    mode = safe_mode_choice()

    if mode == "exit":
        print("Вихід з програми.")
        return

    if mode == "random":
        n = random.randint(2,5)
        length = random.randint(10,50)

        print(f"Випадкова n-грамма: {n}")
        print(f"Випадкова довжина генерації: {length}")

        markov = MarkovChain(n=n)
        markov.train(text)

        start = markov.get_random_start()
        print("Випадковий старт:", start)

    elif mode == "most_common":
        n = safe_int("Введи довжину n-грамми: ", min_val= 1)
        length = safe_int("Введи довжину генерованого тексту: ", min_val= 1)

        markov = MarkovChain(n=n)
        markov.train(text)

        start = markov.get_most_common_start()
        print("Найпоширеніша стартова n-грама:", start)

    elif mode == "manual":
        n = safe_int("Введи довжину n-грамми: " , min_val=1)
        length = safe_int("Введи довжину генерованого тексту: ",min_val=1)

        markov = MarkovChain(n=n)
        markov.train(text)

        start_input = input(f"Введи {n} стартових слова через пробіл: ").strip().split()
        if len(start_input) !=n:
            print(f"Потрібно ввести саме {n} слова.")
            return


        start = tuple(start_input)
        if start not in markov.model:
            print("Ця n-грама відсутня в моделі.")
            suggestions = markov.get_similar_n_starts(start , top_n=5)
            if suggestions:
                print("Можливі варіанти, близькі до введених (обери номер або введи 'r' для випадкового старту):")
                for idx , s in enumerate(suggestions ,1):
                    print(f"{idx}. {' '.join(s)}")
                choice = input("Твій вибір (1-5 / r / cancel): ").strip().lower()
                if choice == "r":
                    start = markov.get_random_start()
                    print("Вибрано випадковий старт:", start)

                elif choice == "cancel" or choice == "c":
                    print("Скасовано.")
                    return
                elif choice.isdigit() and 1<= int(choice) <= len(suggestions):
                    start = suggestions[int(choice)-1]
                    print("Вибрано:", start)
                else:
                    print("Невірний вибір. Скасовано.")
                    return
            else:
                print("Схожих варіантів не знайдено. Спробуйте інший ввід.")
                return


    elif mode == "chat":
        n=safe_int("Введи довжину n-грамми (рекомендовано 2-4): ", min_val=1)
        markov = MarkovChain(n=n)
        markov.train(text)

        from chat_mode import  run_chat
        run_chat(markov)
        return

    else:
        print("Невідомий режим.")
        return


    generated = markov.generate_text(start, length=length)
    print("\nЗгенерований текст:")
    print(generated)

if __name__ == "__main__":
    main()
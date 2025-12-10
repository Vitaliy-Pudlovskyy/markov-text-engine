import random

class MarkovChain:
    def __init__(self,n=2):
        self.model = {}
        self.n = n


    def train(self,text):
        words = text.strip().split()
        if len (words) <= self.n:
            return

        for i in range(len(words) - self.n):
            gram = tuple(words [i:i + self.n])
            next_word = words[i + self.n]
            self.model.setdefault(gram,[]).append(next_word)


    def generate_text(self, start_gram , length = 10):
        if len(start_gram) != self.n:
            raise ValueError(f"Стартова n-грамма повинна мати довжину {self.n}.")

        current_gram = start_gram
        result = list(current_gram)

        for i in range(length -self.n):
            next_words = self.model.get(current_gram)
            if not next_words:
                break
            next_word = random.choice(next_words)
            result.append(next_word)
            current_gram = tuple(result[-self.n:])
        return ' '.join(result)

    def get_all_starts(self):
        return list(self.model.keys())


    def get_random_start(self , seed = None):
        starts = self.get_all_starts()
        if not starts:
            raise ValueError ("Модель порожня — відсутні стартові пари.")
        if seed is not None:
            random.seed(seed)
        return random.choice(starts)


    def get_most_common_start(self):
        if not self.model:
            raise ValueError ("Модель порожня — відсутні стартові n-грамми.")
        most_common = max(self.model.items(), key = lambda kv: len(kv[1]))[0]
        return most_common

    def get_top_n_starts(self,n = 5):
        counts = [(gram, len(nexts)) for gram , nexts in self.model.items()]
        counts.sort(key = lambda x: x[1],reverse = True)
        return counts[:n]

    def get_similar_n_starts(self, start_tuple , top_n= 5):
        scores = []
        target_set = set(start_tuple)
        for gram in self.model.keys():
            score = 0.0
            for i ,w in enumerate(start_tuple):
                if i<len(gram) and gram[i] == w:
                    score += 1
            shared = target_set.intersection(set(gram))
            score += 0.5 * (len(shared))
            if score > 0:
                scores.append((gram , score))

        if not scores:
            top = [item[0] for item in self.get_top_n_starts(top_n)]
            return top
        scores.sort(key = lambda x: x[1] , reverse = True)
        return [ s[0] for s in scores[:top_n]]



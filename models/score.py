class Score:
    def __init__(self):
        self.score = 0
        self.load_score()

    def load_score(self):
        with open('data/score.txt', 'r') as f:
            number = f.read()
            self.score = number if number else 0

    @staticmethod
    def save_best_score(new_score):
        with open('data/score.txt', 'w') as f:
            f.write(str(new_score))

    def get_score(self):
        return int(self.score)

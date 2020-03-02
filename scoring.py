class Scorer:
    def __init__(self, df, module_list, sgmods, schoollist, topx):
        print("I'm at scorer function!")
        self.df = df
        self.module_list = module_list
        self.sgmodslist = sgmods
        self.schoollist = schoollist
        self.topx = topx

        self.schoolscore = {}
        self.tuplescore = None
        self.topxscores = None  # top x list of schools
        pass

    def run(self):
        self.schoolscore = self.scoring()
        self.tuplescore = self.get_scores(self.schoolscore)
        self.topxscores = self.topx_scores()  # highest to lowest in list form
        return self.topxscores

    def add_score(self, scorer, school):
        scorer[school] = scorer.get(school, 0) + 1
        return scorer

    def get_scores(self, scorer):
        return tuple(scorer.items())

    def scoring(self):
        checker = []
        for x in range(len(self.module_list)):
            for y in range(len(self.df)):
                if self.module_list[x] in self.sgmodslist[y] and self.schoollist[y] not in checker:
                    self.add_score(self.schoolscore, self.schoollist[y])
                    checker += [self.schoollist[y]]
            checker = []

        return self.schoolscore  # hopefully this actually does something

    def topx_scores(self):
        topxtuplescores = (sorted(self.get_scores(self.schoolscore), key=lambda y: y[1]))[(-1) * int(self.topx):]
        topxlistscores = list(topxtuplescores)
        topxlistscores.reverse()

        return topxlistscores
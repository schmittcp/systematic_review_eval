
class SRResult:
    """ Holds classification results of an algorithm """
    def __init__(self):
        self.tp = 0
        self.tn = 0
        self.fp = 0
        self.fn = 0

    def precision(self):
        if self.tp == 0:
            return 0.0
        return 100. * self.tp / (self.tp + self.fp)

    def recall(self):
        if self.tp == 0:
            return 0.0
        return 100. * self.tp / (self.tp + self.fn)

    def f1(self):
        p, r = self.precision(), self.recall()
        if p + r == 0.0:
            return 0.0
        return 2 * p * r / (p + r)

    def __str__(self):
        return "Classification:\ttp\t"+str(self.tp)+"\tfp "+str(self.fp)+"\tfn "+str(self.fn)+"\tf1 "+str(self.f1())

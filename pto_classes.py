class PPT:
    def __init__(self):
        self.type = 'PPT'
        self.bal = 0
        self.maxCarryover = 48
        self.extraCarryover = 0
        self.cap = 96
        self.accrual = [[0, 0, 0, 18, 8, 8, 8, 6, 0, 0, 0, 0],
                        [18, 8, 8, 8, 6, 0, 0, 0, 0, 0, 0, 0]]

    def forward(self, yearNo, monthNo, sickObj):
        if yearNo > 0 and monthNo == 0:
            self.extraCarryover = max(self.bal - self.maxCarryover, 0)
            self.bal -= self.extraCarryover
            sickObj.extraCarryover = self.extraCarryover
            self.extraCarryover = 0
        self.bal += self.accrual[min(1, yearNo)][monthNo]
        if self.bal > self.cap:
            self.bal = self.cap

    def use(self, qty, year, month):
        if qty > 0:
            if self.bal >= abs(qty):
                self.bal -= abs(qty)
            else:
                print('{} bank insufficient (requested {}, balance {}, Year {}, Month {})'.format(self.type, qty, self.bal, year, month))


class Vac:
    def __init__(self):
        self.type = 'Vac'
        self.bal = 0
        self.maxCarryover = 160
        self.cap = 160
        self.accrual = [6.67,
                        10.0,
                        10.0,
                        10.0,
                        10.0,
                        13.33]
        self.lost = 0

    def forward(self, yearNo):
        self.bal += self.accrual[min(5, yearNo)]
        if self.bal > self.cap:
            self.lost += self.bal - self.cap
            self.bal = self.cap

    def use(self, qty, year, month):
        if qty > 0:
            if self.bal >= abs(qty):
                self.bal -= abs(qty)
            else:
                print('{} bank insufficient (requested {}, balance {}, Year {}, Month {})'.format(self.type, qty, self.bal, year, month))

class Sick:
    def __init__(self):
        self.type = 'Sick'
        self.bal = 0
        self.maxCarryover = 72
        self.cap = 10**8
        self.accrual = 2
        self.extraCarryover = 0
        self.lost = 0

    def forward(self, yearNo, monthNo):
        if yearNo > 0 and monthNo == 0:
            excess = max(0, self.bal + self.extraCarryover - 72)
            self.bal += min(self.extraCarryover - excess, 72)
            self.extraCarryover = 0
            self.lost += excess

        self.bal += self.accrual
        if self.bal > self.cap:
            self.bal = self.cap

    def use(self, qty, year, month):
        if qty > 0:
            if self.bal >= abs(qty):
                self.bal -= abs(qty)
            else:
                print('{} bank insufficient (requested {}, balance {}, Year {}, Month {})'.format(self.type, qty, self.bal, year, month))

from datetime import datetime

from dateutil.relativedelta import relativedelta

from config_loader import config


class FlexiblePTO:
    def __init__(self):
        self.type = 'Flexible'
        self.bal = config['flexible_pto']['start_balance']
        self.maxRollover = config['flexible_pto']['max_rollover']
        self.cap = config['flexible_pto'].get('cap')
        self.annualGrant = config['flexible_pto']['annual_grant']
        self.startDate = datetime.strptime(config['employment_start_date'], '%Y-%m-%d')
        self.lost = 0
        self.accrual = config['flexible_pto']['monthly_accrual']

    def forward(self, eom_date):
        # Initial grant on the 1st year
        monthNo = eom_date.month
        firstYear = eom_date.year == self.startDate.year

        # Rollover event on Jan 1
        if monthNo == 1:
            if self.bal > self.maxRollover:
                self.lost += self.bal - self.maxRollover
                self.bal = self.maxRollover

        # Grant events
        if firstYear and monthNo == self.startDate.month:
            self.bal += self.annualGrant

        if not firstYear and monthNo == 1:
            self.bal += self.annualGrant
        
        # Regular accrual
        self.bal += self.accrual

        # Testing if we're exceeding the cap
        if self.cap is not None:
            if self.bal > self.cap:
                self.lost += self.bal - self.cap
                self.bal = self.cap

    def use(self, qty, eom_date):
        if qty > 0:
            if self.bal >= abs(qty):
                self.bal -= abs(qty)
            else:
                print('{} bank insufficient (requested {}, balance {}, Year {}, Month {})'.format(self.type, qty, self.bal, eom_date.year, eom_date.month))


class StandardPTO:
    def __init__(self):
        self.type = 'Std'
        self.bal = config['standard_pto']['start_balance']
        self.maxRollover = config['standard_pto']['max_rollover']
        self.cap = config['standard_pto'].get('cap')
        self.startDate = datetime.strptime(config['employment_start_date'], '%Y-%m-%d')
        self.lost = 0
        self.accrual = [x / 12 for x in config['standard_pto']['yearly_accrual']]
        self.lost = 0

    def forward(self, eom_date):
        monthNo = eom_date.month
        # tenure_years = eom_date.year - self.startDate.year
        tenure_years = relativedelta(eom_date, self.startDate).years

        # Rollover event on Jan 1
        if monthNo == 1:
            if self.bal > self.maxRollover:
                self.lost += self.bal - self.maxRollover
                self.bal = self.maxRollover

        # Regular accrual
        self.bal += self.accrual[min(6, tenure_years)]

        # Testing if we're exceeding the cap
        if self.cap is not None:
            if self.bal > self.cap:
                self.lost += self.bal - self.cap
                self.bal = self.cap

    def use(self, qty, eom_date):
        if qty > 0:
            if self.bal >= abs(qty):
                self.bal -= abs(qty)
            else:
                print('{} bank insufficient (requested {}, balance {}, Year {}, Month {})'.format(self.type, qty, self.bal, eom_date.year, eom_date.month))

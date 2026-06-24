from datetime import datetime

import pytest

from pto_classes import FlexiblePTO, StandardPTO


TEST_CONFIG = {
    'employment_start_date': '2023-01-01',
    'schedule_file': '/dummy/path.ods',
    'standard_pto': {
        'start_balance': 0,
        'max_rollover': 160,
        'cap': 160,
        'yearly_accrual': [72, 112, 112, 112, 112, 112, 152],
    },
    'flexible_pto': {
        'start_balance': 0,
        'max_rollover': 108,
        'cap': None,
        'annual_grant': 10,
        'monthly_accrual': 5.84,
    },
}


class TestFlexiblePTO:
    def test_accrual(self):
        pto = FlexiblePTO(TEST_CONFIG)
        pto.forward(datetime(2023, 2, 28))
        assert pto.bal == pytest.approx(5.84)

    def test_annual_grant_first_year(self):
        pto = FlexiblePTO(TEST_CONFIG)
        pto.forward(datetime(2023, 1, 31))
        assert pto.bal == pytest.approx(15.84)  # 5.84 + 10 grant

    def test_annual_grant_subsequent_year(self):
        pto = FlexiblePTO(TEST_CONFIG)
        pto.forward(datetime(2024, 1, 31))
        assert pto.bal == pytest.approx(15.84)  # 5.84 + 10 grant in Jan

    def test_no_grant_other_months(self):
        pto = FlexiblePTO(TEST_CONFIG)
        pto.forward(datetime(2024, 2, 29))
        assert pto.bal == pytest.approx(5.84)

    def test_rollover_january(self):
        pto = FlexiblePTO(TEST_CONFIG)
        pto.bal = 120
        pto.forward(datetime(2024, 1, 31))
        assert pto.bal == pytest.approx(15.84 + 108)  # accrual + grant + rollover capped at 108
        assert pto.lost == 12

    def test_cap(self):
        config = dict(TEST_CONFIG)
        config['flexible_pto'] = dict(config['flexible_pto'])
        config['flexible_pto']['cap'] = 50
        pto = FlexiblePTO(config)
        pto.bal = 48
        pto.forward(datetime(2023, 2, 28))
        assert pto.bal == pytest.approx(50)
        assert pto.lost == pytest.approx(3.84)

    def test_use_sufficient(self):
        pto = FlexiblePTO(TEST_CONFIG)
        pto.bal = 20
        result = pto.use(8, datetime(2023, 1, 31))
        assert result is True
        assert pto.bal == 12

    def test_use_insufficient(self):
        pto = FlexiblePTO(TEST_CONFIG)
        pto.bal = 5
        result = pto.use(8, datetime(2023, 1, 31))
        assert result is False
        assert pto.bal == 5


class TestStandardPTO:
    def test_accrual_year0(self):
        pto = StandardPTO(TEST_CONFIG)
        pto.forward(datetime(2023, 1, 31))
        assert pto.bal == pytest.approx(6.0)

    def test_accrual_year1(self):
        pto = StandardPTO(TEST_CONFIG)
        pto.forward(datetime(2024, 1, 31))
        assert pto.bal == pytest.approx(9.33, rel=1e-2)

    def test_rollover_january(self):
        pto = StandardPTO(TEST_CONFIG)
        pto.bal = 170
        pto.forward(datetime(2024, 1, 31))
        # 170 -> rollover to 160 (lost 10) -> accrual +9.33 -> cap 160 (lost 9.33)
        assert pto.bal == 160
        assert pto.lost == pytest.approx(19.33, rel=1e-2)

    def test_cap(self):
        pto = StandardPTO(TEST_CONFIG)
        pto.bal = 155
        pto.forward(datetime(2023, 2, 28))
        assert pto.bal == 160
        assert pto.lost == 1

    def test_use_sufficient(self):
        pto = StandardPTO(TEST_CONFIG)
        pto.bal = 20
        result = pto.use(8, datetime(2023, 1, 31))
        assert result is True
        assert pto.bal == 12

    def test_use_insufficient(self):
        pto = StandardPTO(TEST_CONFIG)
        pto.bal = 5
        result = pto.use(8, datetime(2023, 1, 31))
        assert result is False
        assert pto.bal == 5

from fancyhotel.api.reservations import nights_between


def test_nights_between_counts_nights_not_days():
    assert nights_between("2026-11-10", "2026-11-12") == 2


def test_nights_between_crosses_month_boundary():
    assert nights_between("2026-11-29", "2026-12-02") == 3

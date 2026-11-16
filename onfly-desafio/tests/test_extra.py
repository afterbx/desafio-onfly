"""Testes adicionais (não alteram os fornecidos)."""

from helpers import run_cli


def test_more_than_200_rows_are_read(tmp_path):
    rows = [{"reservation_id": f"R-{i}"} for i in range(250)]
    report = run_cli(tmp_path, rows)
    assert report["summary"]["total_reservations"] == 250
    assert report["summary"]["total_room_nights"] == 250


def test_top_hotels_tie_breaks_by_hotel_id(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H02", "hotel_name": "B", "amount": "100.00"},
            {"reservation_id": "R-2", "hotel_id": "H01", "hotel_name": "A", "amount": "100.00"},
        ],
    )
    assert [h["hotel_id"] for h in report["top_hotels"]] == ["H01", "H02"]


def test_nights_across_year_boundary_with_rooms(tmp_path):
    report = run_cli(
        tmp_path,
        [{"checkin_date": "2024-12-30", "checkout_date": "2025-01-02", "rooms": "2"}],
    )
    assert report["summary"]["total_room_nights"] == 6


def test_no_billable_reservations_gives_zero_average(tmp_path):
    report = run_cli(tmp_path, [{"status": "NO_SHOW"}])
    assert report["summary"]["average_nightly_rate_brl"] == "0.00"
    assert report["by_month"] == []
    assert report["top_hotels"] == []


def test_rounding_half_up_only_at_the_end(tmp_path):
    # 0.005 * 1 BRL por reserva: duas reservas somam 0.01 (arredondar antes daria 0.02)
    rows = [
        {"reservation_id": "R-1", "amount": "0.005"},
        {"reservation_id": "R-2", "amount": "0.005"},
    ]
    report = run_cli(tmp_path, rows)
    assert report["summary"]["total_amount_brl"] == "0.01"

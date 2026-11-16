"""Cálculo de noites ocupadas."""

from __future__ import annotations

from datetime import date


def calculate_room_nights(checkin: date, checkout: date, rooms: int) -> int:
    """Calcula noites de quarto: diferença de dias (não inclusiva) vezes quartos."""
    # CORREÇÃO: usa a diferença real de datas (antes subtraía só o dia do mês)
    return (checkout - checkin).days * rooms

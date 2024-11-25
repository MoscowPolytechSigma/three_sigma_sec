from app.func import calculate_area, calculate_volume
import pytest

def test_1_calculate_area():
    assert calculate_area(7,3) == 21

def test_2_calculate_area():
    assert calculate_area(8,9) == 72

def test_3_calculate_area():
    assert calculate_area(11,11) == 121

def test_1_calculate_volume():
    assert calculate_volume(5,4,5) == 100

def test_2_calculate_volume():
    assert calculate_volume(7,9,43) == 2709

def test_3_calculate_volume():
    assert calculate_volume(8,5,9) == 360

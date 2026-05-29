from vetlog_buddy.vaccinations.strategies import (
    DogVaccinationStrategy,
    CatVaccinationStrategy,
)
from vetlog_buddy.vaccinations.model import VaccineType


class TestDogVaccinationStrategy:
    def test_early_vaccination(self):
        # < 6 weeks
        strategy = DogVaccinationStrategy()
        vaccines = strategy.get_vaccines(5)
        assert len(vaccines) == 1
        assert VaccineType.DEWORMING in vaccines

    def test_first_vaccination(self):
        # 6-11 weeks
        strategy = DogVaccinationStrategy()
        vaccines = strategy.get_vaccines(8)
        assert len(vaccines) == 2
        assert VaccineType.PUPPY in vaccines
        assert VaccineType.DEWORMING in vaccines

    def test_annual_vaccination(self):
        # >= 12 weeks
        strategy = DogVaccinationStrategy()
        vaccines = strategy.get_vaccines(12)
        assert len(vaccines) == 2
        assert VaccineType.C6CV in vaccines


class TestCatVaccinationStrategy:
    def test_early_vaccination(self):
        # < 9 weeks
        strategy = CatVaccinationStrategy()
        vaccines = strategy.get_vaccines(8)
        assert len(vaccines) == 1
        assert VaccineType.DEWORMING in vaccines

    def test_first_vaccination(self):
        # 9-16 weeks
        strategy = CatVaccinationStrategy()
        vaccines = strategy.get_vaccines(10)
        assert len(vaccines) == 5
        assert VaccineType.TRICAT in vaccines

    def test_annual_vaccination(self):
        # >= 17 weeks
        strategy = CatVaccinationStrategy()
        vaccines = strategy.get_vaccines(17)
        assert len(vaccines) == 3
        assert VaccineType.TRICAT in vaccines

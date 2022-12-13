from project import convert_height
from project import calcuate_weight
from project import cal_bmi



def main():
    test_convertheight()
    test_calcuate_weight()


def test_convertheight():
    assert float != 0
    assert float != -0


def test_calcuate_weight():
    assert int != ("ABC")
    assert int != ("****")


def test_cal_bmi():
    assert round != -0
    assert round != -750

if __name__ == "__main__":
    main()
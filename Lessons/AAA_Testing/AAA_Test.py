from AAA import sum_list

def test_sum_list_with_positive_numbers_returns_correct_total():
    numbers = [1, 2, 3, 4, 5]   # Arrange

    result = sum_list(numbers)  # Act

    assert result == 15         # Assert


def test_sum_list_with_empty_list_returns_zero():
    numbers = []                # Arrange

    result = sum_list(numbers)  # Act

    assert result == 0          # Assert

def sum_list(numbers):
    total = 0
    for n in numbers:
        total += n * 2  # BUG!
    return total
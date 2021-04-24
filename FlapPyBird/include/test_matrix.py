import json

import pytest

from matrix import Matrix


@pytest.fixture()
def init_matrix():
    m = Matrix(3, 3)
    m.data[0] = [1, 2, 3]
    m.data[1] = [4, 5, 6]
    m.data[2] = [7, 8, 9]
    return m


@pytest.fixture()
def init_matrix_10():
    m = Matrix(3, 3)
    m.data[0] = [10, 11, 12]
    m.data[1] = [13, 14, 15]
    m.data[2] = [16, 17, 18]
    return m


def compare(matrix_a, matrix_b):
    assert matrix_a.rows == matrix_b.rows
    assert matrix_a.cols == matrix_b.cols
    assert (matrix_a.data == matrix_b.data).all()


def test_add_scalar_to_matrix(init_matrix):
    init_matrix.add(1)

    expected = Matrix(3, 3)
    expected.data[0] = [2, 3, 4]
    expected.data[1] = [5, 6, 7]
    expected.data[2] = [8, 9, 10]

    compare(init_matrix, expected)


def test_add_matrix_to_matrix(init_matrix, init_matrix_10):
    init_matrix.add(init_matrix_10)

    expected = Matrix(3, 3)
    expected.data[0] = [11, 13, 15]
    expected.data[1] = [17, 19, 21]
    expected.data[2] = [23, 25, 27]

    compare(init_matrix, expected)


def test_subtract_matrix_from_matrix(init_matrix, init_matrix_10):
    result = Matrix.subtract(init_matrix_10, init_matrix)

    expected = Matrix(3, 3)
    expected.data[0] = [9, 9, 9]
    expected.data[1] = [9, 9, 9]
    expected.data[2] = [9, 9, 9]

    compare(result, expected)


def test_from_list():
    result = Matrix.from_list([0, 0, 0])
    expected = Matrix(3, 1)

    compare(result, expected)


def test_transpose():
    m = Matrix(2, 2)
    m.data[0] = [1, 2]
    m.data[1] = [3, 4]
    m = Matrix.transpose(m)

    expected = Matrix(2, 2)
    expected.data[0] = [1, 3]
    expected.data[1] = [2, 4]
    compare(m, expected)


def test_matrix_product():
    m = Matrix(2, 3)
    m.data[0] = [1, 2, 3]
    m.data[1] = [4, 5, 6]
    n = Matrix(3, 2)
    n.data[0] = [7, 8]
    n.data[1] = [9, 10]
    n.data[2] = [11, 12]
    result = Matrix.static_multiply(m, n)

    expected = Matrix(2, 2)
    expected.data[0] = [58, 64]
    expected.data[1] = [139, 154]

    compare(result, expected)


def test_scalar_product():
    m = Matrix(3, 2)
    m.data[0] = [1, 2]
    m.data[1] = [3, 4]
    m.data[2] = [5, 6]
    m.multiply(7)
    expected = Matrix(3, 2)
    expected.data[0] = [7, 14]
    expected.data[1] = [21, 28]
    expected.data[2] = [35, 42]
    compare(m, expected)


def test_hadamard_product():
    m = Matrix(3, 2)
    m.data[0] = [1, 2]
    m.data[1] = [3, 4]
    m.data[2] = [5, 6]
    n = Matrix(3, 2)
    n.data[0] = [7, 8]
    n.data[1] = [9, 10]
    n.data[2] = [11, 12]
    m.multiply(n)

    expected = Matrix(3, 2)
    expected.data[0] = [7, 16]
    expected.data[1] = [27, 40]
    expected.data[2] = [55, 72]

    compare(m, expected)


def test_static_mapping(init_matrix):
    m = Matrix.static_map(init_matrix, lambda e, i, j: e * 10)
    expected = Matrix(3, 3)
    expected.data[0] = [10, 20, 30]
    expected.data[1] = [40, 50, 60]
    expected.data[2] = [70, 80, 90]
    compare(m, expected)


def test_mapping(init_matrix):
    init_matrix.map(lambda e, i, j: e * 10)
    expected = Matrix(3, 3)
    expected.data[0] = [10, 20, 30]
    expected.data[1] = [40, 50, 60]
    expected.data[2] = [70, 80, 90]
    compare(init_matrix, expected)


def test_print(init_matrix, capsys):
    init_matrix.print()
    out, err = capsys.readouterr()
    assert out == "[[1. 2. 3.]\n [4. 5. 6.]\n [7. 8. 9.]]\n"
    assert type(init_matrix.print()) is Matrix


def test_to_list(init_matrix):
    assert (init_matrix.to_list() == [1, 2, 3, 4, 5, 6, 7, 8, 9]).all()

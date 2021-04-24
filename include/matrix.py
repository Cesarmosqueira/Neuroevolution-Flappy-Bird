import random as rnd

import numpy as np


class Matrix():

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.data = np.zeros((rows, cols))

    @staticmethod
    def from_list(arr: list) -> 'Matrix':
        return Matrix(len(arr), 1).map(lambda e, i, j: arr[i])

    @staticmethod
    def subtract(matrix_a: 'Matrix', matrix_b: 'Matrix') -> 'Matrix':
        if matrix_a.rows is not matrix_b.rows or matrix_a.cols is not matrix_b.cols:
            print('Columns and Rows of A must match Columns and Rows of B.')
            return
        return Matrix(matrix_a.rows, matrix_a.cols).map(lambda e, i, j: matrix_a.data[i][j] - matrix_b.data[i][j])

    @staticmethod
    def static_multiply(matrix_a: 'Matrix', matrix_b: 'Matrix') -> 'Matrix':
        if matrix_a.cols is not matrix_b.rows:
            print('Columns of A must Math rows of B.')
            return
        return Matrix(matrix_a.rows, matrix_b.cols).map(lambda e, i, j: sum([matrix_a.data[i][k] * matrix_b.data[k][j] for k in range(matrix_a.cols)]))

    @staticmethod
    def static_map(matrix: 'Matrix', func) -> 'Matrix':
        return Matrix(matrix.rows, matrix.cols).map(lambda e, i, j: func(matrix.data[i][j], i, j))

    @staticmethod
    def transpose(matrix: 'Matrix') -> 'Matrix':
        return Matrix(matrix.cols, matrix.rows).map(lambda e, i, j: matrix.data[j][i])
    
    def copy(self):
        mat = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                mat.data[i][j] = self.data[i][j]
        return mat

    def add(self, n: int) -> 'Matrix':
        if type(n) is Matrix:
            if self.rows is not n.rows or self.cols is not n.cols:
                print('Columns and Rows of A must match Columns and Rows of B.')
                return
            return self.map(lambda e, i, j: e+n.data[i][j])
        else:
            return self.map(lambda e, i, j: e + n)

    def multiply(self, matrix_a: 'Matrix') -> 'Matrix':
        if type(matrix_a) is Matrix:
            if self.rows is not matrix_a.rows or self.cols is not matrix_a.cols:
                print('Columns and Rows of A must match Columns and Rows of B.')
                return
            return self.map(lambda e, i, j: e * matrix_a.data[i][j])
        else:
            return self.map(lambda e, i, j: e * matrix_a)

    def map(self, func) -> 'Matrix':
        for row in range(self.rows):
            for col in range(self.cols):
                tmp = self.data[row][col]
                self.data[row][col] = func(tmp, row, col)
        return self

    def randomize(self) -> 'Matrix':
        return self.map(lambda e, i, j: rnd.random() * 2 - 1)

    def to_list(self) -> np.array:
        return np.array(self.data).flatten()

    def print(self) -> 'Matrix':
        print(self.data)
        return self

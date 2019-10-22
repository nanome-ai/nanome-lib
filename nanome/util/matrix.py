from . import Vector3, Quaternion

import random
import operator
import sys
import unittest

class MatrixException(Exception):
    pass

class Matrix(object):
    def __init__(self, m, n):
        self.__rows = [[0] * n for i in range(m)]
        self.__m = m
        self.__n = n
        
    def __getitem__(self, m):
        return self.__rows[m]

    def __setitem__(self, m, row):
        self.__rows[m] = row
        
    def __str__(self):
        s = '\n'.join([' '.join([str(item) for item in row]) for row in self.__rows])
        return s

    def __eq__(self, matrix):
        return matrix.__rows == self.__rows
        
    def __add__(self, matrix):
        if self.get_rank() != matrix.get_rank():
            raise MatrixException("Only matrices of same rank can be added")

        result = Matrix(self.__m, self.__n)
        
        for i in range(self.__m):
            result[i] = [cur[0] + cur[1] for cur in zip(self.__rows[i], matrix[i])]

        return result

    def __sub__(self, matrix):
        if self.get_rank() != matrix.get_rank():
            raise MatrixException("Only matrices of same rank can be subtracted")

        result = Matrix(self.__m, self.__n)
        
        for i in range(self.__m):
            result[i] = [cur[0] - cur[1] for cur in zip(self.__rows[i], matrix[i])]

        return result

    def __mul__(self, matrix):
        is_vector = False
        if isinstance(matrix, Vector3):
            matrix = Matrix.from_vector3(matrix)
            is_vector = True

        rank_m, rank_n = matrix.get_rank()
        if self.__n != rank_m:
            raise MatrixException("Trying to multiply a matrix with n=" + str(self.__n) + " by a matrix with m=" + str(rank_m))
        
        transpose = matrix.get_transpose()
        result = Matrix(self.__m, rank_n)
        
        for i in range(self.__m):
            for j in range(transpose.__m):
                result[i][j] = sum([cur[0] * cur[1] for cur in zip(self.__rows[i], transpose[j])])

        if is_vector:
            result = Vector3(result[0][0], result[1][0], result[2][0])
        return result

    def __iadd__(self, matrix):
        if self.get_rank() != matrix.get_rank():
            raise MatrixException("Only matrices of same rank can be added")

        for i in range(self.__m):
            for j in range(self.__n):
                self.__rows[i][j] += matrix.__rows[i][j]
        return self

    def __isub__(self, matrix):
        if self.get_rank() != matrix.get_rank():
            raise MatrixException("Only matrices of same rank can be subtracted")

        for i in range(self.__m):
            for j in range(self.__n):
                self.__rows[i][j] -= matrix.__rows[i][j]
        return self

    def transpose(self):
        self.__m, self.__n = self.__n, self.__m
        self.__rows = Matrix.__transpose_rows(self.__rows, self.__m, self.__n)
        return self

    def get_transpose(self):
        result = Matrix(self.__n, self.__m)
        result.__rows = Matrix.__transpose_rows(self.__rows, self.__m, self.__n)
        return result

    @staticmethod
    def __transpose_rows(rows, m, n):
        return [[rows[j][i] for j in range(m)] for i in range(n)]

    def get_minor(self, i, j):
        rows = [row[:j] + row[j+1:] for row in (self.__rows[:i] + self.__rows[i+1:])]
        result = Matrix(len(rows), len(rows[0]))
        result.__rows = rows
        return result

    def get_determinant(self):
        rows = self.__rows
        if self.__m == 2 and self.__n == 2:
            return rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]

        result = 0
        for j in range(self.__n):
            result += ((-1) ** j) * rows[0][j] * self.get_minor(0, j).get_determinant()
        return result

    def get_inverse(self):
        determinant = self.get_determinant()
        rows = self.__rows
        if self.__m == 2 and self.__n == 2:
            return [[rows[1][1] / determinant, -rows[0][1] / determinant], [-rows[1][0] / determinant, rows[0][0] / determinant]]

        result = Matrix(self.__m, self.__n)
        for i in range(self.__m):
            for j in range(self.__n):
                minor = self.get_minor(i, j)
                result[i][j] = (((-1) ** (i + j)) * minor.get_determinant()) / determinant
        result.transpose()
        return result

    def get_rank(self):
        return (self.__m, self.__n)

    @classmethod
    def identity(cls, size):
        result = cls(size, size)
        for i in range(size):
            result.__rows[i][i] = 1
        return result

    @classmethod
    def from_vector3(cls, vector):
        result = cls(4, 1)
        result[0][0] = vector.x
        result[1][0] = vector.y
        result[2][0] = vector.z
        result[3][0] = 1
        return result

    @classmethod
    def from_quaternion(cls, quaternion):
        result = cls(4, 4)
        result[0][0] = 1 - 2 * quaternion.y * quaternion.y - 2 * quaternion.z * quaternion.z
        result[0][1] = 2 * quaternion.x * quaternion.y - 2 * quaternion.z * quaternion.w
        result[0][2] = 2 * quaternion.x * quaternion.z + 2 * quaternion.y * quaternion.w
        result[1][0] = 2 * quaternion.x * quaternion.y + 2 * quaternion.z * quaternion.w
        result[1][1] = 1 - 2 * quaternion.x * quaternion.x - 2 * quaternion.z * quaternion.z
        result[1][2] = 2 * quaternion.y * quaternion.z - 2 * quaternion.x * quaternion.w
        result[2][0] = 2 * quaternion.x * quaternion.z - 2 * quaternion.y * quaternion.w
        result[2][1] = 2 * quaternion.y * quaternion.z + 2 * quaternion.x * quaternion.w
        result[2][2] = 1 - 2 * quaternion.x * quaternion.x - 2 * quaternion.y * quaternion.y
        result[3][3] = 1
        return result
    
    @classmethod
    def compose_transformation_matrix(cls, position, rotation, scale = None):
        if (scale is None):
            return cls._compose_transformation_matrix(position, rotation)
        if not isinstance(position, Vector3) or not isinstance(rotation, Quaternion) or not isinstance(scale, Vector3):
            raise ValueError("compose_translation_matrix expects a Vector3, a Quaternion, and a Vector3.\n Received (" + str(type(position)) + ", " + str(type(rotation)) + ", " + str(type(scale)) + ")")
        S = cls(4,4)
        S[0][0] = scale.x
        S[1][1] = scale.y
        S[2][2] = scale.z
        S[3][3] = 1
        R = cls.from_quaternion(rotation)
        T = cls.identity(4)
        T[0][3] = position.x
        T[1][3] = position.y
        T[2][3] = position.z
        result = T*(R*S)
        return result

    @classmethod
    def _compose_transformation_matrix(cls, position, rotation):
        if not isinstance(position, Vector3) or not isinstance(rotation, Quaternion):
            raise ValueError("compose_translation_matrix expects a Vector3, a Quaternion")
        R = cls.from_quaternion(rotation)
        T = cls.identity(4)
        T[0][3] = position.x
        T[1][3] = position.y
        T[2][3] = position.z
        result = T*R
        return result
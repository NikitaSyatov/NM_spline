#!/bin/env python
# -*- coding: utf-8 -*-
# ./.venv/bin/python

from progon import Progonka
import numpy as np
import pandas as pd
import math


def test_func(x: float):
    if x >= -1 and x <= 0:
        return x**3 + 3 * (x**2)
    if x > 0 and x <= 1:
        return -(x**3) + 3 * (x**2)


def d_test_func(x: float):
    if x >= -1 and x <= 0:
        return 3 * x**2 + 6 * x
    if x > 0 and x <= 1:
        return -3 * (x**2) + 6 * x


def dd_test_func(x: float):
    if x >= -1 and x <= 0:
        return 6 * x + 6
    if x > 0 and x <= 1:
        return -6 * x + 6


def func1(x: float):
    return np.sqrt(x**2 - 1) / x


def d_func1(x: float):
    return 1 / np.sqrt(x**2 - 1) - np.sqrt(x**2 - 1) / (x**2)


def dd_func1(x: float):
    return (
        -(x / (np.sqrt((x**2 - 1) ** 2)))
        - (1 / x * np.sqrt(x**2 - 1))
        - ((2 * np.sqrt(x**2 - 1)) / (x**3))
    )


def func2(x: float):
    return (1 + x**2) ** (1 / 3)


def d_func2(x: float):
    return (2 * x) / (3 * ((1 + x**2) ** (2 / 3)))


def dd_func2(x: float):
    return (2 / (3 * ((1 + x**2) ** (2 / 3)))) - ((8 * x**2) / (9 * (1 + x**2) ** 2))


def func3(x: float):
    return np.sin(x + 1) / x + 1


def d_func3(x: float):
    return np.cos(x + 1) / (x + 1) - np.sin(x + 1) / ((x + 1) ** 2)


def dd_func3(x: float):
    return (
        -(np.sin(x + 1) / (x + 1))
        - (np.cos(x + 1) / ((x + 1) ** 2))
        - (np.cos(x + 1) / ((x + 1) ** 3))
        + 2 * (np.sin(x + 1) / ((x + 1) ** 3))
    )


def oscilate1(func, x):
    return func(x) + np.cos(10 * x)


def d_oscilate1(dfunc, x):
    return dfunc(x) - 10 * np.sin(10 * x)


def dd_oscilate1(ddfunc, x):
    return ddfunc(x) - 100 * np.cos(10 * x)


def oscilate2(func, x):
    return func(x) + np.cos(100 * x)


def d_oscilate2(dfunc, x):
    return dfunc(x) - 100 * np.sin(100 * x)


def dd_oscilate2(ddfunc, x):
    return ddfunc(x) - 100 * 100 * np.cos(100 * x)


def spline(xj, n, a, b, c, d, bord: list, x):
    h = (bord[1] - bord[0]) / n
    xj = np.array(xj)
    i = np.where(x <= xj)[0][0] - 1
    xi = xj[i]
    return (
        a[i]
        + b[i] * (x - xi)
        + (c[i] / 2) * ((x - xi) ** 2)
        + (d[i] / 6) * ((x - xi) ** 3)
    )


def d_spline(xj, n, a, b, c, d, bord: list, x):
    h = (bord[1] - bord[0]) / n
    xj = np.array(xj)
    i = np.where(x <= xj)[0][0] - 1
    xi = xj[i]
    return b[i] + c[i] * ((x - xi)) + (d[i] / 2) * ((x - xi) ** 2)


def dd_spline(xj, n, a, b, c, d, bord: list, x):
    h = (bord[1] - bord[0]) / n
    xj = np.array(xj)
    i = np.argmin(np.abs(xj - x))
    i = np.where(x <= xj)[0][0] - 1
    xi = xj[i]
    return c[i] + d[i] * ((x - xi))


def build_spline(n, bord, f, d_f, dd_f):
    h = (bord[1] - bord[0]) / n
    x_bord_left = [bord[0] + i * h for i in range(0, n)]
    x_bord_right = [bord[0] + i * h for i in range(1, n + 1)]
    C_matrix = [
        [1, 0, 0],
    ]
    vector = [
        bord[0],
    ]
    for i in range(1, n):
        C_matrix.append([h, 4 * h, h])
        vector.append(
            6
            * (
                (f(bord[0] + h * (i + 1)) - f(bord[0] + i * h)) / h
                - (f(bord[0] + i * h) - f(bord[0] + h * (i - 1))) / h
            )
        )
    C_matrix.append([0, 0, 1])
    vector.append(bord[1])
    c = Progonka(C_matrix, vector)
    a = []
    b = []
    d = []
    for i in range(1, n + 1):
        a.append(f(bord[0] + i * h))
        d.append((c[i] - c[i - 1]) / h)
        b.append(
            (f(bord[0] + i * h) - f(bord[0] - h + i * h)) / h
            + c[i] * h / 3
            + c[i - 1] * h / 6
        )
    # dataframe 1
    df1 = pd.DataFrame(
        data={
            "xi-1": x_bord_left,
            "xi": x_bord_right,
            "a": a,
            "b": b,
            "c": c[1:],
            "d": d,
        }
    )
    # dataframe 2
    N = 2 * n
    H = (bord[1] - bord[0]) / N
    xj = [bord[0] + i * H for i in range(0, N + 1)]
    x_old = x_bord_left
    x_old.append(x_bord_right[-1])
    F = np.vectorize(lambda x: f(x))
    F_list = F(xj)
    S = np.vectorize(lambda x: spline(x_old, n, a, b, c, d, bord, x))
    S_list = S(xj)
    dF = np.vectorize(lambda x: d_f(x))
    dF_list = dF(xj)
    dS = np.vectorize(lambda x: d_spline(x_old, n, a, b, c, d, bord, x))
    dS_list = dS(xj)
    df2 = pd.DataFrame(
        data={
            "xj": xj,
            "F(xj)": F_list,
            "S(xj)": S_list,
            "|F(xj) - S(xj)|": np.abs(F_list - S_list),
            "F'(xj)": dF_list,
            "S'(xj)": dS_list,
            "|F'(xj) - S'(xj)|": np.abs(dF_list - dS_list),
        }
    )
    # DataFrame 3
    ddF = np.vectorize(lambda x: dd_f(x))
    ddF_list = ddF(xj)
    ddS = np.vectorize(lambda x: dd_spline(x_old, n, a, b, c, d, bord, x))
    ddS_list = ddS(xj)
    df3 = pd.DataFrame(
        data={
            "xj": xj,
            "F''(xj)": ddF_list,
            "S''(xj)": ddS_list,
            "|F''(xj) - S''(xj)|": np.abs(ddF_list - ddS_list),
        }
    )
    df1.to_csv(
        "koef_abcd.csv",
        index=False,
    )
    df2.to_csv(
        "diffFS.csv",
        index=False,
    )
    df3.to_csv(
        "d_diffFS.csv",
        index=False,
    )
    return 0


if __name__ == "__main__":
    # bord = [-1, 1]  # test func
    bord = [2, 4]  # func1
    build_spline(10, bord, func3, d_func3, dd_func3)

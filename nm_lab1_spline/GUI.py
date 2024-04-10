#!/bin/env python
# -*- coding: utf-8 -*-
# ./.venv/bin/python

import PySimpleGUI as sg
import build_spline as sp
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import sys
import traceback

sg.theme("SystemDefaultForReal")

df_tmp = pd.DataFrame(
    {
        " 1 ": [],
        "     2     ": [],
        "     3     ": [],
        "     4     ": [],
        "     5     ": [],
        "     6     ": [],
        "     7     ": [],
    }
)
df_tmp1 = pd.DataFrame(
    {
        "     1     ": [],
        "     2     ": [],
        "       3       ": [],
        "       4       ": [],
    }
)
df_tmp2 = pd.DataFrame(
    {
        "     1     ": [],
        "     2     ": [],
        "       3       ": [],
        "       4       ": [],
    }
)
fig, graf = plt.subplots(figsize=(5, 5))

list_q = ["Тестовая", "1", "2", "3"]

list_q1 = ["+ 0", "+ cos10x", "+ cos100x"]

frame_output_data = [
    [sg.Output(size=(100, 17), key="-DATA-")],
    [sg.Button("Clear", size=(100, 1))],
]

column1 = [
    [sg.DropDown(list_q, default_value=list_q[0], size=(25, 1), key="-SELECTOR-")],
    [sg.DropDown(list_q1, default_value=list_q1[0], size=(25, 1), key="-SELECTOR1-")],
    [sg.Text("Количество участков разбиений", size=(50, 1))],
    [sg.InputText(default_text="10", size=(27, 1), key="-N-")],
    [sg.Submit(size=(24, 1))],
    [sg.Exit(size=(24, 1))],
]

column_table1 = [
    [
        sg.Table(
            values=df_tmp.values.tolist(),
            headings=df_tmp.columns.tolist(),
            # alternating_row_color="darkblue",
            key="-TABLE1-",
            vertical_scroll_only=False,
            row_height=25,
            size=(600, 600),
            justification="left",
        )
    ],
]

column_table2 = [
    [
        sg.Table(
            values=df_tmp1.values.tolist(),
            headings=df_tmp1.columns.tolist(),
            # alternating_row_color="darkblue",
            key="-TABLE2-",
            vertical_scroll_only=False,
            row_height=25,
            size=(600, 600),
            justification="left",
        )
    ],
]

column_table3 = [
    [
        sg.Table(
            values=df_tmp2.values.tolist(),
            headings=df_tmp2.columns.tolist(),
            # alternating_row_color="darkblue",
            key="-TABLE3-",
            vertical_scroll_only=False,
            row_height=25,
            size=(600, 600),
            justification="left",
        )
    ],
]

column_graf = [
    [sg.Canvas(key="-CANVAS-")],
]

button_column = [
    [sg.Button("Функция F(x)", size=(40, 1), key=("-BUT1-"))],
    [sg.Button("Сплайн S(x)", size=(40, 1), key=("-BUT2-"))],
    [sg.Button("S'(x)", size=(40, 1), key=("-BUT3-"))],
    [sg.Button("F'(x)", size=(40, 1), key=("-BUT4-"))],
    [sg.Button("S''(x)", size=(40, 1), key=("-BUT5-"))],
    [sg.Button("F''(x)", size=(40, 1), key=("-BUT6-"))],
    [sg.Button("|F(x) - S(x)|", size=(40, 1), key=("-BUT7-"))],
    [sg.Button("|F'(x) - S'(x)|", size=(40, 1), key=("-BUT8-"))],
    [sg.Button("|F''(x| - S''(x)", size=(40, 1), key=("-BUT9-"))],
]

# In[]:
layout = [
    [
        sg.Column(column1),
        sg.VerticalSeparator(),
        sg.Column(button_column),
        # sg.Frame("Данные", frame_output_data, element_justification="right"),
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Frame(
            "Таблицы",
            [
                [
                    sg.TabGroup(
                        [
                            [
                                sg.Tab(
                                    "koef: a, b, c, d",
                                    column_table1,
                                    key="-TAB1-",
                                ),
                                sg.Tab(
                                    "dif: F, d_F",
                                    column_table2,
                                    key="-TAB2-",
                                ),
                                sg.Tab(
                                    "d_dif: dd_F, dd_S",
                                    column_table3,
                                    key="-TAB2-",
                                ),
                            ],
                        ],
                        key="-TABLE-",
                        size=(1000, 1000),
                    )
                ]
            ],
            element_justification="left",
            key="-SIZETABLE-",
        ),
        sg.VerticalSeparator(),
        sg.Column(
            column_graf, size=(400, 400), justification="right", key="-SIZEGRAF-"
        ),
    ],
]

window = sg.Window(
    "Построение сплайнов",
    layout,
    finalize=True,
    resizable=True,
    grab_anywhere=True,
)

last_w_size = window.size

canvas_elem = window["-CANVAS-"]
canvas = FigureCanvasTkAgg(fig, master=canvas_elem.Widget)
canvas.get_tk_widget().pack(side="top", fill="both", expand=True)


def update_title(table, headings, df):
    for cid, text in zip(df.columns.tolist(), headings):
        table.heading(cid, text=text)


def on_resize(event):
    if last_w_size != window.size:
        width, height = window.size
        window.Element("-SIZETABLE-").set_size((window.size[0] / 2, window.size[1]))
        window.Element("-SIZEGRAF-").set_size(
            (window.size[0] / 2, window.size[1] / 1.4)
        )
        window.Element("-CANVAS-").set_size((window.size[0] / 2, window.size[1] / 1.4))
        canvas_elem.Widget.pack(side="top", fill="both", expand=True)
        # window.FindElement("-DATA-").Update("")


list_selector = [
    [
        [sp.test_func, sp.d_test_func, sp.dd_test_func],
        [sp.func1, sp.d_func1, sp.dd_func1],
        [sp.func2, sp.func2, sp.dd_func2],
        [sp.func3, sp.d_func3, sp.dd_func3],
    ],
    [
        [
            lambda x: sp.oscilate1(func=sp.test_func, x=x),
            lambda x: sp.oscilate1(func=sp.d_test_func, x=x),
            lambda x: sp.oscilate1(func=sp.dd_test_func, x=x),
        ],
        [
            lambda x: sp.oscilate1(func=sp.func1, x=x),
            lambda x: sp.oscilate1(func=sp.d_func1, x=x),
            lambda x: sp.oscilate1(func=sp.dd_func1, x=x),
        ],
        [
            lambda x: sp.oscilate1(func=sp.func2, x=x),
            lambda x: sp.oscilate1(func=sp.d_func2, x=x),
            lambda x: sp.oscilate1(func=sp.dd_func2, x=x),
        ],
        [
            lambda x: sp.oscilate1(func=sp.func3, x=x),
            lambda x: sp.oscilate1(func=sp.d_func3, x=x),
            lambda x: sp.oscilate1(func=sp.dd_func3, x=x),
        ],
    ],
    [
        [
            lambda x: sp.oscilate2(func=sp.test_func, x=x),
            lambda x: sp.oscilate2(func=sp.d_test_func, x=x),
            lambda x: sp.oscilate2(func=sp.dd_test_func, x=x),
        ],
        [
            lambda x: sp.oscilate2(func=sp.func1, x=x),
            lambda x: sp.oscilate2(func=sp.d_func1, x=x),
            lambda x: sp.oscilate2(func=sp.dd_func1, x=x),
        ],
        [
            lambda x: sp.oscilate2(func=sp.func2, x=x),
            lambda x: sp.oscilate2(func=sp.d_func2, x=x),
            lambda x: sp.oscilate2(func=sp.dd_func2, x=x),
        ],
        [
            lambda x: sp.oscilate2(func=sp.func3, x=x),
            lambda x: sp.oscilate2(func=sp.d_func3, x=x),
            lambda x: sp.oscilate2(func=sp.dd_func3, x=x),
        ],
    ],
]

list_bord = [
    [-1, 1],
    [2, 4],
    [0, 1],
    [0, 2],
]


def create_spline(select1, select2, N):
    sp.build_spline(
        N,
        list_bord[select1],
        list_selector[select2][select1][0],
        list_selector[select2][select1][1],
        list_selector[select2][select1][2],
    )


window.TKroot.bind("<Configure>", on_resize)

while True:
    event, values = window.read()
    # window.FindElement("-DATA-").Update("")
    if event in (None, "Exit", "Cancel"):
        break
    if event == "Submit":
        selector1 = values["-SELECTOR-"]
        sel1 = list_q.index(selector1)
        selector2 = values["-SELECTOR1-"]
        sel2 = list_q1.index(selector2)
        n = int(window.Element("-N-").Get())

        create_spline(sel1, sel2, n)

        df1 = pd.read_csv("koef_abcd.csv")
        df2 = pd.read_csv("diffFS.csv")
        df3 = pd.read_csv("d_diffFS.csv")

        table1 = window.Element("-TABLE1-").Widget
        update_title(table1, df1.columns.tolist(), df_tmp)
        window.Element("-TABLE1-").Update(values=df1.values.tolist())

        table2 = window.Element("-TABLE2-").Widget
        update_title(table2, df2.columns.tolist(), df_tmp1)
        window.Element("-TABLE2-").Update(values=df2.values.tolist())

        table3 = window.Element("-TABLE3-").Widget
        update_title(table3, df3.columns.tolist(), df_tmp2)
        window.Element("-TABLE3-").Update(values=df3.values.tolist())
    if event == "-BUT1-":
        graf = plt.plot(df2["xj"], df2["F(xj)"])
    if event == "-BUT2-":
        graf = plt.plot(df2["xj"], df2["S(xj)"])
    if event == "-BUT3-":
        graf = plt.plot(df2["xj"], df2["S'(xj)"])
    if event == "-BUT4-":
        graf = plt.plot(df2["xj"], df2["F'(xj)"])
    if event == "-BUT5-":
        graf = plt.plot(df3["xj"], df3["S''(xj)"])
    if event == "-BUT6-":
        graf = plt.plot(df3["xj"], df3["F''(xj)"])
    if event == "-BUT7-":
        graf = plt.plot(df2["xj"], df2["|F(xj) - S(xj)|"])
    if event == "-BUT8-":
        graf = plt.plot(df2["xj"], df2["|F'(xj) - S'(xj)|"])
    if event == "-BUT9-":
        graf = plt.plot(df3["xj"], df3["|F''(xj) - S''(xj)|"])
    canvas.draw()
    if event == "Clear":
        fig.clear()
        canvas.draw()


window.close()

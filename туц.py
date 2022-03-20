import random
import numpy
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Point(object):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.point = "+"
        self.b = 0
        self.f = -1
        self.k = -1


N = 20
n = 2
list_points = []

window = Tk()
window.geometry()
window.title("Денис Бабкин")
first_frame = Frame()
first_frame.pack(side=LEFT)
second_frame = Frame()
second_frame.pack(side=RIGHT)

fig, ax = plt.subplots(figsize=(4, 4))

canvas1 = FigureCanvasTkAgg(fig, master=first_frame)


def info_window():
    info_window = Toplevel();
    info_window.resizable(width=False, height=False)
    info_window.title("Explorer.Dialog")
    lbl = Label(info_window, text="Вы уверены, что хотите сгенерировать новые точки?  Старые будут удалены!")
    lbl.pack(side='top', ipadx=4, padx=1, ipady=3, pady=3)
    frame_1 = Frame(info_window)
    frame_1.pack(side=TOP)
    destroy1_window_btn = Button(frame_1, text="Да", command=lambda: [info_window.destroy(), generate_points()],
                                 width=15)
    destroy1_window_btn.pack(side='left', ipadx=6, padx=4, ipady=5, pady=5)
    destroy2_window_btn = Button(frame_1, text="Нет", command=info_window.destroy, width=15)
    destroy2_window_btn.pack(side='left', ipadx=6, padx=4, ipady=5, pady=5)
    info_window.focus_set()
    info_window.grab_set()
    info_window.mainloop()


def paint():
    ax.clear()
    ax.add_patch(plt.Circle((n, n), n, color='k', fill=None))
    x1 = numpy.linspace(-2, 4, 100)
    y1 = n + x1
    x2 = numpy.linspace(-2, 4, 100)
    y2 = n * 2 - x2
    plt.plot(x1, y1, color="k", ms=1)
    plt.plot(x2, y2, color="k", ms=1)
    ax.set_xlabel('f1')
    ax.set_ylabel('f2')


def generate_points():
    paint()
    list_points.clear()
    for d in range(20):
        try:
            table_view.delete(d)
        except:
            break

    while len(list_points) != N:
        X = random.randint(0, 2 * n) + (random.randint(-5, 5) / 10)
        Y = random.randint(0, 2 * n) + (random.randint(-5, 5) / 10)

        if ((X - n) ** 2 + (Y - n) ** 2 <= n ** 2) and (-X + Y <= n) and (X + Y >= 2 * n):
            list_points.append(Point(X, Y))
            plt.plot(X, Y, "o", mfc='r', mec="r", ms=3)
            ax.text(X - 0.1, Y + 0.1, len(list_points), fontsize=8)

    for i in range(len(list_points)):

        if list_points[i].point != "-":
            for k in range(len(list_points)):
                if k != i:
                    if list_points[k].X <= list_points[i].X and list_points[k].Y <= list_points[i].Y:
                        list_points[k].point = "-"

        for k in range(len(list_points)):
            if k != i:
                if list_points[k].X >= list_points[i].X and list_points[k].Y >= list_points[i].Y:
                    list_points[i].b += 1

        list_points[i].f = round((1 / (1 + list_points[i].b / (N - 1))), 3)
        K = [abs(1 - list_points[i].f), abs(0.85 - list_points[i].f), abs(0.75 - list_points[i].f)]
        if K.index(min(K)) == 0:
            list_points[i].k = 1
        elif K.index(min(K)) == 1:
            list_points[i].k = 2
        else:
            list_points[i].k = 3

        table_view.insert(parent='', index='end', iid=i, text='',
                          values=(i + 1, list_points[i].X, list_points[i].Y, list_points[i].b, list_points[i].f,
                                  list_points[i].k))

    canvas1.draw()


def optimization():
    if len(list_points) == 0:
        messagebox.showinfo("Optimization.com", "Сначала сгенерируйте точки!")
    else:
        paint()
        for i in range(len(list_points)):
            if list_points[i].point == "+":
                plt.plot(list_points[i].X, list_points[i].Y, "o", mfc='r', mec="r", ms=3)
                ax.text(list_points[i].X - 0.4, list_points[i].Y + 0.4, i + 1)
        canvas1.draw()


def view_all():
    if len(list_points) == 0:
        messagebox.showinfo("Optimization.com", "Сначала сгенерируйте точки!")
    else:
        paint()

        for i in range(len(list_points)):
            plt.plot(list_points[i].X, list_points[i].Y, "o", mfc='r', mec="r", ms=3)
            ax.text(list_points[i].X - 0.4, list_points[i].Y + 0.4, i + 1)
        canvas1.draw()


table_view = ttk.Treeview(second_frame, height=20)

table_view['columns'] = ('№', 'f1', 'f2', 'b', 'F', 'K')

table_view.column("#0", width=0, stretch=NO)
table_view.column('№', anchor=CENTER, width=40)
table_view.column("f1", anchor=CENTER, width=59)
table_view.column("f2", anchor=CENTER, width=59)
table_view.column("b", anchor=CENTER, width=59)
table_view.column("F", anchor=CENTER, width=59)
table_view.column("K", anchor=CENTER, width=59)

table_view.heading("#0", text="", anchor=CENTER)
table_view.heading('№', text='№', anchor=CENTER)
table_view.heading("f1", text="f1", anchor=CENTER)
table_view.heading("f2", text="f2", anchor=CENTER)
table_view.heading("b", text="b", anchor=CENTER)
table_view.heading("F", text="F", anchor=CENTER)
table_view.heading("K", text="K", anchor=CENTER)

table_view.pack(side=TOP, ipadx=6, padx=4, ipady=4, pady=5, fill=Y)

generate_btn = Button(first_frame, text="Сгенерировать точки", command=info_window, width=40)
generate_btn.pack(side=TOP, fill=X, ipadx=6, padx=4, ipady=4, pady=5)
optimization_btn = Button(first_frame, text="Показать оптимальные решения", command=optimization)
optimization_btn.pack(side=TOP, fill=X, ipadx=6, padx=4, ipady=4, pady=0, )
prosto_btn = Button(first_frame, text="Показать все решения", command=view_all)
prosto_btn.pack(side=TOP, fill=X, ipadx=6, padx=4, ipady=4, pady=5)

canvas1.get_tk_widget().pack(side=TOP, ipadx=6, padx=4, ipady=4, pady=5)

paint()

window.resizable(width=False, height=False)

canvas1.draw()
window.mainloop()

"""Guass Jordan GUI

This app creates two editable matrices:
- Matrix A: m x n (editable grid)
- Matrix B: m x 1 (editable column vector)

Enter m and n, click "Create Matrices", edit any cell directly, then click
"Solve". The external function `solve(a, b)` will be called with both matrices.

Values are parsed to int or float when possible; empty cells become 0.
"""

import tkinter as tk
from tkinter import messagebox, ttk

from guass_jordan import gauss_jordan


def display_matrix(a):
    for row in a:
        for col in row:
            print(col, end="\t")
        print()


def arrange_rows(a, b):
    # this function is important as it prevents the program from assuming that a variable is a free variable just because the current arrangement makes it seem like it
    print(a, b)
    display_matrix(a)
    display_matrix(b)
    for i in range(len(a)):
        for j in range(len(a[0])):
            if i != j:
                continue
            else:
                if a[i][j] == 0:
                    for k in range(i + 1, len(a)):
                        if a[k][j] != 0:
                            a[i], a[k] = a[k], a[i]
                            b[i], b[k] = b[k], b[i]
    display_matrix(a)
    display_matrix(b)
    return a, b


def solve(a_matrix, b_matrix):
    a_matrix, b_matrix = arrange_rows(a_matrix, b_matrix)
    solutions = gauss_jordan(a_matrix, b_matrix)
    message = ""
    for sol in solutions:
        message += f"solution for {sol[0]} = {sol[1]}\n"
    messagebox.showinfo("Solve called", message)


class MatrixEditorApp:
    def __init__(self, root):
        # the window to which the program will be attached
        self.root = root
        root.title("Guass Jordan Implementation")

        ctrl_frame = ttk.Frame(root, padding=(10, 8))
        ctrl_frame.pack(fill="x")

        # Input section
        ttk.Label(ctrl_frame, text="Rows (m):").grid(row=0, column=0, sticky="w")
        self.rows_var = tk.IntVar(value=3)
        self.rows_spin = ttk.Spinbox(
            ctrl_frame, from_=1, to=200, textvariable=self.rows_var, width=6
        )
        self.rows_spin.grid(row=0, column=1, padx=(4, 12))

        ttk.Label(ctrl_frame, text="Cols (n):").grid(row=0, column=2, sticky="w")
        self.cols_var = tk.IntVar(value=3)
        self.cols_spin = ttk.Spinbox(
            ctrl_frame, from_=1, to=200, textvariable=self.cols_var, width=6
        )
        self.cols_spin.grid(row=0, column=3, padx=(4, 12))

        # buttons
        self.create_btn = ttk.Button(
            ctrl_frame, text="Create Matrices", command=self.create_matrices
        )
        self.create_btn.grid(row=0, column=4, padx=(4, 4))

        self.solve_btn = ttk.Button(ctrl_frame, text="Solve", command=self.on_solve)
        self.solve_btn.grid(row=0, column=5, padx=(8, 4))

        self.clear_btn = ttk.Button(
            ctrl_frame, text="Clear", command=self.clear_matrices
        )
        self.clear_btn.grid(row=0, column=6, padx=(4, 4))

        # tooltips
        self.info_label = ttk.Label(
            ctrl_frame, text="Enter dimensions and click Create Matrices"
        )
        self.info_label.grid(row=1, column=0, columnspan=7, pady=(8, 0), sticky="w")

        # Container that will hold both matrix areas stacked vertically
        container = ttk.Frame(root)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Matrix A area (m x n)
        self.a_label = ttk.Label(container, text="Matrix A (m x n)")
        self.a_label.pack(anchor="w")
        self.a_canvas = tk.Canvas(container, height=200)
        a_vsb = ttk.Scrollbar(container, orient="vertical", command=self.a_canvas.yview)
        a_hsb = ttk.Scrollbar(
            container, orient="horizontal", command=self.a_canvas.xview
        )
        self.a_canvas.configure(yscrollcommand=a_vsb.set, xscrollcommand=a_hsb.set)
        a_vsb.pack(side="right", fill="y")
        a_hsb.pack(side="bottom", fill="x")
        self.a_canvas.pack(fill="both", expand=False)
        self.a_frame = ttk.Frame(self.a_canvas)
        self.a_canvas.create_window((0, 0), window=self.a_frame, anchor="nw")
        self.a_frame.bind(
            "<Configure>",
            lambda e: self.a_canvas.configure(scrollregion=self.a_canvas.bbox("all")),
        )

        # Matrix B area (n x 1)
        self.b_label = ttk.Label(container, text="Matrix B (n x 1)")
        self.b_label.pack(anchor="w", pady=(8, 0))
        self.b_canvas = tk.Canvas(container, height=200)
        b_vsb = ttk.Scrollbar(container, orient="vertical", command=self.b_canvas.yview)
        b_hsb = ttk.Scrollbar(
            container, orient="horizontal", command=self.b_canvas.xview
        )
        self.b_canvas.configure(yscrollcommand=b_vsb.set, xscrollcommand=b_hsb.set)
        b_vsb.pack(side="right", fill="y")
        b_hsb.pack(side="bottom", fill="x")
        self.b_canvas.pack(fill="both", expand=False)
        self.b_frame = ttk.Frame(self.b_canvas)
        self.b_canvas.create_window((0, 0), window=self.b_frame, anchor="nw")
        self.b_frame.bind(
            "<Configure>",
            lambda e: self.b_canvas.configure(scrollregion=self.b_canvas.bbox("all")),
        )

        # Track entries for A and B
        self.entries_a = []  # 2D list
        self.entries_b = []  # 2D list (n x 1)

    def clear_matrices(self):
        # use before making a new matrix
        for row in self.entries_a:
            for w in row:
                w.destroy()
        for row in self.entries_b:
            for w in row:
                w.destroy()
        self.entries_a = []
        self.entries_b = []
        self.info_label.config(text="Matrices cleared.")

    def create_matrices(self):
        try:
            rows = int(self.rows_var.get())
            cols = int(self.cols_var.get())
            if rows <= 0 or cols <= 0:
                raise ValueError()
        except Exception:
            messagebox.showerror(
                "Invalid dimensions", "Rows and columns must be positive integers."
            )
            return

        # Save old values
        old_a = [[w.get() for w in r] for r in self.entries_a] if self.entries_a else []
        old_b = [w.get() for w in r for r in self.entries_b] if self.entries_b else []

        # Clear old widgets
        self.clear_matrices()

        # Create A (rows x cols)
        self.entries_a = []
        for r in range(rows):
            row_widgets = []
            for c in range(cols):
                e = ttk.Entry(self.a_frame, width=10)
                e.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
                if r < len(old_a) and c < (len(old_a[0]) if old_a else 0):
                    e.insert(0, old_a[r][c])
                row_widgets.append(e)
            self.entries_a.append(row_widgets)

        # Configure A columns
        for c in range(cols):
            self.a_frame.grid_columnconfigure(c, weight=1)

        # Create B (rows x 1)
        self.entries_b = []
        for r in range(rows):
            e = ttk.Entry(self.b_frame, width=12)
            e.grid(row=r, column=0, padx=2, pady=2, sticky="nsew")
            if r < len(old_b) and (len(old_b[0]) if old_b else 0) > 0:
                try:
                    val = old_b[r][0]
                except Exception:
                    val = ""
                if val:
                    e.insert(0, val)
            self.entries_b.append([e])

        self.b_frame.grid_columnconfigure(0, weight=1)

        self.info_label.config(
            text=f"Matrices created: A {rows}x{cols}, B {rows}x1. Edit any cell."
        )

        # Update scrollregions
        self.root.after(
            50, lambda: self.a_canvas.configure(scrollregion=self.a_canvas.bbox("all"))
        )
        self.root.after(
            50, lambda: self.b_canvas.configure(scrollregion=self.b_canvas.bbox("all"))
        )

    def _parse_text(self, text):
        # important since the input is always string so we convert to float. if the input isnt a number it throws an error
        t = text.strip()
        if t == "":
            return 0
        try:
            return int(t)
        except Exception:
            try:
                return float(t)
            except Exception:
                return t

    def get_matrix_from_entries(self, entries):
        # this fetches all the values
        matrix = []
        for row in entries:
            matrix_row = []
            for widget in row:
                matrix_row.append(self._parse_text(widget.get()))
            matrix.append(matrix_row)
        return matrix

    def on_solve(self):
        # this function is called when solve function is called
        if not self.entries_a or not self.entries_b:
            messagebox.showwarning("No matrices", "Create matrices A and B first.")
            return
        a = self.get_matrix_from_entries(self.entries_a)
        b = self.get_matrix_from_entries(self.entries_b)
        # Call external solver
        solve(a, b)


def main():
    root = tk.Tk()
    app = MatrixEditorApp(root)
    root.geometry("900x700")
    root.mainloop()


if __name__ == "__main__":
    main()

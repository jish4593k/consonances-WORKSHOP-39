import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to calculate Plomp & Levelt consonance
def plomp(f1, f2):
    s = 0.24 / (0.021 * min(f1, f2) + 19.)
    return np.exp(-3.5 * s * abs(f1 - f2)) - np.exp(-5.75 * s * abs(f1 - f2))

# Function to calculate consonance for an entire spectrum
def plomp_spectrum(spectrum):
    n_spectr, n_freq = spectrum.shape
    consonance = 0.0

    for i in range(n_spectr):
        for j in range(i + 1, n_spectr):
            for k in range(n_freq):
                for l in range(n_freq):
                    consonance += plomp(spectrum[i, k], spectrum[j, l])

    return consonance

# Create a simple Tkinter GUI
def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        calculate_consonance(file_path)

def calculate_consonance(file_path):
    try:
        df = pd.read_csv(file_path, header=None)
        tuning_names = df.iloc[0].values.tolist()
        tuning_data = df.iloc[1:].values.astype(float)

        consonance_table = []

        for tuning in tuning_data:
            consonance_row = []
            for index in range(12):
                major_chord = tuning[index:index+3] * (2 ** (index / 12.0))
                minor_chord = tuning[index:index+3] * (2 ** (index / 12.0))

                major_consonance = plomp_spectrum(major_chord)
                minor_consonance = plomp_spectrum(minor_chord)

                consonance_row.extend([major_consonance, minor_consonance])

            consonance_table.append(consonance_row)

        consonance_table = np.array(consonance_table)
        rel_consonance_table = consonance_table - consonance_table[0]

        create_heatmap(tuning_names, rel_consonance_table)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_heatmap(tuning_names, consonance_table):
    df = pd.DataFrame(consonance_table, columns=chordNames, index=tuning_names)

    plt.figure(figsize=(8, 6))
    sns.set(font_scale=0.7)
    sns.heatmap(df, cmap='RdYlGn_r', cbar_kws={'label': 'Relative Consonance'})
    plt.title("Relative Consonance Table")
    plt.xticks(range(len(chordNames)), chordNames, rotation='vertical')
    plt.yticks(range(len(tuning_names)), tuning_names)
    plt.tight_layout()

    root = tk.Tk()
    root.title("Consonance Table")
    root.geometry("800x600")

    canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    canvas.get_tk_widget().pack()

    root.mainloop()

chordNames = ['$C_M$', '$C\sharp_M$', '$D_M$', '$Eb_M$', '$E_M$', '$F_M$', '$F\sharp_M$', '$G_M$', '$G\sharp_M$', '$A_M$', '$Bb_M$', '$B_M$',
              '$C_m$', '$C\sharp_m$', '$D_m$', '$Eb_m$', '$E_m$', '$F_m$', '$F\sharp_m$', '$G_m$', '$G\sharp_m$', '$A_m$', '$Bb_m$', '$B_m$']

# Create a simple Tkinter GUI to open the file
root = tk.Tk()
root.title("Consonance Table Calculator")
root.geometry("300x100")

label = tk.Label(root, text="Select a tuning file:")
label.pack(pady=10)

open_button = tk.Button(root, text="Open File", command=open_file)
open_button.pack()

root.mainloop()

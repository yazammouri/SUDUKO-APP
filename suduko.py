# -*- coding: utf-8 -*-
"""
Created on Tue May 14 23:09:27 2024

@author: Zammouri
"""

# import tkinter
from customtkinter import *
import random

app = CTk()
app.geometry("500x700")
set_appearance_mode("dark")

entries = []  # Liste pour stocker les CTkEntry

def create_grid(event=None):
    global entries
    grid_frame = CTkFrame(app)
    grid_frame.pack(expand=True, fill='both', padx=100, pady=150)

    for i in range(9):
        row_entries = []
        for j in range(9):
            entry = CTkEntry(grid_frame, width=1 ,height=10, font=('Arial', 20, 'bold'), justify='center', border_width =2)
            entry.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")
            entry.grid_propagate(False)
            row_entries.append(entry)
        entries.append(row_entries)

    #Configurer les poids des lignes et colonnes pour que les entrées remplissent tout l'espace
    for i in range(9):
        grid_frame.grid_rowconfigure(i, weight=1)
        grid_frame.grid_columnconfigure(i, weight=1)

    # Afficher les valeurs de la grille
    sudoku = initialiser_sudoku()
    for i in range(9):
        for j in range(9):
            value = sudoku[i][j]
            if value != 0:
                entries[i][j].insert(0, value)

app.title("Jeu Sudoku")




# code pour la génértion des nombres dans une grille
def generate_sudoku():
    sudoku = initialiser_sudoku()
    for i in range(9):
        for j in range(9):
            entry = entries[i][j]
            if sudoku[i][j] != 0:
                entry.delete(0, 'end')
                entry.insert(0, sudoku[i][j])
            else:
                entry.delete(0, 'end')  # Vide la case pour les zéros
            
        
            

def initialiser_sudoku():
    sudoku = [[0 for _ in range(9)] for _ in range(9)]
    remplir_sudoku(sudoku)
    return sudoku

def remplir_sudoku(sudoku):
    chiffres = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(chiffres)
    for i in range(9):
        for j in range(9):
            if random.random() < 0.4:  # Ajustez ce seuil pour changer le nombre de cases remplies
                sudoku[i][j] = chiffres[(i * 3 + i // 3 + j) % 9]

#####
# from tkinter import messagebox
#####
def check_solution():
    message_label.configure(text="")
    for i in range(9):
        for j in range(9):
            entry = entries[i][j]
            value = entry.get()
            if not value.isdigit() or int(value) < 1 or int(value) > 9:
                message_label.configure(text="Veuillez remplir toutes les cases avec des chiffres de 1 à 9.")
                return
    # Vérifier les lignes
    for i in range(9):
        if len(set(entries[i][j].get() for j in range(9))) != 9:
            message_label.configure(text="La ligne {} n'est pas valide.".format(i + 1))
            return
    # Vérifier les colonnes
    for j in range(9):
        if len(set(entries[i][j].get() for i in range(9))) != 9:
            message_label.configure(text="La colonne {} n'est pas valide.".format(j + 1))
            return
    # Vérifier les régions
    for i in range(3):
        for j in range(3):
            if len(set(entries[i*3 + k][j*3 + l].get() for k in range(3) for l in range(3))) != 9:
                message_label.config(text="La région en haut à gauche n°{} n'est pas valide.".format(i*3 + j + 1))
                return
    message_label.configure(text="Bravo ! Vous avez résolu le Sudoku avec succès !")
    app.update()  # Mettre à jour l'interface pour afficher le message
    app.after(2500, lambda: message_label.config(text=""))  # Planifier la suppression du message après 2.5 secondes

    
    
    

def solve_sudoku(grid):
    empty_cell = find_empty_cell(grid)
    if not empty_cell:
        return True  # Aucune cellule vide, le sudoku est résolu
    row, col = empty_cell

    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            if solve_sudoku(grid):
                return True
            grid[row][col] = 0  # Backtrack si la solution n'est pas valide

    return False  # Aucune solution trouvée

def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None

def is_valid_move(grid, row, col, num):
    # Vérifier la ligne
    if num in grid[row]:
        return False

    # Vérifier la colonne
    if num in [grid[i][col] for i in range(9)]:
        return False

    # Vérifier le carré 3x3
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    if num in [grid[i][j] for i in range(start_row, start_row + 3) for j in range(start_col, start_col + 3)]:
        return False

    return True

def copy_grid(grid):
    return [row[:] for row in grid]

def fill_solution():
    current_grid = []
    for i in range(9):
        row = []
        for j in range(9):
            value = entries[i][j].get()
            if value:
                row.append(int(value))
            else:
                row.append(0)
        current_grid.append(row)
    if solve_sudoku(current_grid):
        for i in range(9):
            for j in range(9):
                entry = entries[i][j]
                entry.delete(0, 'end')
                entry.insert(0, current_grid[i][j])
    else:
        message_label.configure(text="Aucune solution trouvée.")






    
    


    
# Ajouter un bouton pour générer la grille Sudoku
button = CTkButton(app, text="Générer Sudoku", command=generate_sudoku)
button.place(x=107.6,y=600)  
    
    
# Ajouter un bouton pour vérifier la solution
check_button = CTkButton(app, text="Vérifier la solution", command=check_solution)
check_button.place(x=247.6, y=600)

#message de succès ou d'erreur
message_label = CTkLabel(app, text="", font=('Arial', 12), fg_color='red')
message_label.place(x=100, y=650)


# Ajouter un bouton pour remplir la grille avec une solution
solve_button = CTkButton(app, text="Résoudre la grille", command=fill_solution)
solve_button.place(x=178.7, y=50)

create_grid()

app.mainloop()


# suduko = [[0 for _ in range(9)] for _ in range(9)]
# print(suduko)
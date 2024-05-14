import tkinter as tk
import pandas as pd
import os
from datetime import datetime

# Définir la police à utiliser
FONT = ("Helvetica", 12)

# Chemin vers le fichier CSV
csv_path = 'C:/Users/Zammouri/Documents/suivi_depenses.csv'

# Vérifier si le fichier CSV existe, sinon le créer avec les noms de colonnes
if not os.path.exists(csv_path):
    with open(csv_path, 'w') as f:
        f.write('Date;Montant;Description\n')

root = tk.Tk()
root.title("Suivi de dépenses mensuelles")

# Créer le frame principal
entries_frame = tk.Frame(root)
entries_frame.pack(padx=10, pady=10)

# Créer les labels et les entrées avec la police spécifiée
date_label = tk.Label(entries_frame, text="Date :", font=FONT)
date_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

date_entry = tk.Entry(entries_frame, font=FONT)
date_entry.grid(row=0, column=1, padx=5, pady=5)

amount_label = tk.Label(entries_frame, text="Montant :", font=FONT)
amount_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

amount_entry = tk.Entry(entries_frame, font=FONT)
amount_entry.grid(row=1, column=1, padx=5, pady=5)

desc_label = tk.Label(entries_frame, text="Description :", font=FONT)
desc_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

desc_entry = tk.Entry(entries_frame, font=FONT)
desc_entry.grid(row=2, column=1, padx=5, pady=5)

total_label = tk.Label(root, text="Total dépenses du mois : 0", font=FONT)
total_label.pack(pady=10)


def save_expense():
    date = date_entry.get()
    amount = amount_entry.get()
    description = desc_entry.get()
    
    # Créer un DataFrame avec les données de la dépense
    expense_data = {'Date': [date], 'Montant': [amount], 'Description': [description]}
    df = pd.DataFrame(expense_data)
    
    # Charger le fichier CSV existant ou créer un nouveau DataFrame s'il n'existe pas encore
    try:
        existing_df = pd.read_csv(csv_path, sep=';')
    except FileNotFoundError:
        existing_df = pd.DataFrame(columns=['Date', 'Montant', 'Description'])
    
    # Vérifier si la nouvelle dépense est déjà dans le DataFrame existant
    is_duplicate = existing_df[(existing_df['Date'] == date) & 
                                (existing_df['Montant'] == amount) & 
                                (existing_df['Description'] == description)].shape[0] > 0
    
    # Ajouter la nouvelle dépense au DataFrame existant s'il n'est pas en doublon
    if not is_duplicate:
        existing_df = pd.concat([existing_df, df], ignore_index=True)
    
    # Enregistrer les dépenses dans le fichier CSV en utilisant le délimiteur ;
    existing_df.to_csv(csv_path, index=False, encoding='utf-8', sep=';')
    
    # Calculer le total des dépenses du mois en cours
    calculate_monthly_expenses()
    
    # Réinitialiser les champs de saisie
    date_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)

def calculate_monthly_expenses():
    # Charger le fichier CSV existant
    existing_df = pd.read_csv(csv_path, sep=';')

    # Convertir la colonne 'Date' en datetime avec le bon format
    existing_df['Date'] = pd.to_datetime(existing_df['Date'], format='%d/%m/%Y')

    # Filtrer les dépenses du mois en cours
    current_month = datetime.now().month
    current_year = datetime.now().year
    monthly_expenses = existing_df[(existing_df['Date'].dt.month == current_month) & 
                                    (existing_df['Date'].dt.year == current_year)]

    # Calculer le total des dépenses du mois en cours
    total_expenses = monthly_expenses['Montant'].astype(float).sum()

    # Mettre à jour le label d'affichage du total
    total_label.config(text=f"Total dépenses du mois : {total_expenses}")

# Calculer le total des dépenses au démarrage de l'application
calculate_monthly_expenses()


def show_expenses():
    # Charger le fichier CSV existant
    existing_df = pd.read_csv(csv_path, sep=';')
    
    # Créer une fenêtre pour afficher les dépenses
    expenses_window = tk.Toplevel(root)
    expenses_window.title("Liste des dépenses")
    
    # Créer un texte pour afficher les dépenses
    expenses_text = tk.Text(expenses_window, font=FONT)
    expenses_text.pack(padx=10, pady=10)
    
    # Ajouter les dépenses au texte
    for index, row in existing_df.iterrows():
        expenses_text.insert(tk.END, f"{row['Date']} - {row['Montant']} - {row['Description']}\n")
    expenses_text.config(state=tk.DISABLED)  # Empêcher l'édition du texte

# Bouton pour afficher les dépenses
show_button = tk.Button(root, text="Afficher les dépenses", command=show_expenses)
show_button.pack(pady=10)
    


save_button = tk.Button(root, text="Enregistrer dépense", command=save_expense)
save_button.pack(pady=10)



root.mainloop()

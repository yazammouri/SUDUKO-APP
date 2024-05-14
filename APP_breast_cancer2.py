# -*- coding: utf-8 -*-


#import sklearn
import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import LabelEncoder


data = load_breast_cancer()
#print(data.target)
#print("Noms des fonctionnalités :", data.feature_names)
df = pd.DataFrame(data.data, columns=data.feature_names)
#X = data.data
#y = data.target
#print(X.shape)
#print(df.shape)
target_names = data.target_names
#print(target_names)
#print(df.head(10)) 
#print(X.shape)
#print(y.shape)
df["cancer_types"]=data.target

#print(df.shape)
#print(df['cancer_types'].head(10))


labels = np.asarray(df.cancer_types)

#transformation des y:)
le = LabelEncoder()
le.fit(labels)
labels = le.transform(labels)
#print(df.head(10))


#transformation des X:)
df_selected1 = df.drop ( [ 'cancer_types' , 'radius error', 'radius error', 'texture error', 'perimeter error', 'area error', 'smoothness error', 'compactness error', 'concavity error', 'concave points error', 'symmetry error', 'fractal dimension error', 'worst radius', 'worst texture', 'worst perimeter', 'worst area', 'worst smoothness', 'worst compactness', 'worst concavity', 'worst concave points', 'worst symmetry', 'worst fractal dimension' ], axis=1)
#print(df_selected1.shape)

df_features = df_selected1.to_dict(orient='records')
from sklearn.feature_extraction import DictVectorizer
vec = DictVectorizer()
features = vec.fit_transform(df_features).toarray()
#features = vec.fit_transform(df_features).toarray(): Cette ligne prend la liste de dictionnaires df_features et la transforme en une matrice numérique en utilisant fit_transform de DictVectorizer(). Ensuite, toarray() est utilisé pour convertir la matrice sparse résultante en un tableau NumPy. 
#La matrice features peut être utilisée comme entrée pour les modèles d'apprentissage automatique.

#Ensemble d’entraînement et ensemble de test
from sklearn.model_selection import train_test_split
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.20, random_state=0)

#classification avec SVM
from sklearn.svm import SVC
#entrainement du modéle:
svm_model_linear = SVC(kernel = 'linear', C = 1).fit (features_train, labels_train)
#prédiction:
svm_predictions = svm_model_linear.predict(features_test)
accuracy = svm_model_linear.score (features_test, labels_test)
print("Précision du test avec SVM:",accuracy)


#classification avec KNN
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors = 7).fit(features_train, labels_train)
accuracy = knn.score(features_test, labels_test)
print("Précision du test avec KNN:", accuracy)






#INTERFACE TKINTER









import random
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog



def predict_tumor_class(features):
    # Utiliser le modèle SVM entraîné ("svm_model_linear") pour prédire la classe
    prediction = svm_model_linear.predict([features])
    if prediction ==0 :
        return "La tumeur est probablement bénigne."
    else:
        return "La tumeur est probablement maligne."
 
def on_click_prediction():
   # Récupérer les valeurs saisies par l'utilisateur
    new_features = []
    for entry in entries:
        new_feature = float(entry.get())
        new_features.append(new_feature)
    
    # Prédire la classe de la tumeur
    prediction = predict_tumor_class(new_features)
    
    # Afficher le résultat de la prédiction
    messagebox.showinfo("Résultat de la prédiction", prediction) 


def load_file():
    global df_loaded
    # Ouvrir une boîte de dialogue pour sélectionner un fichier
    file_path = filedialog.askopenfilename(title="Choisir un fichier CSV", filetypes=(("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")))
    
    # Charger le fichier CSV dans un DataFrame Pandas
    if file_path:
        df_loaded = pd.read_csv(file_path, usecols=range(12))
        
        # Afficher les premières lignes du DataFrame chargé
        print("Fichier chargé avec succès. Voici les premières lignes :")
        print(df_loaded.head())
        
        # Afficher le contenu dans un autre frame
        show_loaded_data()
        
    else:
        print("Aucun fichier sélectionné.")


def show_loaded_data():
    global df_loaded
    global loaded_data_frame 
    # Créer un nouveau frame pour afficher les données chargées
    loaded_data_frame = tk.Frame(root)
    loaded_data_frame.pack(expand=True, fill=tk.X)
    df_loaded = df_loaded.dropna()
    
    # Supprimer la colonne 'id'
    
    df_loaded = df_loaded.drop(columns=['id'])
    #print(df_loaded.columns)
    
    # Créer une étiquette pour afficher le contenu du DataFrame
    data_label = tk.Label(loaded_data_frame, text="5 premières lignes du fichier chargé :")
    data_label.pack()
    
    # Afficher les données du DataFrame dans un widget Text
    data_text = tk.Text(loaded_data_frame, width=100, height=19)
    data_text.pack(expand=True, fill=tk.X)
    data_text.insert(tk.END, df_loaded.to_string(index=False))
    
    button_frame = tk.Frame(root)
    button_frame.pack(anchor=tk.CENTER)
    
    # Convertir 'B' en 0 et 'M' en 1
    df_loaded['diagnosis'] = df_loaded['diagnosis'].map({'B': 0, 'M': 1})

    # Bouton "Tester le modèle SVM"
    test_model_svm_button = tk.Button(button_frame, text="Tester le modèle avec SVM", command=test_model_svm)
    test_model_svm_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Bouton "Tester le modèle KNN"
    test_model_knn_button = tk.Button(button_frame, text="Tester le modèle avec KNN", command=test_model_KNN)
    test_model_knn_button.pack(side=tk.LEFT, padx=5, pady=5)


def test_model_svm():
    global df_loaded
    global svm_model_linear

    df_loaded2=df_loaded
    if df_loaded is not None:
        
        labels = df_loaded2['diagnosis'] 
        df_loaded2 = df_loaded2.drop(columns=['diagnosis'])
        features = df_loaded2.values
        predictions = svm_model_linear.predict(features)
        accuracy = svm_model_linear.score(features, labels)
        messagebox.showinfo("Résultat du test avec SVM", f"Précision : {accuracy}")

    


def test_model_KNN():
    global df_loaded
    global knn

    df_loaded3=df_loaded
    if df_loaded is not None:
        labels = df_loaded3['diagnosis'] 
        df_loaded3 = df_loaded3.drop(columns=['diagnosis'])
        features = df_loaded3.values
        predictions = knn.predict(features)
        accuracy = knn.score(features, labels)
        messagebox.showinfo("Résultat du test avec KNN", f"Précision : {accuracy}")



def generate_random_values():
    # Générer des nombres aléatoires pour chaque champ
    random_values = [random.uniform(0, 1000) for _ in labels]
    
    # Afficher les nombres aléatoires dans les champs d'entrée correspondants
    for entry, value in zip(entries, random_values):
        entry.delete(0, tk.END)
        entry.insert(0, str(value))



# Créer une fenêtre Tkinter
root = tk.Tk()
root.title("Prédiction de classe de tumeur")


# Créer des champs de saisie pour les caractéristiques
features_frame = tk.Frame(root)
features_frame.pack()
loaded_data_frame = tk.Frame(root)
labels = df_selected1.columns
entries = []
for i, label in enumerate(labels):
    tk.Label(features_frame, text=label).grid(row=i, column=0)
    entry = tk.Entry(features_frame)
    entry.grid(row=i, column=1)
    entries.append(entry)

# Bouton "Prédire"


button_frame2 = tk.Frame(root)
button_frame2.pack(anchor=tk.CENTER)

random_button = tk.Button(button_frame2, text="Générer aléatoirement", command=generate_random_values)
random_button.pack(side=tk.LEFT, padx=5, pady=5)

predict_button = tk.Button(button_frame2, text="Prédire", command=on_click_prediction)
predict_button.pack(side=tk.LEFT, padx=5, pady=5)





# Bouton "Charger fichier"
load_file_button = tk.Button(root, text="Charger fichier", command=load_file)
load_file_button.pack()



# Lancer l'interface utilisateur
root.mainloop()    
    
import os
import tkinter as tk
from tkinter import ttk
from clips import Environment
from PIL import Image, ImageTk
import pandas as pd
import joblib
import numpy as np

# ==========================================
# Load ML model and columns
# ==========================================
try:
    # Load ML model
    clf = joblib.load("tomato_disease_model.pkl")

    # Load columns from the data file
    df = pd.read_csv("tomato_disease_symptoms_extended.csv")
    symptom_columns = df.columns[:-1].tolist()  # all columns except 'disease'

    # Get all possible disease names from the model's classes
    all_diseases = clf.classes_.tolist()

except Exception as e:
    # Fallback/error handling if the model/data is missing
    print(f"Error loading model or data: {e}")
    clf = None
    symptom_columns = []
    all_diseases = []

# ==========================================
# Initialize CLIPS environment
# ==========================================
env = Environment()
try:
    env.load("rules_model.clp")
except Exception as e:
    print(f"Error loading CLIPS rules: {e}")

# ==========================================
# Disease Info
# ==========================================
disease_info = {
    "early-blight": {"treatment": "Use copper-based fungicide. Remove affected leaves.",
                     "prevention": "Avoid overhead watering and rotate crops annually."},
    "late-blight": {"treatment": "Apply fungicides with chlorothalonil. Remove infected plants.",
                    "prevention": "Avoid wet conditions. Use resistant tomato varieties."},
    "septoria-leaf-spot": {"treatment": "Spray with copper fungicide weekly until controlled.",
                           "prevention": "Use disease-free seeds and practice crop rotation."},
    "bacterial-spot": {"treatment": "Use copper-based bactericide. Remove infected plants.",
                       "prevention": "Avoid working with wet plants and sanitize tools."},
    "tomato-mosaic-virus": {"treatment": "No chemical cure. Remove and destroy infected plants immediately.",
                            "prevention": "Sanitize tools regularly. Use virus-free seeds."},
    "leaf-mold": {"treatment": "Improve air circulation. Use approved fungicides (e.g., chlorothalonil).",
                  "prevention": "Ventilate greenhouses. Avoid high humidity."},
    "powdery-mildew": {"treatment": "Apply sulfur-based or copper-based fungicides.",
                       "prevention": "Ensure good air circulation and avoid excess nitrogen fertilization."},
    "bacterial-canker": {"treatment": "Remove and destroy infected plants. Use copper sprays for management.",
                         "prevention": "Plant certified disease-free seeds/transplants. Strict sanitation."},
    "fusarium-wilt": {"treatment": "No cure. Remove infected plants. Solarize soil.",
                      "prevention": "Use Fusarium wilt-resistant varieties (look for 'F' on labels)."},
    "verticillium-wilt": {"treatment": "No chemical cure. Remove and destroy infected plants.",
                          "prevention": "Use Verticillium wilt-resistant varieties (look for 'V' on labels)."},
    "alternaria-leaf-spot": {"treatment": "Use fungicides containing chlorothalonil.",
                             "prevention": "Practice crop rotation. Ensure adequate plant spacing."},
    "damping-off": {"treatment": "Apply a fungicide drench to the soil surface.",
                    "prevention": "Use sterile potting mix and avoid overwatering seedlings."},
    "tomato-yellow-leaf-curl-virus": {"treatment": "No cure. Remove and destroy infected plants.",
                                      "prevention": "Control whiteflies (the vector) using insecticides or netting."},
    "pith-necrosis": {"treatment": "No chemical treatment. Prune affected stems to promote recovery.",
                      "prevention": "Avoid excessive nitrogen fertilization and high humidity."},
    "root-knot-nematode": {"treatment": "Soil solarization or application of biological nematicides.",
                           "prevention": "Plant resistant varieties or practice crop rotation with non-hosts."},
    "blossom-end-rot": {"treatment": "Apply calcium foliar sprays immediately. Adjust soil pH.",
                        "prevention": "Ensure consistent watering and proper soil calcium levels."},
    "southern-blight": {"treatment": "Remove infected plants and apply fungicides to the soil.",
                        "prevention": "Deep plowing or soil solarization to reduce fungal spores."},
    "gray-leaf-spot": {"treatment": "Apply fungicides like chlorothalonil or maneb.",
                       "prevention": "Rotate crops and use drip irrigation."},
    "sunscald": {"treatment": "Protect fruit from direct, intense sun (e.g., shade cloth).",
                 "prevention": "Maintain healthy foliage to provide natural shade."},
    "tomato-rust": {"treatment": "Use copper or sulfur fungicides.",
                    "prevention": "Improve air circulation and reduce humidity."},
    "healthy": {"treatment": "Maintain regular watering and fertilization schedule.",
                "prevention": "Monitor plants weekly for early signs of disease."}
}

# ==========================================
# Translation Dictionary
# ==========================================
translations = {
    "en": {
        "title": "Hybrid Tomato Disease Diagnoser",
        "select_symptoms": "Select Symptoms Observed:",
        "diagnose_btn": "Diagnose",
        "disease": "Disease Name",
        "ml_label": "ML Confidence",
        "clips_label": "CLIPS Confidence",
        "final_trust": "Final Trust Score (FTS)",
        "treatment": "Treatment",
        "prevention": "Prevention",
        "no_match": "No matching disease found",
        "reset_btn": "Reset",
        "exit_btn": "Exit",
    },
    "es": {
        "title": "Herramienta de Diagnóstico de Enfermedades del Tomate",
        "select_symptoms": "Seleccionar Síntomas Observados:",
        "diagnose_btn": "Diagnosticar",
        "disease": "Nombre de la Enfermedad",
        "ml_label": "Confianza ML",
        "clips_label": "Confianza CLIPS",
        "final_trust": "Puntuación de Confianza Final (FTS)",
        "treatment": "Tratamiento",
        "prevention": "Prevención",
        "no_match": "No se encontró ninguna enfermedad coincidente",
        "reset_btn": "Reiniciar",
        "exit_btn": "Salir",
    }
}

current_lang = "en"


# ==========================================
# Core CLIPS Logic - Retrieves CF
# ==========================================

def get_clips_diagnosis(selected_symptoms):
    """Asserts selected symptoms into CLIPS, runs, and retrieves CF for all asserted diseases."""
    if not env:
        return {}

    env.reset()

    for symptom in selected_symptoms:
        try:
            env.assert_string(f'(symptom (name {symptom}))')
        except Exception as e:
            print(f"Error asserting symptom {symptom}: {e}")

    env.run()

    clips_results = {}

    for fact in env.facts():
        if fact.template.name == "disease":
            disease_name = fact["name"]

            try:
                # CF is 0.0 to 1.0, convert to percentage (0-100%)
                confidence_factor = float(fact["confidence"]) * 100

                # Take the MAX confidence (the strongest evidence)
                if disease_name in clips_results:
                    clips_results[disease_name] = max(clips_results[disease_name], confidence_factor)
                else:
                    clips_results[disease_name] = confidence_factor

            except Exception as e:
                print(f"Error processing CLIPS fact for {disease_name}: {e}")
                clips_results[disease_name] = 0

    return clips_results


# ==========================================
# Utility Functions
# ==========================================

def reset_selections():
    """Clears all symptom selections and the results table."""
    symptom_listbox.selection_clear(0, tk.END)
    diagnose()


def exit_app():
    """Closes the Tkinter application."""
    app.destroy()


# ==========================================
# Core Diagnosis Logic
# ==========================================

def diagnose():
    if not clf:
        print("ML Model not loaded. Cannot proceed with diagnosis.")
        return

    # 1. Get selected symptoms from the listbox
    selected_symptoms_keys = [symptom_columns[i] for i in symptom_listbox.curselection()]

    # Clear previous results
    for row in tree.get_children():
        tree.delete(row)

    # Handle the "Healthy" case when no symptoms are selected
    if not selected_symptoms_keys:
        info = disease_info.get("healthy", {"treatment": "-", "prevention": "-"})

        # Insert a single, clear row for Healthy (100% FTS)
        # Values are: FTS, ML, CLIPS, Treatment, Prevention
        tree.insert("", "end", text="Healthy",
                    values=("100.0%", "100.0%", "100.0%", info["treatment"], info["prevention"]),
                    tags=('high',))
        return  # Exit the function early

    # 2. Prepare input for ML Model
    ml_input = {col: [1 if col in selected_symptoms_keys else 0] for col in symptom_columns}
    ml_df = pd.DataFrame(ml_input, columns=symptom_columns)

    # 3. Get ML Predictions
    probabilities = clf.predict_proba(ml_df)[0]
    ml_results = {disease: prob * 100 for disease, prob in zip(clf.classes_, probabilities)}

    # 4. Get CLIPS Expert Diagnosis
    clips_results = get_clips_diagnosis(selected_symptoms_keys)

    # 5. Combine ML and CLIPS Results & Calculate Final Trust Score (FTS)
    W_ML = 0.6
    W_CF = 0.4

    combined_results = []

    all_unique_diseases = set(ml_results.keys()) | set(clips_results.keys())

    for disease in all_unique_diseases:
        if disease == "healthy":
            continue

        ml_conf = ml_results.get(disease, 0.0)
        clips_conf = clips_results.get(disease, 0.0)

        # Calculate Final Trust Score (FTS)
        fts = (ml_conf * W_ML) + (clips_conf * W_CF)

        if fts >= 0.1:
            combined_results.append({
                "disease": disease,
                "ml_conf": ml_conf,
                "clips_conf": clips_conf,
                "fts": fts
            })

    # Sort results by Final Trust Score (highest first)
    combined_results.sort(key=lambda x: x["fts"], reverse=True)

    # 6. Display Results

    if not combined_results:
        # If symptoms were selected but nothing matched significantly
        tree.insert("", "end", text=translations[current_lang]["no_match"],
                    values=("-", "-", "-", "Monitor closely.", "Re-check symptoms."), tags=('low',))
        return

    # Insert results in Treeview
    for result in combined_results:
        disease = result["disease"]
        ml_conf = result["ml_conf"]
        clips_conf = result["clips_conf"]
        fts = result["fts"]

        info = disease_info.get(disease, {"treatment": "-", "prevention": "-"})

        # Determine tag for coloring based on the Final Trust Score
        if fts >= 75:
            tag = "high"
        elif fts >= 40:
            tag = "medium"
        else:
            tag = "low"

        # Insert the row with all values (Disease Name in #0, scores/info in subsequent columns)
        # The disease name is inserted using the 'text' argument for column #0
        tree.insert("", "end", text=disease.replace('-', ' ').title(),
                    values=(f"{fts:.1f}%", f"{ml_conf:.1f}%", f"{clips_conf:.1f}%", info["treatment"],
                            info["prevention"]),
                    tags=(tag,))


def update_language():
    """Updates all GUI elements with the current language translations."""
    app.title(translations[current_lang]["title"])
    symptom_label.config(text=translations[current_lang]["select_symptoms"])
    diagnose_button.config(text=translations[current_lang]["diagnose_btn"])
    reset_button.config(text=translations[current_lang]["reset_btn"])
    exit_button.config(text=translations[current_lang]["exit_btn"])
    lang_label.config(text=translations[current_lang].get("lang_label", "Language:"))

    # --- Treeview Column Configuration ---

    # 1. Disease Name (Implicit column #0)
    tree.heading("#0", text=translations[current_lang]["disease"])
    # Set a generous width and minimum width to ensure visibility
    tree.column("#0", width=200, stretch=tk.NO, anchor="w", minwidth=150)

    # 2. Final Trust Score (FTS)
    tree.heading("fts_score", text=translations[current_lang]["final_trust"])
    tree.column("fts_score", width=120, stretch=tk.NO, anchor="center", minwidth=80)

    # 3. ML Confidence
    tree.heading("ml_confidence", text=translations[current_lang]["ml_label"])
    tree.column("ml_confidence", width=120, stretch=tk.NO, anchor="center", minwidth=80)

    # 4. CLIPS Confidence
    tree.heading("clips_confidence", text=translations[current_lang]["clips_label"])
    tree.column("clips_confidence", width=120, stretch=tk.NO, anchor="center", minwidth=80)

    # 5. Treatment (Stretching column)
    tree.heading("treatment", text=translations[current_lang]["treatment"])
    # Use stretch=tk.YES for columns that can expand
    tree.column("treatment", width=280, anchor="w", stretch=tk.YES, minwidth=150)

    # 6. Prevention (Stretching column)
    tree.heading("prevention", text=translations[current_lang]["prevention"])
    # Use stretch=tk.YES for columns that can expand
    tree.column("prevention", width=280, anchor="w", stretch=tk.YES, minwidth=150)


def switch_language(lang):
    """Switches the application language."""
    global current_lang
    current_lang = lang
    update_language()


# ==========================================
# GUI Setup (Tkinter)
# ==========================================

# Main application window
app = tk.Tk()
app.title(translations[current_lang]["title"])
app.resizable(True, True)

style = ttk.Style(app)
style.theme_use('clam')

# Configure Treeview style
style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
style.configure('Treeview', rowheight=25)

# Accent button style
style.configure('Accent.TButton', font=('Arial', 10, 'bold'), foreground='white', background='#4CAF50')
style.map('Accent.TButton', background=[('active', '#66BB6A')])

# Main frame
main_frame = ttk.Frame(app, padding="15")
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Language selection frame
lang_frame = ttk.Frame(main_frame)
lang_frame.pack(fill='x', pady=5, anchor='w')

lang_label = ttk.Label(lang_frame, text="Language:")
lang_label.pack(side=tk.LEFT, padx=(0, 10))

ttk.Button(lang_frame, text="English", command=lambda: switch_language("en")).pack(side=tk.LEFT, padx=5)
ttk.Button(lang_frame, text="Español", command=lambda: switch_language("es")).pack(side=tk.LEFT, padx=5)

# ------------------------------------------
# Symptoms Selection Section
# ------------------------------------------

symptom_label = ttk.Label(main_frame, text=translations[current_lang]["select_symptoms"], font=('Arial', 12, 'bold'))
symptom_label.pack(pady=(10, 5), anchor='w')

list_frame = ttk.Frame(main_frame)
list_frame.pack(fill="x", pady=5)

scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

symptom_listbox = tk.Listbox(
    list_frame,
    selectmode=tk.MULTIPLE,
    height=10,
    width=100,
    yscrollcommand=scrollbar.set,
    exportselection=0
)
symptom_listbox.pack(side=tk.LEFT, fill="both", expand=True)
scrollbar.config(command=symptom_listbox.yview)

if symptom_columns:
    display_symptoms = [s.replace('-', ' ').title() for s in symptom_columns]
    for symptom in display_symptoms:
        symptom_listbox.insert(tk.END, symptom)
else:
    symptom_listbox.insert(tk.END, "Error: Symptoms data not loaded.")

# --- Button Frame (Diagnose, Reset, Exit) ---
button_frame = ttk.Frame(main_frame, padding="0 0 0 15")
button_frame.pack(fill="x", pady=10)

diagnose_button = ttk.Button(button_frame, text=translations[current_lang]["diagnose_btn"], command=diagnose,
                             style='Accent.TButton')
diagnose_button.pack(side=tk.LEFT, padx=(0, 15))

reset_button = ttk.Button(button_frame, text=translations[current_lang]["reset_btn"], command=reset_selections)
reset_button.pack(side=tk.LEFT, padx=5)

exit_button = ttk.Button(button_frame, text=translations[current_lang]["exit_btn"], command=exit_app)
exit_button.pack(side=tk.RIGHT, padx=0)

# ------------------------------------------
# Results Table Section
# ------------------------------------------

result_label = ttk.Label(main_frame, text="Diagnosis Results:", font=('Arial', 12, 'bold'))
result_label.pack(pady=(10, 5), anchor='w')

result_frame = ttk.Frame(main_frame)
result_frame.pack(fill="both", expand=True)

# Define columns (The 5 named columns that follow the implicit #0 'Disease Name' column)
columns = ("fts_score", "ml_confidence", "clips_confidence", "treatment", "prevention")
# FIX: show="tree headings" ensures the #0 column (Disease Name) is actually displayed.
tree = ttk.Treeview(result_frame, columns=columns, show="tree headings", height=10)

# Column setup (Initial definition is handled in update_language for localization)

# Tags for row coloring
tree.tag_configure('high', background='#c8e6c9', foreground='#2e7d32')  # Light Green (High Confidence)
tree.tag_configure('medium', background='#fff9c4', foreground='#fbc02d')  # Light Yellow (Medium Confidence)
tree.tag_configure('low', background='#ffcdd2', foreground='#c62828')  # Light Red (Low Confidence)

tree.pack(fill="both", expand=True)

# Add a vertical scrollbar
vsb = ttk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
vsb.pack(side='right', fill='y')
tree.configure(yscrollcommand=vsb.set)

# Finalize setup
update_language()
diagnose()

app.mainloop()

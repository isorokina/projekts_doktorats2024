import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

def execute_query(query, parameters=()):
    conn = sqlite3.connect('doktorats.db')
    cursor = conn.cursor()
    cursor.execute(query, parameters)
    conn.commit()
    result = cursor.fetchall()
    conn.close()
    return result

def add_person_to_database(first_name, last_name, birth_year, personal_code, phone_number):
    query = 'INSERT INTO people (first_name, last_name, birth_year, personal_code, phone_number) VALUES (?, ?, ?, ?, ?)'
    execute_query(query, (first_name, last_name, birth_year, personal_code, phone_number))

def find_person_by_personal_code(personal_code):
    query = 'SELECT * FROM people WHERE personal_code=?'
    return execute_query(query, (personal_code,))

def register_for_class(person_id, class_type, class_day, class_time):
    query = 'INSERT INTO class_registration (person_id, class_type, class_day, class_time) VALUES (?, ?, ?, ?)'
    execute_query(query, (person_id, class_type, class_day, class_time))

def get_person_classes(person_id):
    query = 'SELECT id, class_type, class_day, class_time FROM class_registration WHERE person_id = ?'
    return execute_query(query, (person_id,))

def delete_class_registration(person_id, registration_id):
    query = 'DELETE FROM class_registration WHERE person_id = ? AND id = ?'
    execute_query(query, (person_id, registration_id))

# GUI funkcijas
def add_person_window():
    def submit():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        birth_year = birth_year_entry.get()
        personal_code = personal_code_entry.get()
        phone_number = phone_number_entry.get()
        add_person_to_database(first_name, last_name, birth_year, personal_code, phone_number)
        messagebox.showinfo("Pievienošana", "Persona pievienota datubāzei")
    
    window = tk.Toplevel()
    window.title("Pievienot cilvēku")
    
    tk.Label(window, text="Vārds").grid(row=0, column=0)
    first_name_entry = tk.Entry(window)
    first_name_entry.grid(row=0, column=1)
    
    tk.Label(window, text="Uzvārds").grid(row=1, column=0)
    last_name_entry = tk.Entry(window)
    last_name_entry.grid(row=1, column=1)
    
    tk.Label(window, text="Dzimšanas gads").grid(row=2, column=0)
    birth_year_entry = tk.Entry(window)
    birth_year_entry.grid(row=2, column=1)
    
    tk.Label(window, text="Personas kods").grid(row=3, column=0)
    personal_code_entry = tk.Entry(window)
    personal_code_entry.grid(row=3, column=1)
    
    tk.Label(window, text="Telefona numurs").grid(row=4, column=0)
    phone_number_entry = tk.Entry(window)
    phone_number_entry.grid(row=4, column=1)
    
    submit_button = tk.Button(window, text="Pievienot", command=submit)
    submit_button.grid(row=5, column=0, columnspan=2)

def find_person_window():
    def submit():
        personal_code = personal_code_entry.get()
        person = find_person_by_personal_code(personal_code)
        if person:
            person_id = person[0][0]
            info = f"Atrasta persona: {person[0][1]} {person[0][2]}, Dzimšanas gads: {person[0][3]}, Telefons: {person[0][5]}"
            person_classes = get_person_classes(person_id)
            classes_info = "\n".join([f"Tips: {cls[1]}, Diena: {cls[2]}, Laiks: {cls[3]}" for cls in person_classes])
            result_text.set(info + "\n" + "Nodarbības:\n" + classes_info)
        else:
            result_text.set("Persona ar norādīto personas kodu netika atrasta")
    
    window = tk.Toplevel()
    window.title("Atrast cilvēku")
    
    tk.Label(window, text="Personas kods").grid(row=0, column=0)
    personal_code_entry = tk.Entry(window)
    personal_code_entry.grid(row=0, column=1)
    
    submit_button = tk.Button(window, text="Meklēt", command=submit)
    submit_button.grid(row=1, column=0, columnspan=2)
    
    result_text = tk.StringVar()
    result_label = tk.Label(window, textvariable=result_text)
    result_label.grid(row=2, column=0, columnspan=2)

def register_for_class_window():
    def submit():
        personal_code = personal_code_entry.get()
        person = find_person_by_personal_code(personal_code)
        if person:
            person_id = person[0][0]
            class_type = class_type_combo.get()
            class_day = class_day_combo.get()
            class_time = class_time_combo.get()
            register_for_class(person_id, class_type, class_day, class_time)
            messagebox.showinfo("Pieraksts", f"Cilvēks pierakstīts uz nodarbību: {class_type} {class_day} {class_time}")
        else:
            messagebox.showerror("Kļūda", "Persona ar norādīto personas kodu netika atrasta")
    
    window = tk.Toplevel()
    window.title("Pieraksts uz nodarbību")
    
    tk.Label(window, text="Personas kods").grid(row=0, column=0)
    personal_code_entry = tk.Entry(window)
    personal_code_entry.grid(row=0, column=1)
    
    tk.Label(window, text="Nodarbības tips").grid(row=1, column=0)
    class_type_combo = ttk.Combobox(window, values=["Konsultācija", "Slimība"])
    class_type_combo.grid(row=1, column=1)
    
    tk.Label(window, text="Diena").grid(row=2, column=0)
    class_day_combo = ttk.Combobox(window, values=["Pirmdiena", "Otrdiena", "Trešdiena", "Ceturdiena", "Piektdiena"])
    class_day_combo.grid(row=2, column=1)
    
    tk.Label(window, text="Laiks").grid(row=3, column=0)
    class_time_combo = ttk.Combobox(window, values=["09:00-09:30", "9:30-10:00"])
    class_time_combo.grid(row=3, column=1)
    
    submit_button = tk.Button(window, text="Pievienoties", command=submit)
    submit_button.grid(row=4, column=0, columnspan=2)

# Galvenais logs
root = tk.Tk()
root.title("Datubāzes vadība")

tk.Label(root, text="Izvēlēties darbību:").grid(row=0, column=0, columnspan=2)

add_person_button = tk.Button(root, text="Pievienot cilvēku", command=add_person_window)
add_person_button.grid(row=1, column=0, padx=10, pady=10)

find_person_button = tk.Button(root, text="Atrast cilvēku", command=find_person_window)
find_person_button.grid(row=1, column=1, padx=10, pady=10)

register_button = tk.Button(root, text="Pieraksts uz nodarbību", command=register_for_class_window)
register_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

exit_button = tk.Button(root, text="Iziet", command=root.quit)
exit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
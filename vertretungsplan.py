import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import random
import pygame
import threading

# Füge diese Funktion zum Laden des Verzeichnisses mit Abkürzungen hinzu
def lade_lehrer_verzeichnis(dateipfad):
    lehrer_verzeichnis = {}

    try:
        with open(dateipfad, 'r', encoding='utf-8') as datei:
            for zeile in datei:
                abkuerzung, name = zeile.strip().split('=')
                lehrer_verzeichnis[abkuerzung.strip()] = name.strip()

    except FileNotFoundError:
        messagebox.showerror("Fehler", "Lehrerverzeichnis nicht gefunden.")
        exit()

    return lehrer_verzeichnis

# Ersetze diese Variable mit dem tatsächlichen Dateipfad zu deiner Textdatei mit den Lehrerabkürzungen
lehrer_verzeichnis_dateipfad = "C:/vertretungsplan_cgj/lehrer_verzeichnis.txt"
lehrer_verzeichnis = lade_lehrer_verzeichnis(lehrer_verzeichnis_dateipfad)

# Füge diese Funktion zum Ersetzen der Abkürzungen durch Namen hinzu
def ersetze_lehrer_abkuerzungen(text):
    for abkuerzung, name in lehrer_verzeichnis.items():
        text = text.replace(abkuerzung, name)
    return text

# URL des Vertretungsplans
url = "https://c-g-j.de/index.php?id=29"

# Herunterladen der Webseite
response = requests.get(url)
html_content = response.content

# Extrahieren der Tabelle mit dem Vertretungsplan
soup = BeautifulSoup(html_content, "html.parser")
table = soup.find("table", class_="table")

# Überprüfen, ob die Tabelle vorhanden ist
if table is None:
    messagebox.showerror("Fehler", "Tabelle nicht gefunden.")
    exit()

# Extrahieren der Tabellenzeilen
rows = table.find_all("tr")

# Erstellen einer Liste aller vorhandenen Klassen
klassen_liste = []
for row in rows:
    columns = row.find_all("td")

    # Überspringen von Leerzeilen und Überschriften
    if not columns or columns[0].text.strip() == "":
        continue

    klasse = columns[0].text.strip()
    klassen_liste.append(klasse)


def zeige_vertretungen():
    gewuenschte_klasse = eingabe_klasse.get().strip()

    # Überprüfen, ob die gewünschte Klasse vorhanden ist
    if gewuenschte_klasse.lower() == "/alle/":
        gewuenschte_klassen = klassen_liste
    else:
        gewuenschte_klassen = [gewuenschte_klasse]

    # Anzeigen der Vertretungsinformationen
    gefundene_klassen = []
    vertretungen_text.config(state=tk.NORMAL)
    vertretungen_text.delete("1.0", tk.END)

    for row in rows:
        columns = row.find_all("td")

        # Überspringen von Leerzeilen und Überschriften
        if not columns or columns[0].text.strip() == "":
            continue

        klasse = columns[0].text.strip()

        if klasse.lower() in gewuenschte_klassen or any(klasse.lower().startswith(k.lower()) for k in gewuenschte_klassen):
            gefunden = False
            for i, column in enumerate(columns[1:]):
                stunde = i + 1
                vertretung = column.text.strip().replace("\n", " ")

                # Ersetze Abkürzungen durch Namen
                vertretung = ersetze_lehrer_abkuerzungen(vertretung)

                if vertretung != "":
                    vertretungen_text.insert(tk.END, f"Klasse: {klasse}\n")
                    vertretungen_text.insert(tk.END, f"Stunde: {stunde}\n")
                    vertretungen_text.insert(tk.END, f"Vertretung: {vertretung}\n")
                    vertretungen_text.insert(tk.END, "-------------------\n")
                    gefunden = True

            if gefunden:
                gefundene_klassen.append(klasse)

    # Überprüfen, ob die Klasse "5 - 12" vorhanden ist und anzeigen
    if "5 - 12" in klassen_liste:
        vertretungen_text.insert(tk.END, "Klasse: 5 - 12\n")
        for i, column in enumerate(rows[1].find_all("td")[1:]):
            stunde = i + 1
            vertretung = column.text.strip().replace("\n", " ")

            # Ersetze Abkürzungen durch Namen
            vertretung = ersetze_lehrer_abkuerzungen(vertretung)

            if vertretung != "":
                vertretungen_text.insert(tk.END, f"Stunde: {stunde}\n")
                vertretungen_text.insert(tk.END, f"Vertretung: {vertretung}\n")
                vertretungen_text.insert(tk.END, "-------------------\n")

        gefundene_klassen.append("5 - 12")

    # Überprüfen, ob die gewünschte Klasse gefunden wurde
    if gewuenschte_klasse.lower() != "/alle/" and gewuenschte_klasse.lower() not in [k.lower() for k in gefundene_klassen]:
        aehnliche_klassen = [k for k in klassen_liste if k.startswith(gewuenschte_klasse[:-1]) and k != gewuenschte_klasse]
        if aehnliche_klassen:
            messagebox.showwarning("Hinweis", f"Die Klasse {gewuenschte_klasse} wurde nicht gefunden oder hat keine Vertretungen/Ausfall. "
                                               f"Ähnliche Klassen gefunden: {', '.join(aehnliche_klassen)}")
        else:
            messagebox.showwarning("Hinweis", f"Keine Vertretungsinformationen gefunden für Klasse {gewuenschte_klasse}.")

    vertretungen_text.config(state=tk.DISABLED)


def start_party_mode():
    # Musik abspielen (Sie müssen den Dateipfad zur Party-Musik angeben)
    party_musik = "C:/vertretungsplan_cgj/party_music.mp3"
    pygame.mixer.init()
    pygame.mixer.music.load(party_musik)
    pygame.mixer.music.play()

    # Hintergrund ändern (Sie müssen den Dateipfad zum Party-Hintergrundbild angeben)
    party_hintergrund = "C:/vertretungsplan_cgj/party_background.png"
    background_image = tk.PhotoImage(file=party_hintergrund)
    background_label.configure(image=background_image)
    background_label.image = background_image

    # Alles herumfahren lassen
    def move_widgets():
        while party_mode_active:
            for widget in window.winfo_children():
                if widget != button_anzeigen:
                    x = random.randint(00, 800)
                    y = random.randint(00, 500)
                    widget.place(x=x, y=y)
            window.update()
            threading.Event().wait(1)

    # Text anzeigen
    vertretungen_text.config(state=tk.NORMAL)
    vertretungen_text.delete("1.0", tk.END)
    vertretungen_text.insert(tk.END, "PARTY MODUS AKTIVIERT!\n")
    vertretungen_text.insert(tk.END, "Es ist Zeit zum Feiern!\n")
    vertretungen_text.insert(tk.END, "Lass uns tanzen und Spaß haben!\n")
    vertretungen_text.config(state=tk.DISABLED)

    # Starten des Threads für die Bewegung der Widgets
    party_mode_active = True
    move_thread = threading.Thread(target=move_widgets)
    move_thread.start()


# Erstellen des GUI-Fensters
window = tk.Tk()
window.title("Vertretungsplan")

# Automatisches Maximieren des Fensters
window.state("zoomed")

# Hintergrundbild
background_image = tk.PhotoImage(file="C:/vertretungsplan_cgj/background.png")
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Logo
logo_image = tk.PhotoImage(file="C:/vertretungsplan_cgj/logo.png")
logo_label = tk.Label(window, image=logo_image)
logo_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

# Eingabefeld für die Klasse
eingabe_klasse = tk.Entry(window, font=("Arial", 16))
eingabe_klasse.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

# Button zum Anzeigen der Vertretungen
button_anzeigen = tk.Button(window, text="Vertretungen anzeigen", font=("Arial", 16), command=zeige_vertretungen)
button_anzeigen.place(relx=0.5, rely=0.26, anchor=tk.CENTER)

# Textfeld für die Vertretungen
vertretungen_text = scrolledtext.ScrolledText(window, font=("Arial", 14), state=tk.DISABLED)
vertretungen_text.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.8, relheight=0.4)

# Starten des Party-Modus oder Anzeigen der Vertretungen, wenn "party" eingegeben wird
def check_party_mode(event):
    klasse = eingabe_klasse.get().strip().lower()
    if klasse == "party":
        start_party_mode()
    else:
        zeige_vertretungen()

eingabe_klasse.bind("<Return>", check_party_mode)

# Schließen des Fensters
def close_window():
    if messagebox.askokcancel("Beenden", "Möchten Sie das Programm wirklich beenden?"):
        window.destroy()

window.protocol("WM_DELETE_WINDOW", close_window)

# Anzeigen des Fensters
window.mainloop()

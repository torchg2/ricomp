# -*- coding: utf-8 -*-
"""Piatti tipici, sedute, target di partenza, versione della build.

VERSIONE: alza il numero a ogni modifica. Finisce nel nome della cache del
service worker, in fondo alla scheda Misure e nella card "Novità".
"""

VERSIONE = 3
DATA_BUILD = "18/09/2026"

NOME = "Ricomp"
NOME_LUNGO = "Ricomp - segui popetto"

# Cosa dice la card "Novità" alla prima apertura dopo l'aggiornamento.
NOVITA = [
    "Scheda Piano: le 80 opzioni del piano denso, con etichetta e peso del piatto. Si registrano da lì.",
    "Anche: il voto si dà tutti i giorni, non solo dopo la seduta.",
    "Allenamento: riscaldamento, recuperi con timer che vibra, scheda di ogni esercizio al tocco.",
    "Protocollo dei 14 giorni e domanda dei 21 giorni in Misure e Oggi. Propongono, non applicano.",
    "Interruttore Settimana storta in cima a Oggi.",
    "Target nuovi: 2.050 e 1.900, proteine 135, fibra 22. Modificabili in Misure.",
    "462 alimenti, con sushi a pezzi e verdure cotte.",
]

# --- Profilo e target di partenza ---------------------------------------
# Valori iniziali: nell'app si cambiano da Misure > Impostazioni e restano
# sul telefono. Rigenerare l'app non li sovrascrive.

PROFILO = {"eta": 35, "altezza": 181, "peso": 71.0}

TARGET = {
    "allen":  {"kcal": 2050, "p": 135, "f": 70, "c": 220, "fib": 22},
    "riposo": {"kcal": 1900, "p": 135, "f": 65, "c": 190, "fib": 22},
    # settimana storta: mantenimento, nessun deficit. Il PDF scriveva
    # 1.950-2.000 chiamandolo mantenimento, ma è sotto il target normale:
    # qui si usa il dispendio sedentario stimato dallo stesso PDF.
    "storta": {"kcal": 2150, "p": 135, "f": 70, "c": 245, "fib": 22},
}

# Pulsante "Calcola dai dati": Mifflin-St Jeor x fattore, poi il deficit
# minimo del piano. Con 71 kg da 2.050 / 1.900.
FATTORE_ATTIVITA = 1.375     # "leggermente attiva", come nel PDF
DEFICIT = 250                # sotto il dispendio, giorno di allenamento
DELTA_RIPOSO = 150           # quanto scende il giorno di riposo
KCAL_MINIME = 1750           # sotto non si va, qualunque cosa dica la bilancia

# Protocollo dei 14 giorni
GIORNI_CREATINA = 21         # niente aggiustamenti prima
PASSO_MAX = 150              # mai più di così alla volta

# --- Piatti tipici: stime per porzione -----------------------------------
# n, kcal, proteine, grassi, carboidrati, fibra

PIATTI = [
    ("Pizza margherita (intera)", 850, 35, 28, 110, 6.0),
    ("Pizza con affettato e rucola", 1000, 45, 38, 115, 7.0),
    ("Pizza diavola", 1050, 42, 42, 112, 6.0),
    ("Pizza salsiccia e friarielli", 1100, 45, 48, 108, 8.0),
    ("Pizza quattro formaggi", 1100, 48, 50, 105, 5.0),
    ("Pizza capricciosa", 1050, 45, 42, 112, 6.0),
    ("Calzone", 900, 38, 38, 95, 5.0),
    ("Hamburger con patatine", 950, 40, 48, 85, 6.0),
    ("Hamburger semplice", 550, 30, 26, 45, 3.0),
    ("Cotoletta alla bolognese", 740, 45, 45, 30, 1.0),
    ("Cotoletta impanata", 600, 40, 35, 25, 1.0),
    ("Lasagne, porzione", 600, 28, 30, 52, 3.0),
    ("Tortellini in brodo, porzione", 360, 20, 12, 40, 2.0),
    ("Tagliatelle al ragu, porzione", 650, 24, 26, 78, 4.0),
    ("Pasta al pomodoro, porzione", 480, 15, 12, 76, 4.0),
    ("Pasta al pesto, porzione", 620, 18, 28, 70, 4.0),
    ("Pasta alla carbonara, porzione", 700, 25, 32, 72, 3.0),
    ("Pasta all'amatriciana, porzione", 620, 20, 26, 74, 4.0),
    ("Cacio e pepe, porzione", 600, 22, 24, 72, 3.0),
    ("Pasta al ragu bianco, porzione", 640, 26, 26, 74, 4.0),
    ("Risotto, porzione", 520, 12, 18, 76, 2.0),
    ("Parmigiana di melanzane", 480, 18, 34, 22, 5.0),
    ("Poke bowl", 700, 35, 24, 82, 5.0),
    ("Insalatona con pollo", 600, 40, 30, 35, 5.0),
    ("Panino con prosciutto", 450, 22, 16, 52, 3.0),
    ("Piadina con crudo e squacquerone", 600, 25, 28, 58, 2.0),
    ("Tramezzino", 300, 12, 15, 28, 1.5),
    ("Kebab", 750, 40, 35, 65, 5.0),
    ("Sushi, 12 pezzi", 550, 25, 12, 85, 2.0),
    ("Pollo arrosto, porzione", 420, 45, 24, 2, 0.0),
    ("Pollo alla cacciatora, porzione", 450, 40, 26, 10, 2.0),
    ("Pesce alla griglia, porzione", 380, 42, 18, 8, 0.0),
    ("Filetto di maiale con contorno", 500, 42, 26, 20, 3.0),
    ("Frittata di 3 uova", 330, 22, 25, 2, 0.0),
    ("Polpette al sugo, porzione", 480, 32, 28, 22, 3.0),
    ("Antipasto affettati e formaggi", 550, 28, 42, 12, 1.0),
    ("Bruschette, 2 pezzi", 240, 6, 10, 30, 2.5),
    ("Gnocco fritto, 3 pezzi", 380, 8, 22, 38, 1.5),
    ("Focaccia, porzione", 400, 8, 18, 50, 2.5),
    ("Arancino", 400, 12, 16, 52, 2.5),
    ("Suppli", 250, 8, 11, 30, 1.5),
    ("Patatine fritte, porzione", 400, 5, 20, 48, 4.0),
    ("Patate al forno, porzione", 260, 5, 9, 40, 3.5),
    ("Friggione bolognese, porzione", 180, 3, 12, 14, 3.0),
    ("Verdure grigliate, porzione", 120, 3, 8, 8, 4.0),
    ("Insalata mista con olio", 90, 2, 7, 4, 2.0),
    ("Gelato, 2 palline", 250, 4, 12, 30, 0.5),
    ("Tiramisu, porzione", 400, 7, 24, 38, 1.0),
    ("Cornetto", 280, 5, 13, 35, 1.5),
    ("Barretta di cioccolato", 250, 3, 13, 30, 1.5),
    ("Cappuccino", 110, 6, 5, 10, 0.0),
    ("Caffè", 2, 0, 0, 0, 0.0),
    ("Birra media, 0,5 L", 200, 2, 0, 16, 0.0),
    ("Birra piccola, 0,33 L", 130, 1, 0, 11, 0.0),
    ("Calice di vino", 120, 0, 0, 4, 0.0),
    ("Distillato liscio", 70, 0, 0, 0, 0.0),
    ("Cocktail", 350, 0, 0, 30, 0.0),
]

# --- Riscaldamento -------------------------------------------------------
RISCALDAMENTO = {
    "alta": ["Circonduzioni delle spalle, 10 per verso",
             "Pull-apart con elastico leggero, 20",
             "Flesso-estensioni e circonduzioni del polso, 15 per verso (per il gomito)",
             "Sospensione attiva alla sbarra, 3 x 10 secondi"],
    "bassa": ["Ponte glutei a corpo libero, 15 lente",
              "Conchiglia senza elastico, 15 per lato",
              "Abduzione da sdraiato di fianco senza elastico, 15 per lato",
              "Marcia sul posto con ginocchia basse, 30 secondi"],
}
NOTA_MATTINO = ("Entro un'ora dal risveglio: 8 minuti invece di 5, e la prima serie di ogni "
                "esercizio al 70%, come prova. Stacco rumeno con il range più corto della giornata.")

# --- Le quattro sedute ---------------------------------------------------
# ex: (nome, serie x ripetizioni, recupero in secondi)
# "corta" è la versione da 15 minuti: i primi tre esercizi.

SEDUTE = {
    "A": {
        "nome": "Parte alta, trazione", "zona": "alta",
        "ex": [("Trazioni alla sbarra", "4 x 5", 120),
               ("Rematore da seduto con l'elastico", "3 x 12-15", 60),
               ("Face pull con l'elastico", "3 x 15", 45),
               ("Curl a martello con i manubri", "2 x 15-20", 45),
               ("Plank sulle mani", "3 x 30-45 s", 45),
               ("Pallof press con l'elastico", "3 x 10 per lato", 45)],
        "corta": ["Trazioni alla sbarra", "Rematore da seduto con l'elastico",
                  "Face pull con l'elastico"],
    },
    "B": {
        "nome": "Parte bassa hip-safe e core", "zona": "bassa",
        "ex": [("Ponte glutei a terra", "4 x 15", 60),
               ("Ponte glutei a una gamba", "3 x 10 per lato", 60),
               ("Abduzione in piedi con l'elastico", "3 x 15 per lato", 45),
               ("Conchiglia (clamshell) con l'elastico", "3 x 15 per lato", 45),
               ("Stacco rumeno con i manubri", "3 x 12-15", 60),
               ("Affondo indietro a range ridotto", "2 x 8 per lato", 60),
               ("Dead bug", "3 x 8 per lato", 45),
               ("Plank laterale sulle ginocchia", "2 x 20-30 s per lato", 45)],
        "corta": ["Ponte glutei a terra", "Abduzione in piedi con l'elastico",
                  "Dead bug"],
    },
    "C": {
        "nome": "Parte alta, spinta", "zona": "alta",
        "ex": [("Piegamenti sulle braccia", "4 x 8-12", 90),
               ("Lento avanti con l'elastico", "3 x 15", 60),
               ("Trazioni alla sbarra", "3 x 4-5", 120),
               ("Rematore in piedi con l'elastico", "3 x 15", 45),
               ("Alzate laterali con i manubri", "3 x 15-20", 45),
               ("Plank con tocco spalla", "3 x 8 per lato", 45)],
        "corta": ["Piegamenti sulle braccia", "Lento avanti con l'elastico",
                  "Rematore in piedi con l'elastico"],
    },
    "D": {
        "nome": "Circuito total body", "zona": "bassa",
        "nota": "4 giri. 40 secondi di lavoro e 20 di pausa per stazione, 1 minuto tra i giri.",
        "ex": [("Piegamenti sulle braccia", "4 giri x 40 s", 20),
               ("Rematore da seduto con l'elastico", "4 giri x 40 s", 20),
               ("Ponte glutei a terra", "4 giri x 40 s", 20),
               ("Abduzione in piedi con l'elastico", "4 giri x 40 s", 20),
               ("Plank sulle mani", "4 giri x 40 s", 20),
               ("Corda per saltare", "4 giri x 40 s", 60)],
        "corta": ["Piegamenti sulle braccia", "Rematore da seduto con l'elastico",
                  "Ponte glutei a terra"],
    },
}

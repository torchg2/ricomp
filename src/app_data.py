# -*- coding: utf-8 -*-
"""Piatti tipici, sedute, target di partenza, versione della build.

VERSIONE: alza il numero a ogni modifica (3.2, 3.3, ... 3.9, poi 4: mai 3.10, che vale
3.1). Finisce nel nome della cache del
service worker, in fondo alla scheda Misure e nella card "Novità".
"""

VERSIONE = 3.2
DATA_BUILD = "21/09/2026"

NOME = "Ricomp"
NOME_LUNGO = "Ricomp - segui popetto"

# Cosa dice la card "Novità" alla prima apertura dopo l'aggiornamento.
NOVITA = [
    "Grafica nuova: caratteri, colori e card ridisegnati. Anelli per calorie e proteine, barre con la tacca del target, pasti in ambra quando sfori.",
    "Allenamento, Riposo, Storta: un unico selettore in cima a Oggi. La storta resta attiva finché scegli un'altra opzione.",
    "Modalità seduta: premi Inizia la seduta. Recuperi automatici, esercizi a tempo e circuito D senza toccare il telefono.",
    "Scheda esercizio: Attenzione in cima, disegno più grande, e tre sezioni nuove: errori comuni, perché lo fai, se fa male.",
    "Suggerimento dei carichi: dopo due sedute sopra il previsto propone il passo successivo. Si blocca se l'anca il giorno dopo era a 2 o più.",
    "Ristorante: nella ricerca, scegli il locale e componi il pasto con + e -.",
    "Tieni premuta l'icona: Peso, Pasto e Allenamento. Può servire un giorno perché Android le mostri.",
    "Più di 30 alimenti e 50 piatti nuovi: Campari, pizze, hamburger da 100 e 200 g, bar, aperitivo, trattoria, cucina di casa. Gin tonic, Aperol spritz e Moscow mule corretti: contavano il doppio.",
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
    ("Tagliatelle al ragù, porzione", 650, 24, 26, 78, 4.0),
    ("Pasta al pomodoro, porzione", 480, 15, 12, 76, 4.0),
    ("Pasta al pesto, porzione", 620, 18, 28, 70, 4.0),
    ("Pasta alla carbonara, porzione", 700, 25, 32, 72, 3.0),
    ("Pasta all'amatriciana, porzione", 620, 20, 26, 74, 4.0),
    ("Cacio e pepe, porzione", 600, 22, 24, 72, 3.0),
    ("Pasta al ragù bianco, porzione", 640, 26, 26, 74, 4.0),
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
    ("Supplì", 250, 8, 11, 30, 1.5),
    ("Patatine fritte, porzione", 400, 5, 20, 48, 4.0),
    ("Patate al forno, porzione", 260, 5, 9, 40, 3.5),
    ("Friggione bolognese, porzione", 180, 3, 12, 14, 3.0),
    ("Verdure grigliate, porzione", 120, 3, 8, 8, 4.0),
    ("Insalata mista con olio", 90, 2, 7, 4, 2.0),
    ("Gelato, 2 palline", 250, 4, 12, 30, 0.5),
    ("Tiramisù, porzione", 400, 7, 24, 38, 1.0),
    ("Cornetto", 280, 5, 13, 35, 1.5),
    ("Barretta di cioccolato", 250, 3, 13, 30, 1.5),
    ("Cappuccino", 110, 6, 5, 10, 0.0),
    ("Caffè", 2, 0, 0, 0, 0.0),
    ("Birra media, 0,5 L", 200, 2, 0, 16, 0.0),
    ("Birra piccola, 0,33 L", 130, 1, 0, 11, 0.0),
    ("Calice di vino", 120, 0, 0, 4, 0.0),
    ("Distillato liscio", 70, 0, 0, 0, 0.0),
    ("Cocktail", 350, 0, 0, 30, 0.0),
    # --- pizzeria (pizza intera da ristorante, circa 300-350 g) ---
    ("Pizza marinara", 700, 20, 18, 112, 6.0),
    ("Pizza bufala", 950, 42, 36, 110, 5.0),
    ("Pizza prosciutto cotto", 950, 45, 34, 110, 5.0),
    ("Pizza prosciutto e funghi", 950, 45, 34, 111, 6.0),
    ("Pizza tonno e cipolla", 950, 48, 34, 112, 6.0),
    ("Pizza vegetariana", 850, 32, 30, 115, 9.0),
    ("Pizza napoli", 850, 40, 28, 110, 6.0),
    ("Pizza crudo e rucola", 1000, 50, 36, 110, 6.0),
    ("Pizza wurstel e patatine", 1150, 38, 50, 135, 7.0),
    ("Pizza mortadella e pistacchi", 1150, 45, 55, 115, 5.0),
    ("Pizza integrale margherita", 800, 34, 26, 105, 12.0),
    ("Pizza al trancio, 1 trancio", 300, 12, 10, 40, 2.0),
    ("Pinsa margherita", 700, 28, 22, 98, 5.0),
    ("Focaccia farcita crudo e mozzarella", 700, 30, 30, 75, 3.0),
    # --- hamburger da ristorante: panino, carne, verdure, salsa. Patatine a parte ---
    ("Burger classico, 100 g di manzo", 530, 26, 26, 47, 3.0),
    ("Burger classico, 200 g di manzo", 780, 43, 45, 47, 3.0),
    ("Cheeseburger, 100 g di manzo", 610, 31, 32, 48, 3.0),
    ("Cheeseburger, 200 g di manzo", 860, 48, 52, 48, 3.0),
    ("Burger bacon e cheddar, 100 g di manzo", 710, 38, 40, 48, 3.0),
    ("Burger bacon e cheddar, 200 g di manzo", 960, 55, 60, 48, 3.0),
    ("Burger con cipolla caramellata, 100 g di manzo", 600, 27, 27, 60, 4.0),
    ("Burger con cipolla caramellata, 200 g di manzo", 850, 44, 46, 60, 4.0),
    ("Burger con salse gourmet, 100 g di manzo", 760, 32, 47, 50, 3.0),
    ("Burger con salse gourmet, 200 g di manzo", 1010, 49, 67, 50, 3.0),
    ("Anelli di cipolla, porzione", 400, 5, 22, 44, 3.0),
    ("Nuggets di pollo, 6 pezzi", 290, 15, 18, 17, 1.0),
    # --- panini, piadine, kebab, poke ---
    ("Piadina cotto e fontina", 650, 28, 32, 58, 3.0),
    ("Piadina verdure grigliate e stracchino", 560, 20, 26, 60, 5.0),
    ("Panino bresaola, rucola e grana", 450, 32, 12, 52, 3.0),
    ("Panino con cotoletta", 750, 32, 32, 80, 4.0),
    ("Panino con porchetta", 650, 30, 30, 60, 3.0),
    ("Piadina kebab", 700, 32, 32, 70, 4.0),
    ("Kebab al piatto con patatine", 950, 45, 50, 80, 5.0),
    ("Poke bowl al tonno", 560, 35, 18, 65, 6.0),
    ("Poke bowl al pollo", 600, 40, 20, 65, 6.0),
    # --- trattoria ---
    ("Tagliata di manzo con rucola e grana", 520, 55, 32, 2, 1.0),
    ("Grigliata mista di carne", 750, 65, 52, 0, 0.0),
    ("Passatelli in brodo, porzione", 420, 20, 15, 50, 2.0),
    ("Tortelloni burro e salvia, porzione", 600, 20, 28, 65, 3.0),
    ("Gramigna con salsiccia, porzione", 650, 25, 28, 75, 4.0),
    ("Pasta alle vongole, porzione", 550, 26, 14, 78, 3.0),
    ("Vitello tonnato, porzione", 420, 38, 28, 3, 0.0),
    # --- cucina di casa ---
    ("Pasta e fagioli, porzione", 450, 18, 10, 70, 11.0),
    ("Minestrone con pasta, porzione", 300, 10, 7, 48, 8.0),
    ("Pasta al tonno, porzione", 580, 28, 16, 80, 5.0),
    ("Pasta con zucchine, porzione", 520, 16, 16, 78, 5.0),
    ("Riso e piselli, porzione", 450, 15, 10, 75, 7.0),
    ("Insalata di riso, porzione", 520, 18, 20, 68, 3.0),
    ("Spezzatino di manzo con patate, porzione", 520, 38, 22, 38, 4.0),
    ("Orata al forno con patate, porzione", 480, 38, 20, 35, 3.0),
    ("Pollo al curry con riso, porzione", 650, 42, 18, 78, 3.0),
    ("Petto di pollo alla piastra con verdure", 350, 45, 12, 10, 5.0),
    ("Zuppa di legumi, porzione", 350, 18, 8, 50, 13.0),
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

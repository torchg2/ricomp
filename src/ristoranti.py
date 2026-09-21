# -*- coding: utf-8 -*-
"""Stime da ristorante: per ogni tipo di locale, le cose che ci trovi di solito.

Nell'app scegli il locale e componi il pasto con i contatori - e +.
Ogni voce è il nome esatto di un alimento (foods.py) o di un piatto
(PIATTI in app_data.py):
  "Nome"            alimento che si conta a pezzi, oppure piatto a porzione
  ("Nome", grammi)  alimento a peso: ogni + aggiunge quei grammi
La build si ferma se un nome non esiste.

CONDIMENTO: l'interruttore "condimento da ristorante" aggiunge questa quota
alle calorie dei piatti (non a bevande e alimenti singoli), come grasso.
"""

CONDIMENTO = 0.15

LOCALI = [
    ("Pizzeria", [
        "Pizza margherita (intera)", "Pizza marinara", "Pizza bufala", "Pizza diavola",
        "Pizza capricciosa", "Pizza quattro formaggi", "Pizza prosciutto cotto",
        "Pizza prosciutto e funghi", "Pizza tonno e cipolla", "Pizza vegetariana",
        "Pizza napoli", "Pizza crudo e rucola", "Pizza con affettato e rucola",
        "Pizza salsiccia e friarielli", "Pizza wurstel e patatine",
        "Pizza mortadella e pistacchi", "Pizza integrale margherita", "Pinsa margherita",
        "Calzone", "Pizza al trancio, 1 trancio", "Focaccia farcita crudo e mozzarella",
        "Bruschette, 2 pezzi", "Supplì", "Arancino", "Patatine fritte, porzione",
        "Birra chiara", "Cola", "Cola zero", "Vino rosso", "Tiramisù, porzione",
        "Gelato, 2 palline",
    ]),
    ("Sushi", [
        "Nigiri salmone", "Nigiri tonno", "Nigiri branzino", "Nigiri gambero",
        "Sashimi salmone", "Sashimi tonno", "Sashimi branzino",
        "Uramaki California", "Uramaki Philadelphia", "Uramaki tempura gambero",
        "Uramaki tonno e avocado", "Uramaki salmone e avocado",
        "Hosomaki (salmone, tonno o cetriolo)", "Temaki salmone", "Gyoza",
        "Tempura di gamberi", ("Edamame", 80), "Insalata di alghe wakame",
        "Zuppa di miso", "Gamberi sale e pepe", "Carpaccio di pesce",
        ("Tartare di salmone", 80), ("Tartare di tonno", 80), "Poke bowl al salmone",
        "Birra chiara",
    ]),
    ("Trattoria", [
        "Antipasto affettati e formaggi", "Tigella", "Gnocco fritto, 3 pezzi",
        "Tagliatelle al ragù, porzione", "Lasagne, porzione",
        "Tortellini in brodo, porzione", "Tortelloni burro e salvia, porzione",
        "Passatelli in brodo, porzione", "Gramigna con salsiccia, porzione",
        "Pasta alle vongole, porzione", "Risotto, porzione",
        "Cotoletta alla bolognese", "Tagliata di manzo con rucola e grana",
        "Grigliata mista di carne", "Pollo arrosto, porzione",
        "Pesce alla griglia, porzione", "Vitello tonnato, porzione",
        "Friggione bolognese, porzione", "Patate al forno, porzione",
        "Verdure grigliate, porzione", "Insalata mista con olio", ("Pane bianco", 50),
        "Vino rosso", "Vino bianco", "Tiramisù, porzione",
    ]),
    ("Hamburgeria", [
        "Burger classico, 100 g di manzo", "Burger classico, 200 g di manzo",
        "Cheeseburger, 100 g di manzo", "Cheeseburger, 200 g di manzo",
        "Burger bacon e cheddar, 100 g di manzo", "Burger bacon e cheddar, 200 g di manzo",
        "Burger con cipolla caramellata, 100 g di manzo",
        "Burger con cipolla caramellata, 200 g di manzo",
        "Burger con salse gourmet, 100 g di manzo", "Burger con salse gourmet, 200 g di manzo",
        "Patatine fritte, porzione", "Anelli di cipolla, porzione",
        "Nuggets di pollo, 6 pezzi", "Cola", "Cola zero", "Birra chiara",
        "Birra artigianale IPA",
    ]),
    ("Bar, colazione", [
        "Cappuccino", "Caffè", "Caffè con zucchero", "Latte macchiato",
        "Cappuccino di soia", "Cappuccino con latte d'avena", "Caffè al ginseng",
        "Brioche vuota", "Brioche alla crema", "Brioche alla marmellata",
        "Brioche integrale al miele", "Pain au chocolat", "Muffin al cioccolato",
        "Spremuta d'arancia", "Toast prosciutto e formaggio",
        "Tramezzino tonno e pomodoro", "Tramezzino prosciutto e mozzarella",
        "Pizzetta rossa",
    ]),
    ("Aperitivo", [
        "Aperol spritz", "Campari spritz", "Hugo spritz", "Campari soda",
        "Campari liscio", "Gin tonic", "Negroni", "Americano", "Mojito",
        "Moscow mule", "Prosecco", "Vino bianco", "Birra chiara", "Crodino",
        "Birra analcolica", ("Olive verdi", 30), ("Taralli", 30),
        ("Arachidi tostate salate", 30), ("Patatine in busta", 30),
        "Tartina con salumi", "Pizzetta mignon", "Salatino di sfoglia",
    ]),
    ("Piadineria e kebab", [
        "Piadina con crudo e squacquerone", "Piadina cotto e fontina",
        "Piadina verdure grigliate e stracchino", "Piadina kebab", "Kebab",
        "Kebab al piatto con patatine", ("Falafel", 100), "Panino con porchetta",
        "Panino con cotoletta", "Panino bresaola, rucola e grana",
        "Patatine fritte, porzione", "Cola", "Birra chiara",
    ]),
    ("Poke", [
        "Poke bowl al salmone", "Poke bowl al tonno", "Poke bowl al pollo", "Poke bowl",
        ("Edamame", 80), "Insalata di alghe wakame", "Zuppa di miso",
    ]),
]

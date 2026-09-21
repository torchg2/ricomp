# Ricomp — guida passo passo

v3.2 · 21/09/2026

Metti questo file nel repo insieme agli altri: GitHub lo mostra formattato,
quindi lo leggi dal telefono aprendo il repo.

---

## 1. Aggiornare l'app

Fallo in questo ordine. Salta il passo 1 e rischi di perdere i dati.

1. **Backup prima di toccare qualsiasi cosa.** Apri l'app com'è adesso
   (v2) → scheda **Misure** → in fondo, card **Dati** → **Scarica file**.
   Ti salva `ricomp-backup-AAAA-MM-GG.json` nei Download. Non serve
   aprirlo, serve solo che esista.
2. **Apri il repo** su GitHub: `github.com/torchg2/ricomp`.
3. **Carica i file della radice.** Pulsante **Add file** → **Upload
   files** → trascina (o seleziona) questi sei:
   - `index.html`
   - `sw.js`
   - `manifest.json`
   - `icon-192.png`
   - `icon-512.png`
   - `icon-maskable-512.png`

   Sono gli stessi nomi di prima: GitHub li sovrascrive, è giusto così.
4. **Scrivi il messaggio di commit** (in fondo alla pagina): il numero di versione basta (`v3.2`).
   Poi **Commit changes**.
5. **Crea la cartella `src/`.** Serve solo la prima volta: nel repo non
   esiste ancora, e su GitHub non c'è un pulsante "nuova cartella". Si fa
   così: **Add file** → **Create new file** → nel campo del nome scrivi
   esattamente

   ```
   src/note.txt
   ```

   La barra `/` è quello che crea la cartella. Nel riquadro del contenuto
   scrivi una riga qualsiasi (`sorgenti`), poi **Commit changes**. Adesso
   nel repo vedi la cartella `src`.
6. **Carica i sorgenti.** Entra in `src/` (tocchi il nome della cartella)
   → **Add file** → **Upload files** → carica questi dieci file:
   - `foods.py`, `meals.py`, `app_data.py`, `esercizi.py`
   - `ristoranti.py`, `fonts_data.py` (nuovi dalla 3.2)
   - `build_app.py`, `make_icons.py`
   - `test.js`, `tests_body.js`

   Sono file, non cartelle: li selezioni tutti insieme. Poi **Commit
   changes**. Le volte successive parti direttamente da qui, perché la
   cartella ormai c'è.
7. **Aspetta il deploy.** Tab **Actions** del repo: compare una riga con
   una pallina gialla che gira. Quando diventa un segno verde, il sito è
   aggiornato. Di solito 1-2 minuti.
8. **Chiudi l'app sul telefono davvero.** Non basta tornare alla home:
   apri il multitasking (il quadratino o lo swipe su) e scarta la scheda
   di Ricomp.
9. **Riapri dall'icona.** La prima apertura scarica la versione nuova.

### Verifica che sia andata

- Scheda **Misure**, in fondo alla pagina: deve leggersi la versione nuova
  (**v3.2 · 21/09/2026**). Se leggi quella vecchia, l'app sta ancora usando la copia in cache:
  ripeti i passi 8 e 9, e se serve aspetta un minuto.
- In **Oggi** compare una volta sola la card **Novità** della versione. La
  chiudi con **Ok, visto** e non torna più.
- In basso ci sono **cinque** schede: Oggi, Piano, Allenamento, Misure,
  Grafici. Se ne vedi quattro, sei ancora sulla v2.
- I dati del diario ci sono ancora. Se per qualunque motivo non ci fossero:
  Misure → **Importa backup** → scegli il file del passo 1.

### Se qualcosa non torna

| Cosa vedi | Cosa fare |
|---|---|
| Resta la v2 dopo due riaperture | Chiudi l'app, aspetta 2 minuti, riapri. Il service worker aggiorna alla prima richiesta riuscita. |
| Actions con la pallina rossa | Il commit non è passato. Apri la riga, guarda l'errore, ricarica il file mancante. |
| L'icona sulla home è quella vecchia | È la cache di Android, non un problema. Togli l'icona e rimettila da Chrome: i dati stanno nel browser, non nell'icona, non si perde niente. |
| Pagina bianca | Hai caricato `index.html` dentro `src/` invece che nella radice. Rimettilo nella radice. |
| Vuoi tornare indietro | Repo → `index.html` → **History** → commit precedente → **View file** → **Raw** → salvi e ricarichi quel file. |

---

## 2. La giornata

### Mattina

1. **Misure** → campo **Peso di stamattina**. A digiuno, dopo il bagno,
   sempre nelle stesse condizioni. Se scrivi un numero fuori da 40-150 kg
   l'app ti chiede conferma: è il filtro contro il 7,1 al posto di 71.
2. **Allenamento** → in fondo, card **Anche oggi** → premi il numero.
   Ogni giorno, anche di riposo: **0** niente · **1** lo sento ma passa ·
   **2** fastidio tutto il giorno · **3** dolore.
   Il voto sta sul giorno in cui lo dai, e l'app sa da sola se ieri avevi
   fatto una seduta e quale.

### Durante il giorno, i pasti

In **Oggi**, ogni pasto è una card. Quattro modi per riempirla, dal più
veloce al più lento:

1. **Dal piano** — apre le opzioni del pasto dal piano alimentare. Tocchi
   un'opzione, vedi ingredienti e grammi, **Aggiungi**. È la strada
   normale.
2. **Ripeti ieri** — copia lo stesso pasto di ieri, tutte le righe in un
   colpo. Se sbagli, **Annulla** in fondo allo schermo toglie tutto il
   gruppo.
3. **+ Cerca un alimento** — la ricerca. Tollera gli errori di battitura
   ("yougurt", "brocoli"). Cerca tra alimenti, opzioni del piano (anche
   per ingrediente: scrivi "sgombro" e trovi le cene che lo contengono),
   piatti tipici e i tuoi alimenti nuovi.
4. **Ristorante** — chip nella ricerca. Scegli il locale (pizzeria,
   sushi, trattoria, hamburgeria, bar, aperitivo, piadineria, poke) e
   componi il pasto con **−** e **+**. L'interruttore *condimento da
   ristorante* aggiunge il 15% alle calorie dei piatti, come olio.
5. **Nuovo alimento** / **Stima rapida** — in fondo alla ricerca.
   *Nuovo alimento* salva i valori per 100 g dall'etichetta e lo ritrovi
   per sempre nella categoria Nuovi. *Stima rapida* è per quello che non
   trovi da nessuna parte: kcal, proteine, grassi, carboidrati e fibra a
   occhio.

Dopo **+ Aggiungi** la scheda resta aperta, così ne metti tre di fila. La
chiudi con **Fatto**. La quantità proposta è l'ultima che hai usato per
quell'alimento.

In cima alla scheda Oggi scegli il tipo di giornata (**Allenamento**,
**Riposo**, **Storta**), poi vedi due anelli: calorie che restano e
proteine che mancano. Sotto, grassi, carboidrati e fibra con una tacca sul
target. Un pasto oltre il 10% del suo obiettivo diventa ambra. In **Piano** le opzioni che non
ci stanno più nel residuo diventano grigie: non sono vietate, sono un
avviso.

### Sera, dopo l'allenamento

Scheda **Allenamento**:

1. Controlla la seduta proposta in alto (il calendario di partenza è
   lunedì A, martedì B, giovedì C, sabato D). Se oggi fai un'altra seduta,
   tocca la pillola **A / B / C / D** giusta.
2. **30 minuti** o **15 minuti**. La versione corta tiene i primi tre
   esercizi.
3. Apri **Riscaldamento**: la lista cambia secondo la zona della seduta.
   Se ti alleni entro un'ora dal risveglio metti **Entro un'ora dal
   risveglio**: diventa di 8 minuti e la prima serie di ogni esercizio va
   fatta al 70%.
4. Premi **Inizia la seduta**: si apre la modalità a tutto schermo.
   Negli esercizi a ripetizioni premi **Serie fatta** e il recupero parte
   da solo. Negli esercizi a tempo lavoro e recupero si alternano da soli.
   Il circuito D va avanti da solo per i quattro giri. Vibra a 3-2-1 e a
   ogni cambio; lo schermo resta acceso. Alla fine **Segna come fatta**.
   Se preferisci la lista, tocca il **nome** di un esercizio per la
   scheda (Attenzione, Prima, Durante, Errori comuni, Perché lo fai, Se
   fa male) e il pulsante con i secondi per il recupero.
5. Dopo la seduta compaiono i **+** e i **−** accanto a ogni esercizio:
   segni solo quelli andati diversamente dal previsto. Due volte di fila
   sopra il previsto e l'app propone il passo successivo (serie, poi
   ripetizioni, poi elastico, poi tempo): lo applichi tu con **Applica**.
   Se il giorno dopo l'anca era a 2 o più, niente proposta. Dalla scheda
   dell'esercizio puoi sempre tornare allo schema del piano.

### Il resto

Tieni premuta l'icona di Ricomp sulla home: compaiono **Peso**, **Pasto**
(apre il pasto giusto per l'ora) e **Allenamento**. Android può metterci un
giorno a mostrarle; se non arrivano, togli e rimetti l'icona.

Integratori e acqua sono in fondo a Oggi: le pillole si accendono al tocco
(creatina, omega-3, vitamina D), l'acqua va a bicchieri da 0,25 L.

Per cambiare giorno: frecce in cima, oppure **scorri col dito** a destra o
sinistra sulla scheda. Tocchi la data e torni a oggi.

---

## 3. Modificare i valori nutrizionali

Cerchi l'alimento, apri la quantità, **Modifica i valori nutrizionali**.
Poi scegli:

- **Salva per sempre** — da adesso in poi ogni volta che usi
  quell'alimento. È per le correzioni da etichetta: il tuo yogurt fa 10,3
  g di proteine e non 10. Compare un'etichetta *modificato* accanto al
  nome.
- **Solo per questa volta** — vale solo per la riga che stai aggiungendo.
  È per "oggi ho preso un'altra marca".
- **Ripristina il valore originale** — compare solo se l'alimento è già
  stato modificato, e riporta ai valori del database.

Le righe già registrate nei giorni passati non cambiano mai: restano con i
valori che avevano quando le hai scritte.

---

## 4. Una volta a settimana

- **Girovita e fianchi** in Misure: stesso giorno, a digiuno, a fine
  espirazione, metro non stretto. Sono la misura che conta più del peso.
- Guarda **Settimana contro settimana**: appare quando hai almeno 14
  pesate e confronta due periodi senza giorni in comune.
- Guarda l'**aderenza** in Grafici: sedute a settimana sulle ultime
  quattro.

---

## 5. Ogni 14 giorni: il protocollo

In **Misure**, card **Protocollo dei 14 giorni**.

- **Tace fino al giorno 21.** Nelle prime tre settimane la creatina
  trattiene 1-1,5 kg d'acqua e ogni numero sarebbe falso.
- Poi legge peso, girovita e forza e **propone** una mossa: aggiungere
  150, togliere 150 o non toccare niente, con scritto il perché.
- Premi **Applica** solo se sei d'accordo. L'app sposta i target, poi tace
  altri 14 giorni. Non scende mai sotto 1.750 kcal e non si muove mai di
  più di 150 alla volta.
- Se la forza è calata, la bilancia perde: il protocollo te lo dice e
  blocca la discesa.

### Al giorno 21, una domanda sola

Compare in Oggi: **finisci i pasti senza sforzo?**
Se rispondi **Sì**, il target sale di 100 kcal e la domanda sparisce.
Se rispondi **No, non ancora**, te la richiedo fra 14 giorni.
Motivo: 2.050 non è un mantenimento, è un deficit di 250 sul dispendio
stimato. È un punto di partenza, non un dogma.

---

## 6. La settimana storta

Terza opzione del selettore in cima a **Oggi**. Sceglila quando sei in
influenza, notti in bianco, viaggio.

Cosa cambia finché è attiva:
- tre pasti invece di quattro (colazione, pranzo, cena);
- target a **2.150 kcal**, che è mantenimento, non deficit;
- proteine sempre 135: quelle non si toccano mai;
- in Allenamento: due sedute, A e B, in versione corta. L'obiettivo è non
  perdere terreno.

Resta attiva anche nei giorni dopo, finché non scegli **Allenamento** o
**Riposo**: a quel punto il periodo finisce ieri e oggi torna normale.
Se la attivi e la togli lo stesso giorno, non resta traccia. Su un giorno
passato vale solo per quel giorno. La settimana dopo la fine resta fuori
dai calcoli del protocollo.

---

## 7. Backup

I dati stanno **solo su questo telefono**, dentro il browser. Nessun
server, nessun account.

- **Una volta al mese**, e sempre prima di aggiornare: Misure →
  **Condividi backup**. Si apre il menu di Android: mandalo su Drive, o su
  Telegram a te stesso. Se preferisci il file nei Download, **Scarica
  file**.
- Dopo un mese senza backup l'app te lo ricorda da sola.
- **Importa backup** sostituisce tutto quello che c'è adesso, quindi usalo
  solo per recuperare.
- In Misure c'è scritto **Dati: protetti / non protetti**. Sull'app
  installata dalla home dovrebbe diventare *protetti* da solo: significa
  che Android non li cancellerà per liberare spazio. Se resta *non
  protetti*, non è grave, ma il backup conta di più.

Cosa cancella i dati: svuotare i dati di Chrome, disinstallare Chrome,
"pulizia spazio" aggressiva. Togliere e rimettere l'icona dalla home no.

---

## 8. Chiedermi delle modifiche

Il file `index.html` è **generato**: non si modifica a mano, si rigenera
dai `.py` dentro `src/`. Quindi:

1. Apri una chat nuova con me.
2. Carica i file di `src/` che servono. Se non sai quali, caricali tutti:
   sono otto e leggeri.
3. Dimmi cosa cambiare. Esempi: "aggiungi questi 12 alimenti",
   "cambia i grammi del pranzo con il salmone", "il timer deve vibrare
   due volte".
4. Ti restituisco `index.html` aggiornato **e** i `.py` modificati. Li
   ricarichi tutti e due, come nella sezione 1 di questa guida.

Regola: **index.html e src/ si committano sempre insieme.** Se aggiorni
solo uno dei due, la volta dopo ripartiamo da sorgenti sbagliati.

Cose che puoi cambiare da solo senza di me, direttamente nell'app:
target e profilo (Misure → Target e profilo), valori di un alimento,
alimenti nuovi.

---

## 9. Cosa l'app non fa

- **Notifiche e promemoria.** Servirebbe un server che le mandi, e GitHub
  Pages non lo è. Se vuoi il promemoria, mettilo nella sveglia del
  telefono.
- **Sincronizzazione tra dispositivi.** Un telefono, un diario. Il backup
  è l'unico ponte.
- **Codici a barre.** Serve la fotocamera e un database di prodotti a
  pagamento.
- **Diagnosi.** Il voto anca è un registro, non un medico.

---

## 10. Due promemoria che restano fuori dall'app

- La **parte bassa** del piano (ponte, abduzione, stacco rumeno, affondo
  indietro) va fatta validare da un fisioterapista. L'app te la mostra
  perché è quello che c'è scritto nel piano, non perché qualcuno l'abbia
  vista muoversi.
- **Regola del dolore**: se il giorno dopo il voto è 2, dimezzi il range
  dell'esercizio sospetto; se è 3, lo togli. Se il fastidio c'è anche
  senza allenarti, o ti sveglia di notte, chiami l'ortopedico invece di
  aggiustare le ripetizioni.

# Migrazione Joomla → POC statico (senza deploy)

## Perimetro e decisioni

- Sorgente: dump locale fornito dall'utente; lettura offline esclusiva di `jos25_content`, `jos25_categories`, `jos25_menu`. SQL mai eseguito. Il dump integrale e la copia filtrata privata non sono nel repository.
- 292 articoli: 200 pubblicati, 23 archiviati, 12 non pubblicati, 57 cestinati; 37 categorie, 22 `com_content`; 42 articoli con `catid=0`; 84 menu. Censimento verificato autonomamente dal dump.
- Importati **83** articoli, esclusi **209**, errori **0**. Esclusioni mutuamente esclusive: 92 non pubblici/non pubblicati (inclusi archiviati e cestinati), 28 con categoria mancante/non pubblica o ascendenza non pubblica, 89 fuori dalla finestra di pubblicazione al cutoff esplicito `2026-10-29 00:00:00`. Nessuna bozza/cestinato/archiviato viene pubblicato per errore. `catid=0` non equivale a categoria pubblica ed è escluso.
- Accesso articolo e categoria richiesto: `1` (Public). Stato articolo e categorie: `1`. Sono controllati anche gli antenati delle categorie e le date `publish_up`/`publish_down`.
- Testi proiettati in testo semplice, poi escaped da Astro: niente `set:html`, script, attributi, form, iframe o plugin. Autori, utenti, sessioni, credenziali e metadati privati non sono esportati. Email, telefoni, IBAN e codici fiscali riconoscibili sono oscurati automaticamente. Serve comunque revisione editoriale della privacy: non è una garanzia assoluta su qualsiasi dato nel testo pubblico.
- 76 articoli richiedono revisione automatica; 96 riferimenti multimediali omessi. Immagini, locandine, mappe incorporate, allegati e collegamenti HTML originali **non migrati**, non scaricati e non inventati. Anche gli articoli senza avviso richiedono approvazione editoriale prima di un eventuale deploy.

## Struttura e URL

Il confronto degli href pubblici osservati con le rotte effettive e la specifica non eseguibile dei redirect candidati sono in [URL-COMPARISON-DRAFT.md](URL-COMPARISON-DRAFT.md). È una bozza parziale, non una configurazione di produzione.

`src/data/joomla.json` è un formato pubblico minimizzato con ID, alias originale, titolo, categoria, date originali e paragrafi. `docs/import-report.json` contiene soltanto conteggi e limiti.

Le nuove pagine POC sono `/notizie/<id>-<alias>/`: sono percorsi nuovi e univoci, **non URL SEF storici dedotti**. Solo un menu pubblico diretto ad articolo è mappabile: `/dove-siamo/`. La pagina mantiene l'indirizzo POC ed espone anche il testo storico associato, distinto dai dati correnti da confermare. Le altre voci menu (categorie, estensioni o destinazioni escluse) non sono trasformate arbitrariamente in redirect. Occorrono un inventario URL pubblico e verifica editoriale prima di definire redirect Joomla, `.html`, `/joomla/` e query `index.php`.

Date conservate come wall time originali; il dump non specifica il fuso. `created` mancante resta tale, non viene sostituito con una data inventata. Home e archivio usano la stessa fonte; le schede rimandano a pagine reali. Ricerca e filtro categoria sono miglioramenti progressivi: senza JavaScript l'archivio resta interamente leggibile.

## Discrepanze da confermare

- La precedente demo conteneva titoli, date, riassunti e categorie scritti a mano, non un'estrazione affidabile. Sono sostituiti dall'archivio, senza presumere che quelle date fossero reali.
- Un elemento della demo associava un concerto alla categoria Teatro; ora si usano le categorie Joomla, senza riclassificazione inventata.
- Nome completo del circolo, indirizzo, email, telefono, Facebook e coordinate provengono **solo dal POC precedente** e sono centralizzati in `src/data/association.ts`, con avviso di conferma. Non si assumono verificati dal dump né si inferiscono codici fiscali, rappresentanti o dati legali.
- Orari della demo contraddittori (apertura tutti i pomeriggi ma lunedì/festivi chiuso) e cellulari non confermati: rimossi come informazioni correnti, non sostituiti con altri valori.
- Media e allegati non disponibili nel dump; recupero, diritti e verifica dei link esterni restano da completare. Nessuna richiesta al sito istituzionale.

## Riproduzione locale

Richiesti Node >=22.12 e Python 3. Non servono DB, PHP, credenziali o accesso Joomla.

```sh
npm ci
python3 scripts/import_joomla.py /percorso/privato/dump.sql --as-of '2026-10-29 00:00:00'
npm run verify
npm audit
```

`npm run verify`: unit test parser/privacy/visibilità, Astro check, build statica, verifica di tutti i percorsi interni e asset locali generati, riconciliazione conteggi e `noindex`. Non verifica media esterni: non sono incorporati nell'archivio. Il POC ha banner esplicito e `noindex,nofollow`, ma non è un sistema di controllo accessi.

## Sicurezza operativa

Il guard `verify_private_inventory_is_not_built` è un **controllo strutturale di leakage noto, non un sistema completo di data-loss prevention**: rifiuta `complete-review-inventory.json` come componente esatto di un percorso di output (file o directory), i token case-sensitive `editorialStatus`, `reviewFlags`, `sourceAccess`, `sourceState` nei nomi di file/directory e i marker letterali nei contenuti letti come UTF-8 e nei dati pubblici serializzati. Dati privati rinominati arbitrariamente, codificati, compressi o trasformati possono sfuggire al controllo. Il guard verifica inoltre gli ID nelle route articolo convenzionali; il controllo principale verifica separatamente tutti i percorsi attesi e il conteggio HTML. Nessun esito positivo sostituisce la revisione editoriale/privacy né autorizza la pubblicazione.

Il workflow esistente `.github/workflows/deploy.yml` effettua deploy su push a **main** o avvio manuale. Per questo il lavoro viene mantenuto su ramo dedicato e PR non integrata: **non fare merge, non avviare workflow, non pubblicare**, finché l'utente non autorizza separatamente. Non sono modificati DNS, Cloudflare, Joomla, sito istituzionale o produzione. Prima di qualsiasi futuro push verificare anche eventuali integrazioni Cloudflare Git esterne alle Actions.

La directory `tools/` era già presente e non tracciata all'avvio: non fa parte di questa modifica e non è stata eseguita né inclusa nel commit.

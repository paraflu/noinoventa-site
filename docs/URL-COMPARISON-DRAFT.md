# Confronto URL pubblici Joomla → rotte Astro — BOZZA

## Stato e provenienza

Documento di lavoro sul ramo `feat/joomla-static-archive`, PR draft #1. **Non è una configurazione redirect, non è approvato e non attiva alcuna regola.** Nessun deploy, merge, modifica DNS o scrittura su Joomla.

Rilevazione della sola home pubblica `https://www.noinoventa.it/` tramite browser, senza login. Il browser mantiene questo URL: la presenza di link sotto `/joomla` **non dimostra un redirect HTTP della root**. La tabella conserva gli href assoluti effettivamente osservati, decodificati dal DOM (non i byte HTML con `&amp;`). Nessuna destinazione elencata è stata aperta in questa rilevazione: stato HTTP, canonical e catene di redirect restano da verificare. Esclusi account, invio email e frammenti.

Il confronto usa esclusivamente `src/data/joomla.json`, `src/pages/` e `docs/import-report.json`. Gli alias non ricostruiscono gli URL SEF storici. Nessun dump privato o inventario editoriale è esportato qui.

## Rotte già esistenti (non proposte nuove)

- `/`: home POC, con selezione di articoli.
- `/notizie/`: archivio POC degli articoli importati, non archivio Joomla né pagina dedicata alla categoria 35.
- `/dove-siamo/`: pagina POC collegata dal solo menu articolo nel JSON (`articleId=73`).
- Le pagine articolo sono esclusivamente i campi `articles[].path` del JSON, generati da `src/pages/notizie/[slug].astro`.

Per l'articolo 73 esiste anche `/notizie/73-dove-siamo-52774165/`: la bozza sceglie `/dove-siamo/` come destinazione del vecchio menu. La gestione del duplicato/canonical richiede una decisione successiva; nessun redirect interno è stato aggiunto.

## Inventario osservato e confronto

45 URL distinti dopo deduplica: 16 candidato, 2 candidato parziale, 27 sospeso. I candidati indicano corrispondenze documentali, non equivalenze approvate.

| Etichetta nella home | URL Joomla osservato | Rotta Astro esistente | Esito / limite |
|---|---|---|---|
| Associazione NOI - Noventa di Piave | `https://www.noinoventa.it/joomla` | `/` | Candidato — Ingresso al sito; equivalenza editoriale da approvare. |
| Home | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=category&layout=blog&id=35&Itemid=60` | `/` | Candidato parziale — Il POC aggrega più categorie: non è una replica della categoria 35. |
| Dove siamo... | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=article&id=73&Itemid=57` | `/dove-siamo/` | Candidato — ID presente nel JSON pubblico; pagina istituzionale già mappata nel POC. |
| Notizie | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=category&layout=blog&id=35&Itemid=50` | `/notizie/` | Candidato parziale — Il POC aggrega più categorie: non è una replica della categoria 35. |
| Articoli archiviati | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=archive&Itemid=58` | — | Sospeso — Archivio Joomla (anche mensile) non equivalente a /notizie/: gli articoli source state=2 sono esclusi dal POC. |
| Rassegne Teatrali | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=category&layout=blog&id=34&Itemid=59` | — | Sospeso — Nessuna rotta di categoria esistente; /notizie/ è solo una possibile alternativa editoriale, non equivalente. |
| Sagra ed Eventi | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=category&layout=blog&id=15&Itemid=170` | — | Sospeso — Nessuna rotta di categoria esistente; /notizie/ è solo una possibile alternativa editoriale, non equivalente. |
| Rassegna cinematografica | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=category&layout=blog&id=15&Itemid=171` | — | Sospeso — Nessuna rotta di categoria esistente; /notizie/ è solo una possibile alternativa editoriale, non equivalente. |
| Galleria | `https://www.noinoventa.it/joomla/index.php?option=com_phocagallery&view=categories&Itemid=158` | — | Sospeso — Componente e media non migrati; nessuna /galleria/ esistente. |
| Stampa | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=article&id=293:veneto-legge-2026&catid=35&Itemid=50&tmpl=component&print=1&layout=default&page=` | `/notizie/293-veneto-legge-2026/` | Candidato — ID presente nel JSON pubblico; destinazione esatta dal campo path. Link osservato solo nella variante stampa; non prova il permalink ordinario. |
| veneto legge 2026_3.pdf | `https://www.noinoventa.it/joomla/attachments/article/293/veneto%20legge%202026_3.pdf` | — | Sospeso — Allegato osservato ma non scaricato/migrato; nessun redirect a una pagina HTML. |
| Stampa | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=article&id=292:castagnata-2026&catid=35&Itemid=50&tmpl=component&print=1&layout=default&page=` | `/notizie/292-castagnata-2026/` | Candidato — ID presente nel JSON pubblico; destinazione esatta dal campo path. Link osservato solo nella variante stampa; non prova il permalink ordinario. |
| Stampa | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=article&id=291:il-palco-ti-aspetta&catid=35&Itemid=50&tmpl=component&print=1&layout=default&page=` | `/notizie/291-il-palco-ti-aspetta/` | Candidato — ID presente nel JSON pubblico; destinazione esatta dal campo path. Link osservato solo nella variante stampa; non prova il permalink ordinario. |
| CorsoTeatro2026.png | `https://www.noinoventa.it/joomla/attachments/article/291/CorsoTeatro2026.png` | — | Sospeso — Allegato osservato ma non scaricato/migrato; nessun redirect a una pagina HTML. |
| Stampa | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=article&id=290:benedizione-e-affidamento-dei-bambini-a-maria&catid=35&Itemid=50&tmpl=component&print=1&layout=default&page=` | `/notizie/290-benedizione-e-affidamento-dei-bambini-a-maria/` | Candidato — ID presente nel JSON pubblico; destinazione esatta dal campo path. Link osservato solo nella variante stampa; non prova il permalink ordinario. |
| Stampa | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=article&id=289:marco-tanduo-e-band-christian-music-concert&catid=35&Itemid=50&tmpl=component&print=1&layout=default&page=` | `/notizie/289-marco-tanduo-e-band-christian-music-concert/` | Candidato — ID presente nel JSON pubblico; destinazione esatta dal campo path. Link osservato solo nella variante stampa; non prova il permalink ordinario. |
| Appuntamenti in Chiesa 3-8 settembre 2026 | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=article&id=288:appuntamenti-in-chiesa-3-8-settembre-2026&catid=35&Itemid=50` | `/notizie/288-appuntamenti-in-chiesa-3-8-settembre-2026/` | Candidato — ID presente nel JSON pubblico; destinazione esatta dal campo path. |
| Notte di fiabe al Parco – ECCO I MOSTRI! | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=article&id=287:notte-di-fiabe-al-parco-ecco-i-mostri&catid=35&Itemid=50` | `/notizie/287-notte-di-fiabe-al-parco-ecco-i-mostri/` | Candidato — ID presente nel JSON pubblico; destinazione esatta dal campo path. |
| In nome della madre | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=article&id=286:in-nome-della-madre&catid=35&Itemid=50` | `/notizie/286-in-nome-della-madre/` | Candidato — ID presente nel JSON pubblico; destinazione esatta dal campo path. |
| Festeggiamenti del Rosario – 24ª edizione | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=article&id=285:festeggiamenti-del-rosario-24-edizione&catid=35&Itemid=50` | `/notizie/285-festeggiamenti-del-rosario-24-edizione/` | Candidato — ID presente nel JSON pubblico; destinazione esatta dal campo path. |
| Rassegna Teatrale | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=category&id=34&Itemid=59` | — | Sospeso — Nessuna rotta di categoria esistente; /notizie/ è solo una possibile alternativa editoriale, non equivalente. |
| Rassegna cinematografica | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=category&id=45&Itemid=50` | — | Sospeso — Nessuna rotta di categoria esistente; /notizie/ è solo una possibile alternativa editoriale, non equivalente. |
| 2 | `https://www.noinoventa.it/joomla/index.php?limitstart=5&limit=5` | — | Sospeso — Paginazione Joomla non riprodotta; nessun redirect generalizzato al solo archivio. |
| 3 | `https://www.noinoventa.it/joomla/index.php?limitstart=10&limit=5` | — | Sospeso — Paginazione Joomla non riprodotta; nessun redirect generalizzato al solo archivio. |
| 4 | `https://www.noinoventa.it/joomla/index.php?limitstart=15&limit=5` | — | Sospeso — Paginazione Joomla non riprodotta; nessun redirect generalizzato al solo archivio. |
| 5 | `https://www.noinoventa.it/joomla/index.php?limitstart=20&limit=5` | — | Sospeso — Paginazione Joomla non riprodotta; nessun redirect generalizzato al solo archivio. |
| 6 | `https://www.noinoventa.it/joomla/index.php?limitstart=25&limit=5` | — | Sospeso — Paginazione Joomla non riprodotta; nessun redirect generalizzato al solo archivio. |
| 7 | `https://www.noinoventa.it/joomla/index.php?limitstart=30&limit=5` | — | Sospeso — Paginazione Joomla non riprodotta; nessun redirect generalizzato al solo archivio. |
| 8 | `https://www.noinoventa.it/joomla/index.php?limitstart=35&limit=5` | — | Sospeso — Paginazione Joomla non riprodotta; nessun redirect generalizzato al solo archivio. |
| 9 | `https://www.noinoventa.it/joomla/index.php?limitstart=40&limit=5` | — | Sospeso — Paginazione Joomla non riprodotta; nessun redirect generalizzato al solo archivio. |
| Dove siamo | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=article&id=73:dove-siamo-52774165&catid=36:notizie&Itemid=57` | `/dove-siamo/` | Candidato — ID presente nel JSON pubblico; pagina istituzionale già mappata nel POC. |
| La storia siamo noi | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=article&id=77:lastoriasiamonoi&catid=34:rassegna-teatrale&Itemid=59` | `/notizie/77-lastoriasiamonoi/` | Candidato — ID presente nel JSON pubblico; destinazione esatta dal campo path. |
| La Scena incantata 2011 - Letture di fiabe e fumetti con video animazioni | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=article&id=66:la-scena-incantata-2011-letture-di-fiabe-e-fumetti-con-video-animazioni&catid=34:rassegna-teatrale&Itemid=59` | `/notizie/66-la-scena-incantata-2011-letture-di-fiabe-e-fumetti-con-video-animazioni/` | Candidato — ID presente nel JSON pubblico; destinazione esatta dal campo path. |
| "Non spegnere... la candela" | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=article&id=76:qnon-spegnere-la-candelaq&catid=34:rassegna-teatrale&Itemid=59` | `/notizie/76-qnon-spegnere-la-candelaq/` | Candidato — ID presente nel JSON pubblico; destinazione esatta dal campo path. |
| Domenica 1 Aprile | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=article&id=80:domenica-1-aprile&catid=34:rassegna-teatrale&Itemid=59` | `/notizie/80-domenica-1-aprile/` | Candidato — ID presente nel JSON pubblico; destinazione esatta dal campo path. |
| Marzo, 2020 | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=archive&year=2020&month=3&Itemid=58` | — | Sospeso — Archivio Joomla (anche mensile) non equivalente a /notizie/: gli articoli source state=2 sono esclusi dal POC. |
| Ottobre, 2019 | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=archive&year=2019&month=10&Itemid=58` | — | Sospeso — Archivio Joomla (anche mensile) non equivalente a /notizie/: gli articoli source state=2 sono esclusi dal POC. |
| Aprile, 2019 | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=archive&year=2019&month=4&Itemid=58` | — | Sospeso — Archivio Joomla (anche mensile) non equivalente a /notizie/: gli articoli source state=2 sono esclusi dal POC. |
| Settembre, 2018 | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=archive&year=2018&month=9&Itemid=58` | — | Sospeso — Archivio Joomla (anche mensile) non equivalente a /notizie/: gli articoli source state=2 sono esclusi dal POC. |
| Novembre, 2017 | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=archive&year=2017&month=11&Itemid=58` | — | Sospeso — Archivio Joomla (anche mensile) non equivalente a /notizie/: gli articoli source state=2 sono esclusi dal POC. |
| Novembre, 2016 | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=archive&year=2016&month=11&Itemid=58` | — | Sospeso — Archivio Joomla (anche mensile) non equivalente a /notizie/: gli articoli source state=2 sono esclusi dal POC. |
| Settembre, 2016 | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=archive&year=2016&month=9&Itemid=58` | — | Sospeso — Archivio Joomla (anche mensile) non equivalente a /notizie/: gli articoli source state=2 sono esclusi dal POC. |
| Ottobre, 2015 | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=archive&year=2015&month=10&Itemid=58` | — | Sospeso — Archivio Joomla (anche mensile) non equivalente a /notizie/: gli articoli source state=2 sono esclusi dal POC. |
| Maggio, 2015 | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=archive&year=2015&month=5&Itemid=58` | — | Sospeso — Archivio Joomla (anche mensile) non equivalente a /notizie/: gli articoli source state=2 sono esclusi dal POC. |
| Aprile, 2015 | `https://www.noinoventa.it/joomla/index.php?option=com_content&view=archive&year=2015&month=4&Itemid=58` | — | Sospeso — Archivio Joomla (anche mensile) non equivalente a /notizie/: gli articoli source state=2 sono esclusi dal POC. |

## Bozza regole candidate non-SEF (solo specifica, NON eseguibile)

1. Limitare il futuro matcher al dominio legacy autorizzato e al percorso `/joomla/index.php`. Fare parsing dei parametri, senza dipendere dall'ordine della query; rifiutare parametri duplicati/ambigui. Non applicare wildcard a tutto `/joomla/*`.
2. Per `option=com_content`, `view=article`, usare un allowlist esplicito ID → `articles[].path` verificato sul JSON pubblico. Per ID 73 la destinazione candidata del menu è `/dove-siamo/`. Mai costruire la destinazione dall'alias ricevuto nella richiesta.
3. Gli href osservati includono ID numerici (`73`) e token `id:alias`. L'eventuale riconoscimento di entrambe le forme è una **proposta da testare**, non prova che ogni variante senza `Itemid`, senza `catid`, con alias diverso o sotto `/index.php` funzioni sul legacy. Prima usare le combinazioni effettivamente elencate. Gli eventuali ID non importati restano sospesi, senza fallback a home; l'ID 80 osservato è invece presente nel JSON e ha una destinazione esplicita nella tabella.
4. I link 293–289 sono stati osservati come URL di stampa (`tmpl=component&print=1&layout=default&page=`). La candidatura punta alla pagina articolo esistente; rimozione dei parametri stampa e uso della pagina ordinaria richiedono approvazione. Non presentare una variante ordinaria sintetizzata come URL osservato.
5. Le due combinazioni categoria 35 / Itemid 60 e 50 possono candidarsi rispettivamente a `/` e `/notizie/`, ma con perdita di semantica documentata. Non estendere questa regola alle altre categorie, all'archivio o alla paginazione.
6. Non associare automaticamente `com_phocagallery`, `com_users`, `com_mailto`, allegati, archivio mensile o articoli esclusi a pagine generiche. Per contenuti mancanti valutare recupero autorizzato o risposta 404/410 dopo revisione; nessuno stato viene imposto ora.
7. Nessun codice permanente 301/308 va attivato prima di inventario completo, revisione editoriale e test di equivalenza. L'hosting attuale/futuro e il supporto al matching delle query non sono stati verificati: non assumere che un file `_redirects` possa implementare questa specifica.

## Limiti e discrepanze verificati

- Campione della sola home: non è un crawl, sitemap, log accessi o inventario esaustivo; le destinazioni e gli allegati non sono stati richiesti. Nessun URL SEF `.html`, variante di host/protocollo, `/joomla/` con slash finale o altra root `index.php` è provato dal solo campione.
- La home mostra due riferimenti cinematografici incoerenti: voce menu categoria `15` / Itemid `171` e collegamento categoria `45` / Itemid `50`. Non correggerli arbitrariamente e non inventare una rotta cinema.
- L'articolo 80, incluso tra i collegamenti storici della home, è presente nel JSON pubblico (`/notizie/80-domenica-1-aprile/`), come gli altri ID articolo osservati. Questo dimostra la corrispondenza locale, non la risposta HTTP della pagina legacy.
- Il JSON pubblico minimizzato non conserva `categoryId` o `Itemid` per articolo; gli ID di categoria nella tabella provengono dai soli href osservati, non da una ricostruzione del routing Joomla.
- Report import: cutoff `2026-10-29 00:00:00` come wall time, non fuso verificato; 292 righe sorgente, 83 importate, 209 escluse, 0 errori. Gli archiviati sono esclusi: l'archivio storico Joomla non è coperto dal solo archivio POC. 76 articoli segnalati per revisione e 96 riferimenti media omessi; nessuna equivalenza visiva/editoriale garantita.
- I contenuti della home live e il dump possono rappresentare snapshot diversi. Presenza di un link non prova visibilità effettiva, completezza del testo, integrità degli allegati o validità della destinazione.
- Contatti e informazioni correnti restano da confermare; redazione automatica e `noindex` non sostituiscono revisione privacy né controllo accessi.

## Verifica locale e confini operativi

`npm run verify` esercita unit test, Astro check, build e controllo dei link/asset locali del POC. Non verifica i vecchi endpoint Joomla, le regole redirect (non implementate), la ricerca con interazione browser né media esterni. Verifica eseguita: 7 unit test superati; Astro check su 15 file con 0 errori, warning o hint; build di 86 pagine, incluse 83 rotte articolo; controllo statico di 1298 riferimenti interni/asset con riconciliazione e `noindex` superato. La verifica include il working tree attuale e quindi anche i test preesistenti non inclusi in questo aggiornamento. I path destinazione della tabella sono controllati separatamente contro `dist/` dopo build.

Il workflow tracciato effettua deploy su push a `main` o avvio manuale. Le eventuali integrazioni Cloudflare Git esterne non sono state verificate: questo aggiornamento documentale resta locale sul feature branch, senza push né attivazione workflow. Le modifiche preesistenti a `scripts/import_joomla.py`, `scripts/test_import_joomla.py` e la directory non tracciata `tools/` non fanno parte di questo intervento.

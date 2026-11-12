---
title: Vägar i AndThen
tab: Vägar
token: paths
order: 7
depends_on: []
source: AndThen 1.1.0 – plugin/README.md and COOKBOOK.md (https://github.com/IT-HUSET/andthen), labs/x2-ui-ux.md
---

# Vägar i AndThen

Eyebrow: Vägar och artefakter

## Vad kan du göra, och när?

Component: ”när” i rubriken sätts i accentfärgen.

Core Loop är huvudvägen. Vid sidan av den har AndThen fler vägar: en snabb rättelse, en omväg via design, en buggjakt, en ny domän. Den här fliken visar vilken väg som passar din situation, vad varje steg lämnar efter sig och vad du kan göra när pull requesten är mergad.

Component: under ingressen en rad länkknappar som scrollar till de fem sektionerna nedan. Den första är ifylld, de andra har kontur.

- Välj en väg → (#paths-pick)
- Vad som blir kvar → (#paths-left)
- Efter ship → (#paths-next)
- Exempel: ui-ux-design → (#paths-ui)
- Exempel: decide och spike → (#paths-decide)

## Vilken väg – Välj din situation

Varje skill fungerar på egen hand, så du börjar där du står. Är du osäker? Då undersöker `/andthen:now-what` projektet och skickar dig rätt.

Interactive component: en lista med situationsknappar till vänster och ett kort till höger (staplade på en telefon). Kortet visar situationen som rubrik, kedjan av skills som piller med pilar emellan (en valfri skill inom hakparentes får streckad ram), texten, en rad ”Du får” och kommandona med kopieringsknappar. Varje kommandoruta är först dold bakom en knapp ”Visa kommando”, som på de andra flikarna. En Link-rad blir en knapp under kommandona: en flik-token byter flik och ett #ankare scrollar till den sektionen. Kortet börjar på den första situationen. Piltangenterna upp och ned flyttar genom listan.

### fix

- Situation: En rättelse du kan beskriva i en mening
- Chain: implement-fix, ship
- Text: Ingen spec. `implement-fix` gör den minsta säkra ändringen, validerar den igen och committar den. På `main` frågar den först om den ska starta en funktionsbranch. `ship` skriver pull requesten och pushar den när du har sagt ja.
- You get: En verifierad ändring och en pull request. Inget annat skrivs.
- Command: `/andthen:implement-fix "<request>"`
- Command: `/andthen:ship`

### feature

- Situation: En riktig funktion, med kantfall
- Chain: [clarify], plan, exec-plan, review --fix, ship
- Text: Core Loop för en FIS. Börja med `clarify` om du inte kan räkna upp tre acceptanskriterier, annars med `plan`.
- You get: Koden med sina tester, en pull request som anger avsikt och bevis, och PRD:n om `clarify` kördes.
- Command: `/andthen:plan docs/specs/<feature>/`
- Command: `/andthen:exec-plan docs/specs/<feature>/s01-<name>.md`
- Link: Gå igenom Core Loop → (loop)

### idea

- Situation: En idé utan tre acceptanskriterier
- Chain: clarify, [decide], plan
- Text: `clarify` intervjuar dig i omgångar om luckor, kantfall och omfång och skriver sedan PRD:n. Med `--brief` stannar den vid `intent.md`, ett kort dokument som du kan redigera eller dela före PRD:n.
- You get: `prd.md` i funktionens mapp, eller `intent.md` med `--brief`.
- Command: `/andthen:clarify "<your idea in one line>"`
- Command: `/andthen:clarify --brief "<your idea in one line>"`

### choice

- Situation: Ett tekniskt val som är dyrt att ångra
- Chain: decide, plan
- Text: `decide` räknar upp beslutspunkterna och intervjuar dig om dem som binder mer än en story. Ber du om en jämförelse gör den en viktad avvägning. En fråga som bara mätningar kan avgöra går i stället till `spike`.
- You get: En ADR per beslut i `docs/adrs/`, var och en med en rad i `docs/DECISIONS.md`, och PRD-raderna som den avgör hänvisar nu till den. Inga kodändringar.
- Command: `/andthen:decide docs/specs/<feature>/`
- Command: `/andthen:decide "compare three options for <the choice>"`
- Link: Se det genomarbetade exemplet → (#paths-decide)

### screens

- Situation: Skärmar som inte finns än
- Chain: ui-ux-design, plan, exec-plan, visual-validation
- Text: Designen kommer före specen, så att FIS:en kan peka på wireframes i stället för att hitta på skärmarna. Det genomarbetade exemplet nedan går igenom det för delade listor.
- You get: Wireframes i `docs/wireframes/<feature>/`. För en bred yta ett designsystem i `docs/design-system/`, och sedan klickbara mockups i `docs/mockups/<feature>/`.
- Command: `/andthen:ui-ux-design "wireframe <the screens>, all states" docs/specs/<feature>/prd.md`
- Link: Se det genomarbetade exemplet → (#paths-ui)

### bug

- Situation: En bugg eller ett trasigt bygge
- Chain: triage
- Text: Beskriv symtom, inte lösningar. `triage` hittar grundorsaken, rättar den och kontrollerar rättelsen mot det ursprungliga symtomet. Vill du först ringa in buggen med ett test som fallerar använder du `testing --mode prove-it`.
- You get: En rättelse av grundorsaken. Fällor hamnar i `docs/LEARNINGS.md` och uppskjutna rättelser i `docs/TECH-DEBT-BACKLOG.md`.
- Command: `/andthen:triage "<what you see>"`
- Command: `/andthen:testing --mode prove-it "<the bug>"`

### existing

- Situation: En kodbas som AndThen aldrig har sett
- Chain: init, describe
- Text: `init` skriver Project Document Index, så att varje skill vet var dokumenten finns. `describe` kartlägger koden utan att ändra den.
- You get: Arkitekturdokumentet, `requirements-discovered.md` och `decisions-discovered.md` som teamet granskar, och ett avsnitt Conventions i `CLAUDE.md`.
- Command: `/andthen:init`
- Command: `/andthen:describe`

### domain

- Situation: En ny eller snårig domän
- Chain: domain
- Text: Du är domänexperten. Event storming samlar domänens händelser, aktörer och öppna frågor på en tavla. Domain Map klassificerar domänens delar och drar gränserna mellan dem, och ordlistan låser ett namn per begrepp.
- You get: En event storming-tavla i `docs/models/event-storms/`, `docs/DOMAIN-MAP.md` och `docs/UBIQUITOUS_LANGUAGE.md`.
- Command: `/andthen:domain --mode event-storming "<scope>"`
- Command: `/andthen:domain --mode subdomains,contexts,glossary "<scope>"`

### spike

- Situation: En fråga som bara körande kod kan besvara
- Chain: spike, decide
- Text: Spiken bygger slängkod i ett eget worktree och lämnar sedan ett utlåtande: svaret, belägget och vad det inte täckte. Spikekod mergas aldrig. Utlåtandet blir underlag för `clarify`, `decide` eller `plan`.
- You get: En Spike Verdict i chatten och koden på branchen `spike/<slug>` som belägg.
- Command: `/andthen:spike "<the one question>"`
- Link: Se det genomarbetade exemplet → (#paths-decide)

### pause

- Situation: Arbete som måste avbrytas halvvägs
- Chain: handoff
- Text: `handoff` packar ihop sessionen till ett dokument. Efter `/clear` fortsätter en ny session därifrån, utan att du behöver skriva om något.
- You get: `.agent_temp/handoff/handoff-<UTC-ts>.md`, en lokal fil som inte är privat.
- Command: `/andthen:handoff "next: <the focus>"`
- Prompt: Fortsätt från .agent_temp/handoff/handoff-<UTC-ts>.md

### unsure

- Situation: Jag vet inte var jag ska börja
- Chain: now-what
- Text: `now-what` läser av läget i projektet, till exempel en PRD, en plan eller en granskningsrapport på disk, frågar ”Run it?” och lämnar sedan över till den skill som passar.
- You get: Ett rekommenderat nästa steg, kört eller utskrivet.
- Command: `/andthen:now-what "<what you want, in one sentence>"`

## Vad som blir kvar – Vad varje steg lämnar efter sig

Varje steg skriver något som nästa steg läser. Vissa filer stannar för gott, vissa finns bara på branchen och vissa lämnar aldrig din dator.

Interactive component: en tidslinje med en kolumn per fas och en rad per artefakt. Varje artefakt är en stapel från fasen som skriver den till där den tar slut, formad efter sin Kind: en heldragen stapel som fortsätter in i ”Efter merge” för kept (på `main`, eller på GitHub för pull requesten), en streckad stapel som slutar vid Ship med ett kryss för branch och en prickad grå stapel för local. En förklaring ovanför namnger de tre sorterna. Ett klick på en rad, eller Enter på den, öppnar radens kort under tidslinjen: sökväg, skrivs av, läses av och anteckningen. På en smal skärm scrollar tidslinjen i sidled i sin egen ruta.

| Stage | Label |
| - | - |
| req | Krav |
| design | Design |
| plan | Plan |
| build | Bygge |
| review | Granskning |
| ship | Ship |
| after | Efter merge |

| Artifact | Path | Written by | Read by | From | To | Kind | Note |
| - | - | - | - | - | - | - | - |
| Produktfakta | `docs/PRODUCT.md` | `clarify`, eller den första av `decide`, `plan` och `architecture` som behöver mognadsfas och skala | varje skill som föreslår något | req | after | kept | Ankaret som avgör hur stort det som byggs ska vara: mognadsfas, skala och tekniska icke-mål. |
| PRD | `docs/specs/<feature>/prd.md` | `clarify` | `plan`, `review` (gap och outcome) | req | after | kept | Produktens dokumentation. Den överlever mergen, så att skälen finns kvar även nästa år. När `ship` tar bort planen får den en Shipped-rad. |
| ADR:er och beslut | `docs/adrs/`, `docs/DECISIONS.md` | `decide` | varje skill när en uppgift börjar | design | after | kept | En ADR per dyrt val, med alternativen och vad som krävs för att backa. |
| Ordlista | `docs/UBIQUITOUS_LANGUAGE.md` | `domain --mode glossary`, och `clarify` för fastställda termer | varje skill som namnger saker | design | after | kept | Ett namn per begrepp, och de synonymer som ska undvikas. |
| Wireframes och designsystem | `docs/wireframes/`, `docs/design-system/` | `ui-ux-design` | `plan`, `exec-plan`, `visual-validation` | design | after | kept | FIS:en hänvisar till dem, och de byggda skärmarna kontrolleras mot dem. Designsystemet ligger kvar. `ship` frågar om funktionens mappar med wireframes och mockups ska tas bort, och rekommenderar det när skärmarna är byggda. |
| Underlag för avvägning | `docs/research/<topic>/` | `decide`, för ett omstritt beslut | ADR:en, dina granskare | design | after | kept | Belägget bakom en ADR: utredningen, den viktade matrisen och rekommendationen. Committas tillsammans med ADR:en. |
| Spike | branchen `spike/<slug>` | `spike` | `decide` och `plan`, via utlåtandet | design | after | local | Mergas aldrig. AndThen behåller branchen som belägg. Radera den när utlåtandet är infört i ADR:en. |
| Plan | `docs/specs/<feature>/plan.json` | `plan`, sedan `exec-plan` för varje storys status | `exec-plan`, `review`, `ship` | plan | ship | branch | Stories, deras beroenden och status. `ship` frågar om den ska raderas, och rekommenderar det: en plan gäller en branch. Behålls den får den en `shipped`-markering. |
| FIS | `docs/specs/<feature>/s01-<name>.md` | `plan` | `exec-plan`, `review`, `ship` | plan | ship | branch | Raderas av `ship` när du säger ja, efter att dess Implementation Observations har blivit lärdomar. PR:en och git-historiken behåller den. |
| Kod och tester | källkodsträdet | `exec-plan`, en commit per story plus en eventuell `refactor`-commit. `review --fix` och `implement-fix` committar sina rättelser | `review`, ditt team | build | after | kept | En squash-commit på `main` efter mergen. |
| Granskningsrapport | bredvid den granskade specen, annars `.agent_temp/reviews/` | `review` | `implement-fix`, `ship` | review | after | local | Gitignorerad som standard: en arbetsfil för en körning. Utlåtandet hamnar i PR-texten. |
| Teknisk skuld | `docs/TECH-DEBT-BACKLOG.md` | `review --fix` och `implement-fix` för fynd du skjuter upp, `triage` | den skill som arbetar i det området | review | after | kept | Varje post anger vad som blockerar den. Bara det du godkänner skrivs. |
| Lärdomar | `docs/LEARNINGS.md` | `ship`, från FIS:ens observationer, och även `triage` och `handoff` | varje skill när en uppgift börjar | ship | after | kept | Fällorna som är värda att minnas, en punkt för varje. |
| Pull request | på GitHub | `ship`, när du har sagt ja | dina granskare | ship | after | kept | Avsikt, utfall, beviset för varje utfall, dörrtypen, var granskaren ska läsa noga och en avslutande Ship summary. Vid en squash-merge är det här som berättelsen om FIS:en finns kvar. |
| Överlämning | `.agent_temp/handoff/` | `handoff` | nästa nya session | req | after | local | Skrivs i vilket steg som helst. Ligger under `.agent_temp/` och committas därför aldrig. |

### Efter ship

Component: tre kolumner under tidslinjen (staplade på en telefon), byggda från tabellens Kind: ”Kvar efter mergen” (kept), ”Bara i PR:en och git-historiken” (branch) och ”Lämnar aldrig din dator” (local). Varje kolumn listar sina artefakters namn med sökvägar.

## Efter ship – Vad du kan göra sedan

Branchen är mergad, och `plan.json` är borta om du inte behöll den vid ship. Dokumenten som blev kvar pekar ut vad som kommer härnäst.

Component: vita kort i ett rutnät, tre i bredd (ett på en telefon). Varje kort har en rubrik, texten och sitt kommando, dolt bakom en knapp ”Visa kommando”.

1. **Bygg nästa funktion** · PRD:ns Out of Scope och Open Questions är en färdig backlog. Skapa en ny branch från `main` och välj en punkt. · `/andthen:clarify "<the next idea>"`
2. **Betala av teknisk skuld** · Varje uppskjutet fynd ligger i `docs/TECH-DEBT-BACKLOG.md` tillsammans med det som blockerar det. En post som du kan formulera i en mening är en `implement-fix`. · `/andthen:implement-fix "<an entry from docs/TECH-DEBT-BACKLOG.md>"`
3. **Gör det som ship rekommenderade** · `ship` skriver bara lärdomar och PRD:ns Shipped-rad. Resten rekommenderar den, till exempel en körning av `decide` för en designändring som ingen ADR dokumenterar än. · `/andthen:decide "<the change ship named>"`
4. **Kontrollera utfallet** · Löste funktionen PRD:ns problem för sina användare? Linsen outcome läser PRD:n mot det som byggdes. · `/andthen:review --mode outcome docs/specs/<feature>/prd.md`
5. **Sortera inkommande ärenden** · Nya idéer och buggar samlas i trackern. `tracker triage` sätter etikett på varje ärende och skickar det vidare, och du godkänner allt den skriver. · `/andthen:tracker triage "the ten oldest"`
6. **Sluta för dagen** · Lämna över med nästa fokus, så att morgondagens nya session börjar från filer och inte från minnet. · `/andthen:handoff "next: <the focus>"`

## Genomarbetat exempel – ui-ux-design för delade listor

Samma funktion som i Foundation Lab, men nu designas skärmarna före specen. Delningsdialogen har flera tillstånd som måste bli rätt, så den är värd wireframes. En enda dialog är inte värd ett designsystem.

Component: ett vågrätt flöde av stegen som små piller med pilar (staplade på en telefon), sedan ett block i två kolumner: till vänster de numrerade stegen, vart och ett med sitt kommando dolt bakom en knapp ”Visa kommando”, och till höger filträdet i en mörk ruta med anteckningar i dämpad färg. Under det kommer ”Det här gör du med dem” som numrerade kort, och storlekskontrollen som en dämpad rad.

Flow: prd.md → research → wireframes → [designsystem] → plan → exec-plan → visual-validation

### Steg

1. **Utred flödena om de är oklara.** Svaret kommer i chatten, utan någon fil: jobbet som användaren vill få gjort, två till fem användarresor, en skiss av navigeringen, begränsningar och öppna frågor. Öppna frågor skickar dig tillbaka till `clarify`.
   Command: `/andthen:ui-ux-design "research the shared-lists flows" docs/specs/let-people-share-their-lists/prd.md`
2. **Gör wireframes för varje skärm och tillstånd.** Först skriver den en sidinventering, sedan en HTML-sida i gråskala per skärm och tillstånd, och sist kontrollerar den sidorna i fyra skärmstorlekar.
   Command: `/andthen:ui-ux-design "wireframe the share dialog and the member list, all states" docs/specs/let-people-share-their-lists/prd.md`
3. **Ett designsystem, bara för en bred yta.** Ett helt samarbetsområde med många skärmar är värt tokens och komponentstilar. En enda dialog är det inte. När `DESIGN.md` finns bygger en beställning av mockups klickbara mockups av dess tokens i `docs/mockups/<feature>/`.
   Command: `/andthen:ui-ux-design "create a design system for the collaboration screens" docs/specs/let-people-share-their-lists/prd.md`
4. **Planera utifrån designen.** `ui-ux-design` avslutar med det här kommandot. FIS:en hänvisar till wireframes, så `exec-plan` bygger efter dem.
   Command: `/andthen:plan docs/specs/let-people-share-their-lists/`
5. **Kontrollera de byggda skärmarna.** Ställ in rutinen för skärmbilder en gång och jämför sedan de byggda skärmarna med wireframes.
   Command: `/andthen:visual-validation --mode setup`
   Command: `/andthen:visual-validation "share dialog and member list, mobile and desktop" docs/wireframes/shared-lists/`

### Artefakterna

```
docs/
├── wireframes/shared-lists/   en mapp per funktion
│   ├── index.html              ← open this: every wireframe as a preview
│   ├── page-inventory.md       every screen and state, checked off
│   ├── share-dialog.html       one page per screen…
│   ├── share-dialog-error.html …and one per state
│   ├── member-list-empty.html
│   ├── screenshots/            the check's captures, per viewport
│   └── validation-report.md    what the check found
└── design-system/              only for a broad surface
    ├── DESIGN.md               tokens and the reasons behind them
    ├── tokens.css
    └── showcase.html
```

Note: Filnamnen på wireframes är exempel. Det är sidinventeringen som bestämmer dem.

### Det här gör du med dem

1. **Öppna `docs/wireframes/shared-lists/index.html` i en webbläsare.** Alla skärmar ska finnas där, och alla tillstånd: tom, fel (”no account for that email”), redan delad och laddar.
2. **Jämför med `page-inventory.md`.** Ingen sida får hoppas över för att den ser ”likadan” ut som en annan. Ett tillstånd som saknas är en skärm som agenten hittar på senare.
3. **Committa dem tillsammans med PRD:n.** FIS:en hänvisar till dem medan branchen byggs. Vid leveransen frågar `ship` om funktionens mapp med wireframes ska tas bort, och rekommenderar det när skärmarna är byggda och validerade. Designsystemet ligger kvar.
4. **Planera utifrån dem.** FIS:en anger wireframes som underlaget att bygga efter, och `exec-plan` bygger efter dem i stället för att gissa layouten.
5. **Validera det som byggdes.** `visual-validation` listar varje avvikelse från wireframes innan den ger sitt utlåtande. Fynd med P1 och P2 blockerar, medan P3 rapporteras.

Sizing check: Ett fält som läggs till i ett befintligt formulär är inte värt några wireframes. En dialog med riktiga tillstånd är värd wireframes. En hel yta med många skärmar är värd ett designsystem, och mockups när skärmarna ska godkännas i dess utseende. En API-ändring får ingenting från den här skillen.

## Genomarbetat exempel – decide, architecture och spike för todo-sökning

Nästa funktion i todo-appen: sök bland dina egna todos och bland dem i listor som delas med dig. Hur sökningen ska gå till är ett verkligt val. Alternativen ligger nära varandra, ett av dem bryter mot ett gällande icke-mål, och en av frågorna kan bara körande kod besvara. PRD:n finns redan, i `docs/specs/search-todos/prd.md`.

Component: samma layout som i ui-ux-design-exemplet: flödet som piller, de numrerade stegen med sina kommandon dolda bakom knappar ”Visa kommando” bredvid filträdet, sedan ”Det här gör du med dem” som numrerade kort och storlekskontrollen som en dämpad rad.

Flow: prd.md → architecture → decide → avvägning → spike → ADR → plan

### Steg

1. **Be om råd om strukturen.** `architecture` i rådgivningsläge svarar i chatten och skriver ingenting. Här leder den sökningen genom läskontrollen från ADR-002, så att todos i en delad lista hittas men inga andras. Ett vägskäl som är värt att dokumentera går vidare till `decide`.
   Command: `/andthen:architecture "how should todo search fit with the list access helpers, so shared lists are searched but nobody else's?"`
2. **Rama in beslutet.** `decide` räknar upp beslutspunkterna och sorterar dem. Var åtkomsten kontrolleras är redan avgjort i ADR-002, så `decide` hänvisar dit i stället för att fråga. Hur resultaten rangordnas gäller bara en story och lämnas till `plan`. Hur sökningen ska gå till binder mer än en story, och inget alternativ sticker ut, så den frågan får en viktad avvägning.
   Command: `/andthen:decide "compare three options for searching todos, from docs/specs/search-todos/prd.md"`
3. **Bekräfta kriterierna före utredningen.** Den första kontrollpunkten: beslutets sammanhang, alternativen och en vikt per kriterium. Icke-målet om en enda SQLite i `docs/PRODUCT.md` flaggar en extern sökmotor. Basalternativet, en enkel fråga med `LIKE` mot det som redan finns, är alltid med. Justera vikterna nu, eftersom fel vikter gör utredningen bortkastad.
4. **Gör en spike på det som utredningen inte kan avgöra.** Om FTS5 är inbyggt i den modul `sqlite3` som följer med din Python, och hur snabbt varje alternativ är på 10 000 todos, kan bara körande kod avgöra. `decide` lämnar frågan till `spike`, som bygger i ett eget worktree, committar på en branch `spike/<slug>`, tar bort worktreet och rapporterar en Spike Verdict: frågan, svaret med siffror, hur du kör om det och vad den inte täckte. Utlåtandet förs tillbaka in i avvägningen som belägg. Kör du kommandot fristående ser det ut så här:
   Command: `/andthen:spike "is FTS5 in our Python's sqlite3, and how fast are LIKE and FTS5 on 10,000 todos?"`
5. **Godta rekommendationen och välj status för ADR:en.** Den andra kontrollpunkten: det valda alternativet, vad det ger jämfört med basalternativet, vilka kriterier som avgjorde och vilka som bara skilde alternativ som låg lika. Godta den, finjustera vikterna eller be om en djupare granskning av ett alternativ. Sedan sammanfattar `decide` de avgjorda punkterna och frågar om ADR:en ska föras in som `Accepted` eller `Proposed`.
6. **Behåll resultatet och ta bort spikekoden.** Kontrollera att utlåtandets siffror har kommit med i ADR:en eller i `research.md`. Som standard behåller AndThen spikebranchen som belägg. När resultatet finns i ADR:en bestämmer du själv om den ska raderas. Worktreet är redan borta, och branchen kräver `-D` eftersom den aldrig har mergats.
   Command: `git worktree list`
   Command: `git branch -D spike/<slug>`
7. **Planera utifrån beslutet.** `decide` avslutar med det här kommandot. Avsnittet Architecture Decision i FIS:en hänvisar till den nya ADR:en.
   Command: `/andthen:plan docs/specs/search-todos/`

### Artefakterna

```
docs/
├── adrs/
│   └── ADR-003-<title>.md      the decision and its door type
├── DECISIONS.md                one new Current ADRs row
└── research/
    └── todo-search/
        ├── research.md         findings per option
        ├── tradeoff-matrix.md  a weighted score per criterion
        └── recommendation.md   the report: read it first
.agent_temp/spike/<slug>/       the worktree, removed at the end
spike/<slug>                    the spike code, never merged
```

Note: Namnen är exempel. `decide` väljer ADR:ens titel och ämnesmappen, och `spike` väljer branchens namn. Ett beslut med flera oberoende dimensioner får också `design-tree.md`.

### Det här gör du med dem

1. **Läs `recommendation.md` först.** Avsnittet Executive Summary ger svaret i ett stycke, och How to Read This Report förklarar vikterna. Kontrollera vilka kriterier som avgjorde och vilka som bara skilde alternativ som låg lika.
2. **Läs raden Reversal och avsnittet Alternatives i ADR:en.** Ett beslut som inte går att backa (en envägsdörr) ska läsas långsamt. Både basalternativet och den flaggade externa sökmotorn finns med, var och en med skälet till att den förlorade.
3. **Gör spikeresultatet beständigt.** Siffrorna i Spike Verdict och kommandot för att köra om den hör hemma under References i ADR:en eller i `research.md`. Dokumentera beslutet och belägget för det, aldrig koden.
4. **Ta bort spikekoden.** När utlåtandet är dokumenterat raderar du branchen `spike/<slug>`. Spikekod mergas eller återanvänds aldrig: den riktiga implementationen skrivs från grunden utifrån FIS:en.
5. **Committa beslutet tillsammans med PRD:n.** `git add docs` tar med ADR:en, `DECISIONS.md` och utredningsmappen. `plan` och alla senare skills läser dem via indexet.

Sizing check: Ligger alternativen nära varandra och går beslutet att backa (en tvåvägsdörr) behövs ingen avvägning: välj ett. Ett bärande val utan något verkligt alternativ blir en rad under Still Current i `DECISIONS.md`. Ett omstritt val får avvägningen och en ADR. En fråga som bara mätningar kan avgöra får en spike, och bara då.

## Härnäst

Component: en rad knappar som byter flik. Den första är ifylld, de andra har kontur.

- Gör Foundation Lab → (lab)
- Tillbaka till Core Loop → (loop)
- Utforska skills → (skills)

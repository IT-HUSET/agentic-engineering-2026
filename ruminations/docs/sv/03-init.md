---
title: AndThen:init
tab: Init
token: init
order: 3
depends_on: [shared/skills.md]
---

# AndThen:init

Eyebrow: andthen:init

## Vad andthen:init lägger i Claudes minne

Component: ”andthen:init” i rubriken sätts i accentfärgen.

Init körs en gång per projekt som en kort process: den tar reda på vad som finns, skriver standardfilerna och erbjuder sedan tillval som du väljer. Nedan ser du processen steg för steg, med vad varje steg läser och skriver. Var filerna hamnar bland resten av Claudes minne visar fliken Claudes minne.

### Grundidén

`CLAUDE.md` är den enda fil som init alltid lägger i Claudes minne i varje session, och därför lämnar init ingen TODO kvar i den. Andra dokument får en rad i dess Project Document Index, och Claude öppnar dem bara när en uppgift matchar.

## Processen – Så går andthen:init till, steg för steg

Init körs som en kort process: den tar reda på vad projektet har, skriver standardfilerna och erbjuder sedan tillval som du väljer. Klicka på en symbol för att se vad den läser eller skriver, med ett exempel.

Interactive component: ett processdiagram på 760 × 590 i BPMN-liknande stil, över hela bredden, med detaljkortet under, också i full bredd. På en bred skärm lägger kortet exemplet bredvid texten. Utan exempel tar texten hela kortet. Tre radrubriker: Läser · Process · Skriver. Det som läses är dataobjekt (en sida med vikt hörn) som är kopplade till ”1 Inventera” med en prickad association. Det streckade objektet ”agents/” är kopplat till ”3 Erbjud tillval”. Processen går från vänster till höger: en tunn startcirkel, rundade uppgifter, romber med ett × som gateways, en användaruppgift med en personikon och en tjock slutcirkel, sammanbundna med heldragna sekvenspilar. Den första gatewayen märker sina grenar ”ingen” (uppåt) och ”finns” (nedåt), den andra ”tomt” (uppåt) och ”filer” (åt höger). Det som skrivs är dataobjekt i två band: ALLTID ELLER SOM STANDARD (vanliga), kopplat till ”2b” med en prickad linje märkt ”från 2a eller 2b”, och BARA OM DU TACKAR JA (lavender, streckade objekt), kopplat till ”3 Erbjud tillval”. En kryssruta, ”Dölj erbjudanden”, tonar ned de streckade objekten. Kortet visar Kind som eyebrow, Label som rubrik, Path i monospace, Text och, när det finns ett, Example i en mörk kodruta. Kortets tint: det som läses cream, händelser och gateways teal, steg rust, ditt svar teal, det som skrivs green, erbjudanden lavender. Börjar på s3.

Hint below 960 px: Scrolla i sidled för att se hela diagrammet.

Legend: Start · Uppgift · Du svarar · Gateway: en väg · Slut · Dataobjekt · Bara om du tackar ja (streckad)

Source: Bygger på skillen init i AndThen {andthen_version}.

| Id | Label | Subtitle | Shape | Box | Border |
| - | - | - | - | - | - |
| r1 | CLAUDE.md | även AGENTS.md | data | 24, 32, 108, 52 | solid |
| r2 | docs/ | och riktlinjer | data | 146, 32, 108, 52 | solid |
| r3 | README | och manifest | data | 268, 32, 108, 52 | solid |
| r4 | Byggskript | Makefile, CI | data | 390, 32, 108, 52 | solid |
| r5 | Tester, UI | och workspace | data | 512, 32, 108, 52 | solid |
| r6 | agents/ | roller som finns | data | 634, 32, 108, 52 | dashed |
| start | /andthen:init |  | start | 52, 238, 15 | solid |
| s1 | 1 Inventera |  | task | 84, 214, 96, 48 | solid |
| g1 | Instruktionsfil? |  | gateway | 224, 238, 20 | solid |
| g2 | Tomt repo? |  | gateway | 278, 174, 18 | solid |
| ask | Vad är det? |  | user | 320, 104, 128, 34 | solid |
| s2a | 2a Från mall |  | task | 320, 154, 128, 40 | solid |
| s2b | 2b Komplettera |  | task | 320, 286, 128, 40 | solid |
| g3 | Vägarna möts |  | gateway | 492, 238, 20 | solid |
| s3 | 3 Erbjud tillval |  | task | 532, 214, 112, 48 | solid |
| end | Sammanfattning | Nästa: clarify | end | 700, 238, 15 | solid |
| w1 | CLAUDE.md | Index och regler | data | 28, 376, 106, 52 | solid |
| w7 | Dev-kommandon | fast och full | data | 142, 376, 106, 52 | solid |
| w9 | .gitignore | två rader | data | 256, 376, 106, 52 | solid |
| w5 | Rollagenter | modell och effort | data | 392, 376, 108, 52 | dashed |
| w2 | Kritiska regler | i CLAUDE.md | data | 512, 376, 108, 52 | dashed |
| w4 | Svarsstil | settings.json | data | 632, 376, 108, 52 | dashed |
| w3 | Egna regler | ~/.claude | data | 392, 442, 108, 52 | dashed |
| w8 | Fler dokument | välj bland sex | data | 512, 442, 108, 52 | dashed |
| w6 | Delprojekt | för ett monorepo | data | 632, 442, 108, 52 | dashed |
| w10 | Nästa skills | tre kommandon | data | 392, 508, 108, 52 | dashed |

### Detaljer

Format: id · Kind · Path · Text, sedan ett valfritt Example. Kortet visar Label som rubrik.

- **start** · Start · `/andthen:init [project name]` · Du kör den en gång per projekt, från projektets rotmapp. Utan namn tar den mappens eller manifestets namn. Den skriver aldrig över något: ditt innehåll behålls, och den ersätter bara det du väljer.
  Example:
  ```
  /andthen:init
  /andthen:init "todo-app"
  ```
- **r1** · Läser · `./CLAUDE.md, ./AGENTS.md` · Filen avgör vägen vid den första gatewayen. Saknas en instruktionsfil skapas en ny från mallen. Finns det redan en kompletteras den, och ditt innehåll behålls.
- **r2** · Läser · `docs/, docs/guidelines/` · Varje AndThen-dokument som redan finns där får en rad i Project Document Index, med den sökväg där det hittades.
  Example:
  ```
  found   docs/DECISIONS.md
  writes  - **Decisions** – `docs/DECISIONS.md`: ADR index and Still Current notes. …
  ```
- **r3** · Läser · `README.md, pyproject.toml, package.json och liknande` · Projektnamnet och teknikstacken fyller i Project Overview. Bara i ett tomt repo, utan manifest, README eller källfil, frågar init dig vad projektet är.
  Example:
  ```
  pyproject.toml  name "todo-app"
                  "Modern todo application with FastAPI, HTMX, and Shoelace"
                  Python >= 3.11, FastAPI, SQLAlchemy, pytest
  ```
- **r4** · Läser · `Makefile, justfile, CI-arbetsflödet, manifestets skript` · Här hittar init kommandona fast, full och run one test, som blir startinnehållet i dokumentet Key Dev Commands.
  Example:
  ```
  pyproject.toml has pytest  →  fast  uv run pytest -x -q
                                full  uv run pytest
  ```
- **r5** · Läser · `en testmapp eller ett testskript · ett UI-ramverk, mallar eller en dev-server · en workspace-konfiguration` · Det som hittas här avgör vilka tillval du erbjuds: en teststrategi, visual-validation i setup-läge eller delprojektfiler för ett monorepo.
  Example:
  ```
  tests/                 →  offer /andthen:testing --mode strategy
  src/app/templates/     →  offer /andthen:visual-validation --mode setup
  ```
- **r6** · Läser · bara för ett erbjudande · `.claude/agents/, ~/.claude/agents/` · Init läser dem bara om du tackar ja till erbjudandet om rollagenter: den jämför det som är installerat med sina mallar och frågar innan den ersätter en fil.
- **s1** · Steg · `Steg 1` · Init går igenom projektet en gång. Steget frågar inget och skriver inget: det som hittas avgör vägen och tillvalen.
- **g1** · Gateway · `ingen CLAUDE.md eller AGENTS.md → 2a · en finns → 2b` · Exakt en väg tas. Ett projekt som redan har gått igenom init tar alltid 2b, så det är säkert att köra init igen. Vad den gör då står under diagrammet.
- **g2** · Gateway · `inget manifest, ingen README eller källfil?` · Ett tomt repo får frågan först. I alla andra fall hämtar init Project Overview från README, manifestet och koden, och frågar inget.
- **ask** · Du svarar · `en fråga, bara i ett tomt repo` · Innan init skriver något frågar den, med en enda fråga, vad projektet är. Ditt svar fyller i Project Overview.
  Example:
  ```
  What is this project?
  > A todo app for the course: FastAPI, HTMX and SQLite
  ```
- **s2a** · Steg · `Steg 2a: ingen instruktionsfil` · Init skriver instruktionsfilen från AndThens mall, lägger till en rad i indexet för varje AndThen-dokument som hittas, löser eller tar bort varje TODO och lägger till de två raderna i .gitignore. Finns det ett manifest fyller en subagent i Key Dev Commands. Inget annat skapas.
  Example:
  ```
  Claude Code only   →  CLAUDE.md
  Codex only         →  AGENTS.md
  both, or unclear   →  AGENTS.md, and a CLAUDE.md whose first line is @AGENTS.md
  ```
- **s2b** · Steg · `Steg 2b: en instruktionsfil finns` · Init behåller ditt innehåll och lägger bara till det som saknas, utan att fråga: indexrader för dokument som inte står med, indexets inledande text, en tom Project Overview, avsnitt som saknas, Key Dev Commands och raderna i .gitignore. Två ändringar erbjuds bara, i steg 3: att göra om CLAUDE.md och AGENTS.md till den gemensamma layouten och att lägga till den motsvarande filen när den saknas.
- **g3** · Gateway · `2a och 2b möts` · Oavsett vilken väg som togs går init vidare till tillvalen.
- **s3** · Steg · `Steg 3: erbjud resten` · ”Erbjud resten” betyder tillvalen. Efter standardfilerna listar init de tillval som passar ditt projekt, ett per rad, och gör bara det du tackar ja till. Det du tackar ja till gör den direkt. Tackar du nej till de kritiska reglerna skrivs en markering om att du hoppade över dem, så att du inte får frågan igen. Hoppar du över ett tillval utan att svara skrivs inget, och nästa körning erbjuder det igen.
  Example (formen, inte exakt ordalydelse):
  ```
  Offers
  - Role agents oracle, implementer, reviewer, worker – pin model and effort?
  - Critical rules – adopt into CLAUDE.md?
  - Documents – Product, Decisions, Learnings, Tech Debt, Roadmap, Ubiquitous Language?
  - /andthen:testing --mode strategy – a test suite was found
  - /andthen:visual-validation --mode setup – a served UI was found
  ```
- **end** · Slut · `den avslutande sammanfattningen` · Sammanfattningen listar bara det som den här körningen skapade eller ändrade, en rad per fil med dess syfte, sedan erbjudandena och hur du committar granskningsrapporter. Den avslutas med att rekommendera clarify som första steg.
  Example:
  ```
  Created  CLAUDE.md                         instructions and the Document Index
  Created  docs/KEY_DEVELOPMENT_COMMANDS.md  fast, full and run-one-test commands
  Changed  .gitignore                        .agent_temp/ and review reports
  Next: /andthen:clarify
  ```
- **w1** · Skriver · alltid · `./CLAUDE.md, eller AGENTS.md plus en CLAUDE.md som importerar den` · Project Overview, Project Document Index, riktlinjer och regler. Claude Code läser in filen i början av varje session, och därför lämnar init ingen TODO kvar i den. De andra dokumenten får en rad i indexet och läses bara när en uppgift matchar.
  Example:
  ```
  ## Project Document Index

  Documents here are read whole when their trigger matches, so keep them short …

  - **Key Dev Commands** – `docs/KEY_DEVELOPMENT_COMMANDS.md`: dev, test, build, deploy commands. Read before running verification; update when a command changes.
  - **Agent Temp** – `.agent_temp/`: scratch workspace for reviews, research, and QA; never ship from it.
  ```
- **w7** · Skriver · som standard · `docs/KEY_DEVELOPMENT_COMMANDS.md` · En subagent skapar filen när det finns ett manifest, så att mallarna hålls utanför huvudkontexten. Claude läser den när indexet pekar dit, före verifiering. exec-plan kör fast en gång per story och full i slutet.
  Example:
  ```
  | fast         | uv run pytest -x -q             | Once per story |
  | full         | uv run pytest                   | End of run     |
  | run one test | uv run pytest {file}::{test}    | One test       |
  ```
- **w9** · Skriver · alltid · `.gitignore` · Inte minne: filen håller tillfälliga filer och granskningsrapporter utanför git. Ta bort den andra raden om du vill committa granskningsrapporter.
  Example:
  ```
  .agent_temp/
  *-andthen-*-review-*.md
  ```
- **w5** · Skriver · om du tackar ja · `.claude/agents/ för teamet, eller ~/.claude/agents/ för dig` · oracle, implementer, reviewer och worker, som låser modell och effort för varje subagentnivå. De läses in vid sessionsstart och gäller alltså från nästa session. Utan init kan du kopiera dem från pluginets mallar: fliken Anatomi visar hur, och vilka standardvärdena är.
  Example:
  ```
  ---
  name: reviewer
  model: opus
  effort: medium
  ---
  ```
- **w2** · Skriver · om du tackar ja · `# Critical Rules and Guardrails i rotens instruktionsfil` · AndThens skyddsregler, införda i projektfilen så att de följer med repot in i CI och containrar. Tackar du nej skrivs en markering om det i stället, och du får inte frågan igen.
  Example:
  ```
  # Critical Rules and Guardrails
  …
  or, when you decline:
  <!-- AndThen critical rules: skipped -->
  ```
- **w4** · Skriver · om du ber om det · `outputStyle i ~/.claude/settings.json` · Korta, raka och kritiska svar, med svaret först. Init lägger in inställningen och behåller dina övriga nycklar. Den gäller från nästa session.
  Example:
  ```
  "outputStyle": "andthen:concise-critical"
  ```
- **w3** · Skriver · om du ber om det · `~/.claude/CLAUDE.md` · Samma skyddsregler för dig personligen, i alla projekt på den här datorn. Init skriver den bara när du ber om det.
- **w8** · Skriver · om du tackar ja · `docs/PRODUCT.md, DECISIONS.md, LEARNINGS.md, TECH-DEBT-BACKLOG.md, ROADMAP.md, UBIQUITOUS_LANGUAGE.md` · Du väljer från en enda rad. Varje dokument du väljer får en fil från sin mall och en rad i indexet. Ett dokument du hoppar över skapas senare av den första skill som skriver till det.
- **w6** · Skriver · om du tackar ja · `<sub-project>/CLAUDE.md` · För ett monorepo: en lätt instruktionsfil per delprojekt, med dess kommandon och de konventioner som skiljer sig från roten. Claude Code läser den när den arbetar i den mappen.
- **w10** · Kör sedan · om du tackar ja · `tre skills, erbjudna som kommandon` · Tre tillval kör en annan skill i stället för att skriva en fil: describe för en befintlig kodbas utan Architecture-dokument, testing i strategiläge när det finns en testsvit och visual-validation i setup-läge när projektet har ett UI som serveras.
  Example:
  ```
  /andthen:describe
  /andthen:testing --mode strategy
  /andthen:visual-validation --mode setup
  ```

## Köra igen – Vad händer om du kör andthen:init igen

Du kan köra init igen utan risk. Nu finns det en instruktionsfil, så init tar alltid väg 2b, och den skriver aldrig över ditt innehåll. Kör den igen efter en uppgradering av AndThen eller när du har lagt till dokument för hand, så fyller den i det som saknas. Vad som händer beror på vad det gäller.

Component: fyra kolumner under processen (två på en mellanstor skärm, en på en telefon), i samma stil som kolumnerna efter ship på fliken Vägar. Varje kolumn har en eyebrow, en rubrik och en lista där varje rad är ett namn med en kort förklaring. Under kolumnerna står undantaget som en nedtonad rad.

### Lämnas som det är

- Eyebrow: Rörs aldrig
- Tint: green
- **Din text** · allt du har skrivit i `CLAUDE.md` och `AGENTS.md`
- **Dokument som finns** · behåller sitt innehåll och får som mest en rad i indexet
- **Din svarsstil** · en befintlig `outputStyle` ersätts aldrig
- **En symlänkad instruktionsfil** · init rapporterar den men skriver aldrig genom länken

### Fylls i utan att fråga

- Eyebrow: Steg 2b
- Tint: teal
- **Indexrader** · för AndThen-dokument som inte står med än
- **Indexets inledning** · de inledande meningarna, som stäms av mot mallen
- **Project Overview** · bara när den är tom eller en TODO
- **Avsnitt som saknas** · läggs till i rotens instruktionsfil
- **Key Dev Commands** · när det finns ett manifest men inget dokument
- **.gitignore** · de två raderna, om de saknas

### Frågar först

- Eyebrow: Steg 3
- Tint: lav
- **Rollagenter** · init namnger varje fil som skiljer sig från mallen innan den ersätts
- **Kritiska regler** · en befintlig policy ersätts bara om du ber om en uppdatering, och du ser diffen först
- **CLAUDE.md och AGENTS.md** · att göra om båda till den gemensamma layouten eller att lägga till den som saknas

### Erbjuds igen

- Eyebrow: Nästa körning
- Tint: cream
- **Tillval du hoppade över** · ett erbjudande du inte svarade på kommer tillbaka
- **Dokument som inte finns än** · på samma rad att välja från
- **Skillerbjudandena** · describe, testing och visual-validation, så länge det som utlöser dem finns kvar

Undantag: tackar du nej till de kritiska reglerna skrivs markeringen `<!-- AndThen critical rules: skipped -->`, och init frågar inte igen. Ta bort markeringen om du vill få frågan igen.

## Nästa

Component: en rad med knappar som byter flik. Den första är fylld, den andra har bara kontur.

- Se var varje del av AndThen finns → (anatomy)
- Se var Claudes minne finns → (memory)

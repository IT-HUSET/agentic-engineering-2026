# Ruminations

Egna fördjupningar och visualiseringar under kursen Agentic Engineering 2026. Den första är **AndThen Guide**, en interaktiv sida om AndThen: kursens mål, installation, hur `andthen:init` går till, en karta över alla skills, Core Loop från idé till pull request, Foundation Lab steg för steg och var AndThen Studio hjälper till, och på en sidoflik var Claudes minne finns.

Single source of truth är markdown-filerna i `docs/`. HTML-sidorna i `html/` är genererade vyer av dem och redigeras aldrig för hand.

Guiden finns på engelska och svenska. Den svenska versionen har egna md-filer i `docs/sv/` och en egen sida, `html/andthen-guide.sv.html`. En växlare uppe till höger (EN/SV) byter mellan sidorna och behåller fliken.

Ingång: `html/andthen-guide.html`, eller den publicerade sidan [AndThen Guide](https://claude.ai/artifact/HAVpWj74fHd8ZMU5xyUJyT).

## Struktur

```
ruminations/
├── README.md                     ← den här filen
├── docs/                         ← SSOT (markdown)
│   ├── 00-guide.md               Sidans ram: titel, version, artifact-URL, flikordning, sidhuvud och sidfot
│   ├── 01-start.md               Flik Start · målet med kursen och todo-appen
│   ├── 02-setup.md               Flik Setup · installation och AndThen Studio
│   ├── 03-init.md                Flik Init · processdiagrammet för andthen:init
│   ├── 04-skills.md              Flik Skills · skill-kartan och översiktstabellen
│   ├── 05-anatomy.md             Flik Anatomy · kartan över tre platser, var man ställer in vad, modellerna
│   ├── 06-core-loop.md           Flik Core Loop · vägval, steg, produkt och PRD, plan, stories och FIS, parallella stories och regler
│   ├── 07-paths.md               Flik Paths · vägval, vad som blir kvar, efter ship, två exempel
│   ├── 08-foundation-lab.md      Flik Foundation Lab · labbets sju steg F1–F7 med checklistor
│   ├── 09-studio.md              Flik Studio · start, vyerna, AI-åtgärder och regler
│   ├── 10-memory.md              Flik Claude’s memory · sidoflik om Claude Codes minne: minnesdiagrammet och /memory
│   ├── sv/                       Svenska versionen: samma filer på svenska, plus TERMS.md (låsta ordval)
│   │                             08-foundation-lab är delad i .part1.md (steg F1–F7) och .part2.md (exemplen)
│   └── shared/
│       ├── skills.md             Alla skills: grupp, roll, kartposition, texter, kommando, samarbeten, resultat
│       └── icons.md              Ikonerna för resultat och artefakter (SVG-innehåll)
├── assets/                       ← källfiler, inbäddas i HTML
│   ├── logo-black.png            IT-HUSETs ordmärke för ljus bakgrund
│   ├── logo-white.png            IT-HUSETs ordmärke för mörk bakgrund
│   ├── todo-app-work-tasks.png   Skärmbild av kursens todo-app, listan Work Tasks
│   └── todo-app-personal.png     Skärmbild av kursens todo-app, listan Personal
└── html/
    ├── andthen-guide.html        AndThen Guide (genererad, engelska)
    └── andthen-guide.sv.html     AndThen-guiden (genererad, svenska)
```

## Leverabler

| Sida | Källa | HTML | Artifact | Status |
| - | - | - | - | - |
| AndThen Guide | `docs/00-guide.md` + `01`–`10` + `shared/` | `html/andthen-guide.html` | [AndThen Guide](https://claude.ai/artifact/HAVpWj74fHd8ZMU5xyUJyT) | v1.57 · publicerad |
| AndThen-guiden (svenska) | `docs/sv/` | `html/andthen-guide.sv.html` | samma artifact, fil `andthen-guide.sv.html` | v1.57 · publicerad |

Publiceras en sida som artifact skrivs URL:en in i ramfilens frontmatter (`artifact`) och i tabellen ovan. Därefter republiceras alltid mot samma URL. Artifacten har den engelska sidan som huvudsida och båda sidorna som filer (`andthen-guide.html` och `andthen-guide.sv.html`), så att växlarens länkar fungerar åt båda hållen.

## Arbetsflöde

1. **Ändra i `docs/` och `docs/sv/`.** En ändring görs på båda språken i samma omgång, med ordvalen i `docs/sv/TERMS.md` och skill `it-huset-skills:ith-svenska` för svenskan. Ett värde som förekommer i flera flikar ändras i den gemensamma filen: allt om en skill (text, kommando, resultat, kartposition) i `shared/skills.md`, ikoner i `shared/icons.md`. Varje flik anger i frontmatter vilka gemensamma filer den beror på (`depends_on`).
2. **Stega version och datum** i `00-guide.md` och `sv/00-guide.md`.
3. **Regenerera HTML.** Be Claude bygga om `html/andthen-guide.html` från `docs/` och `html/andthen-guide.sv.html` från `docs/sv/` enligt kontraktet nedan. Republicera mot samma artifact-URL.
4. **Rör aldrig HTML för hand.** Hittas ett fel på sidan: rätta i md och regenerera.
5. **Ny AndThen-version.** Stäm av `shared/skills.md` mot `plugin/skills/*/SKILL.md` i den installerade AndThen och uppdatera `andthen_version`. Antalet skills räknas ur filen.

## Regenereringskontrakt (vad HTML-sidan ska uppfylla)

Ett eventuellt framtida byggskript ska implementera samma kontrakt.

### Profil och språk

- IT-HUSETs designsystem (skill `it-huset-skills:ith-design-system`). Typsnitt Outfit (rubriker, eyebrows), Inter (brödtext) och JetBrains Mono (kod, filnamn, kommandon) från Google Fonts. Inga andra externa beroenden.
- Bara färger ur designsystemets tokens. Cream som sidbakgrund, vita kort, skogsgrön sidfot. Tint-namnen i md (`rust`, `red`, `cream`, `green`, `teal`, `lav`) betyder designsystemets mjuka bakgrund plus dess djupa accent.
- Ljust och mörkt läge. Alla färger definieras som tokens på `:root` och definieras om för mörkt läge både under `prefers-color-scheme: dark` och `[data-theme="dark"]`.
- Logotyper och bilder bäddas in som PNG data-URI från `assets/`, så att sidan är en fristående fil som fungerar lokalt och som artifact. En rad `- Image: <sökväg> · <bildtext> · <alt-text>` i md blir en bild med bildtext och alt-text.
- Två sidor med samma struktur, samma skript och samma länktoken: `andthen-guide.html` på engelska (`<html lang="en">`) från `docs/` och `andthen-guide.sv.html` på svenska (`<html lang="sv">`) från `docs/sv/`. Var sida har texten i den ordalydelse som står i dess md. Kommandon, sökvägar, kod och exempelinnehåll i filer är desamma på båda sidorna.
- Språkväxlaren i sidhuvudet (EN/SV) länkar till den andra sidan med den öppna flikens token, sparar valet i localStorage (`andthen-guide-lang`) och öppnar det sparade språket vid nästa besök. Foundation Labs kryss delar nyckel mellan språken.
- Varumärket skrivs alltid IT-HUSET. Huvudflödet heter alltid Core Loop, och dess flik heter Core Loop, på båda språken. Flikarnas etiketter saknar ordet AndThen: det står en gång, som en etikett före flikraden, och gäller alla flikar utom den sista. Sidofliken Claudes minne handlar om Claude Code, står sist och skiljs från AndThen-flikarna med en tunn lodrät linje.
- Sidans innehåll är högst 1360 px brett. Flikarnas huvudrubriker (`h1`) och sektionsrubriker (`h2`) har ingen egen maxbredd. De bryts bara när de inte ryms, och då fyller första raden bredden; bara ett ensamt sista ord undviks (`text-wrap: pretty`, inte `balance`). Huvudrubrikerna är högst 56 px stora (3.5rem), Start-flikens högst 64 px (4rem), så att de ryms på en rad från 1280 px bredd.
- Ingresser och brödtext är högst 85 tecken breda (`--measure: 85ch`), så att texten använder bredden men raderna går att läsa.
- Sidan fungerar i 375 px bredd utan vågrät scroll. Breda diagram och tabeller scrollar i sidled i sin egen ruta.

### Sidans ram

- En HTML-sida med en flik per fil i `tabs` (frontmatter i `00-guide.md`). Fliketiketten är filens `tab`, länktoken är `token`.
- Sidhuvud med logotyp och metatext, flikrad, sidfot enligt `00-guide.md`.

### Tolkning av md

- `#`-rubriken är filens namn och visas inte. `##`-rubriker blir sektioner. Text före tankstrecket blir eyebrow och texten efter blir rubrik, om inte en egen rad `Eyebrow:` anges. Första stycket blir sektionens ingress.
- Rader som börjar med `Component:` eller `Interactive component:` beskriver hur innehållet ska visas och visas inte som text. Detsamma gäller `Legend:`, `Source:`, `Note`, `Button:` och `Command:`, som blir sina respektive element.
- `{skill_count}` ersätts med antalet skills i `shared/skills.md`. `{andthen_version}` ersätts med `andthen_version` därifrån. Siffrorna skrivs aldrig in för hand.
- Markdown-länkar blir länkar. Externa länkar öppnas i ny flik (`target="_blank" rel="noopener"`).
- `**fet**` blir fetstil och `` `kod` `` blir kod i HTML.

### Data som tolkas strukturerat

- **Skills** (`shared/skills.md`): ett `###`-block per skill med fälten Group, Role, Optional, Map, Document, Summary, When, Reads, Command, Works with, Result och Tag. Gruppordningen och gruppernas etiketter och tints står i tabellen Groups.
- **Skill-kartan** (`04-skills.md`): tabellerna Bands och Arrows. Skill-rutornas läge kommer från Map i `shared/skills.md`.
- **Core Loop** (`06-core-loop.md`): tabellen över vägar och ett `###`-block per steg. `Command (several):` och `Note (several):` gäller bara den vägen; en Note blir en nedtonad ruta under When, med den fetstilta inledningen som etikett. `Studio:` blir en lavendelremsa i stegkortet med länk till fliken AndThen Studio. Stegets resultat och tagg hämtas från skillens Result och Tag. Avsnittet om produkt och PRD har två `####`-kort (Eyebrow, Tint, Arrow, Text, Row med två fält och en Note) som ritas bredvid varandra med en pil, i samma stil som korten om plan, stories och FIS, följt av hur clarify väljer nivå och en tumregel. Källan är `skills/clarify/SKILL.md` och `references/product-template.md` i AndThen 1.1.0. Avsnittet om plan, stories och FIS har tre `####`-kort (Eyebrow, Tint, Arrow, Text, Row med tre fält, i plan.json fyra med status, och en eller flera Note) som ritas som ett diagram med pilar, fyra regler för slices som kort och ett namntips. Källan är `references/plan-schema.md`, `skills/plan/SKILL.md` steg 3, `skills/plan/references/breakdown.md` och `fis-template.md` i AndThen 1.1.0. Avsnittet om parallella stories har exempelplanen (Story, Name, Depends on), banorna (kommando · stories med `→`, `[a, b]` för samtidiga och `merge` · förklaring), tre kort och förutsättningarna. Källan är `skills/plan/references/breakdown.md` och `skills/exec-plan/references/plan-run.md` samt `story-worktrees.md` i AndThen 1.1.0.
- **Init-diagrammet** (`03-init.md`): processdiagrammet för `init` i BPMN-lik stil (tabell med Id, Label, Subtitle, Shape – start, end, task, user, gateway eller data – Box och Border, och detaljer med Kind, Path, Text och ett valfritt Example i kodblock).
- **Köra init igen** (`03-init.md`): fyra `###`-block under processen (Eyebrow, Tint och rader med namn · förklaring) som ritas som kolumner i samma stil som kolumnerna efter ship, plus en rad med undantaget. Källan är `skills/init/SKILL.md`, `references/partial-setup.md` och `references/offers.md` i AndThen 1.1.0.
- **Claudes minne** (`10-memory.md`): minnesdiagrammets nodtabell (id, etikett, undertext, läge, ram, märke) och detaljlista, samt måltabellen för `/memory`.
- **Installationsstegen** (`02-setup.md`): de numrerade stegen med sina villkor och kommandon.
- **AndThen Paths** (`07-paths.md`): ett `###`-block per situation med Situation, Chain (en skill inom hakparentes är valfri), Text, You get, Command, Prompt och Link (flik-token eller #ankare), artefakttabellen (Stage, From, To och Kind: kept, branch eller local) som ritas som tidslinje och sammanfattas i tre kolumner efter ship, korten efter ship (titel · text · kommando) och de två exemplen, ui-ux-design samt decide, architecture och spike, var och ett med flöde, steg, filträd och "What you do with them". Källan är AndThen 1.1.0:s `plugin/README.md` och `COOKBOOK.md` samt `labs/x2-ui-ux.md`; stäm av mot dem vid en ny AndThen-version.
- **Foundation Lab** (`08-foundation-lab.md`): ett `###`-block per steg med Tint, Skills, Input, Output (ikon · titel · text), Command (med en valfri etikett inom parentes), Prompt (text man skriver till Claude Code, visas utan kopieringsknapp, med etikett inom parentes), Example (en länk till ett genomarbetat exempel, med dialogens id inom parentes), Studio command och Studio (en valfri ruta om AndThen Studio i stegkortet), Steps, Verify och Sizing check. Ett genomarbetat exempel är en egen `##`-sektion som visas i en dialog. Källan är `labs/foundation.md` i repot; ändras labbet stäms filen av mot den.
- **AndThen Studio** (`09-studio.md`): startstegen, vytabellen (stegchippen F1–F7 växlar till Foundation Lab och väljer steget), de tre AI-åtgärderna och felsökningsfrågorna. Källan är README i `IT-HUSET/andthen-studio`; stäm av filen mot den vid en ny Studio-release.
- **AndThen Anatomy** (`05-anatomy.md`): ett `###`-block per plats (Eyebrow, Title, Root och en tabell med Node, Level, What it is, Written by, When you touch it) som ritas som klickbara träd med ett detaljkort, tabellen "Where do I set…?" (Question, Where, How), rolltabellen (Role, Model, Effort, Used for) och installationsstegen. Källan är AndThen 1.1.0:s `plugin/README.md`, `skills/init/references/offers.md` och mallarna under `skills/init/templates/`; stäm av vid en ny AndThen-version, särskilt rollagenternas `model` och `effort`.
- **Ikoner** (`shared/icons.md`): SVG-innehåll per ikonnamn.

### Interaktiva komponenter

- **Skill-karta:** klickbara SVG-noder, markering av valt skill och dess samarbeten, detaljkort under kartan och översiktstabell som väljer på kartan. Tangentbord: Tab och Enter.
- **Core Loop:** vägval, stegrad med piltangenter, stegkort med Föregående och Nästa och kopieringsknappar.
- **Init:** processdiagrammet, klickbart med ett detaljkort som visar ett exempel när det finns, och "Hide offers".
- **Claudes minne:** minnesdiagrammet, klickbart med sticky detaljkort, och målväljaren för `/memory`.
- **Start:** skärmbilderna på todo-appen öppnas i full storlek vid klick.
- **Setup:** installationsstegen byggs om när någon av de två kryssrutorna ändras (redan installerat; tillagt från en tagg eller @develop). Studio-kortet växlar installationskommando mellan macOS / Linux och Windows.
- **AndThen Paths:** situationslistan väljer kort med piltangenter, tidslinjens rader öppnar ett detaljkort med klick eller Enter, och ankarknapparna scrollar till sektionerna.
- **AndThen Anatomy:** trädens noder väljs med klick eller piltangenter upp och ned och visar sitt detaljkort, och ankarknapparna scrollar till sektionerna.
- **Foundation Lab:** stegrad F1–F7 med piltangenter, stegkort med Föregående och Nästa, kopieringsknappar och Verify-kryssrutor som sparas i webbläsaren (localStorage) med en räknare och en Återställ-knapp.
- Alla kommandorutor (den mörka rutan med Copy-knapp) är dolda från början bakom en knapp "Show command" med terminalikon, som blir "Hide command" när rutan är öppen. En öppnad ruta förblir öppen när kortet byggs om, till exempel vid byte av steg eller val. Exemplens kodblock i dialogerna påverkas inte.
- Alla kopieringsknappar använder urklipp och markerar texten om urklipp inte är tillgängligt.

### Kontroll efter regenerering

- Inga konsolfel och alla skript tolkas utan fel.
- Varje text och varje kommando i md finns på sidan, och sidan har inga texter som saknas i md. Gäller båda språken.
- Den svenska sidan har inga engelska meningar kvar utöver namn och kommandon som `docs/sv/TERMS.md` behåller på engelska.
- Antal, versioner och kommandon i HTML stämmer med md.
- Inga brutna länkar och ingen vågrät scroll vid 375 px bredd.

## Förhandsvisning

```bash
python -m http.server 8765
```

Öppna sedan http://localhost:8765/html/andthen-guide.html. Sidan går också att öppna direkt som fil.

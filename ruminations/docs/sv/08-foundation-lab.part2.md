## Genomarbetat exempel: så bedömer du uppvärmningsdiffen

Component: en dialog med id:t `warmup`, som öppnas från exempellänken på F1-kortet. Eyebrow ”F1 · Steg 3”, en Stäng-knapp och sedan innehållet nedan. Diffen visas som ett kodblock där borttagna och tillagda rader har var sin färg. De fem frågorna är en numrerad lista, och varje fråga har en rad ”Kontroll” och en rad ”Här”. Bra och Mindre bra står bredvid varandra och läggs under varandra på en smal skärm.

När en agent fick uppgiften ”Lägg till en kort docstring för modulen i src/app/utils.py som förklarar vad den är till för” svarade den med diffen nedan. Din agent svarar på ett annat sätt, men frågorna är desamma.

```diff
-"""Shared utility functions for templates and routes."""
+"""Shared utility functions for templates and routes.
+
+Due-date checks (is_overdue, is_due_today) and date formatting for display
+and for HTML date inputs (format_date, format_date_input). The route modules
+register them as Jinja template globals.
+"""
```

### Fem frågor

1. **Gjorde den det jag bad om?** Kontroll: jämför med din instruktion, ord för ord. Här: delvis. Du bad om en kort docstring, men det fanns redan en, och agenten byggde ut den utan att fråga.
2. **Stämmer det?** Kontroll: pröva varje påstående mot koden. Här: ja. Funktionsnamnen finns (`grep -n "^def" src/app/utils.py`), och registreringen i Jinja finns i tre route-filer.
3. **Höll den sig inom omfånget?** Kontroll: `git diff --stat` visar bara de filer och rader du väntade dig. Här: ja. Bara docstringen i en fil ändrades, ingen kod.
4. **Passar den in i omgivningen?** Kontroll: titta på koden runt omkring, på stil, längd och ton. Här: tveksamt. Alla andra docstrings i filen är en rad lång, och den här är sex.
5. **Gick något sönder?** Kontroll: `uv run pytest`. Här: nej, 58 tester gick igenom.

### Bra

- Allt den säger stämmer och är kontrollerat.
- Ändringen är liten och håller sig till en fil.
- Ingen logik ändrades, och testerna går igenom.
- Den behöll den gamla raden i stället för att skriva över den.

### Mindre bra

- **Den frågade inte.** När det redan fanns en docstring hade det bästa svaret kanske varit ”Det finns redan en. Vill du att jag bygger ut den?”
- **Den upprepar koden.** Funktionsnamnen står nu både i koden och i docstringen. Lägger du till en funktion blir docstringen fel, om ingen kommer ihåg att uppdatera den.
- **”Kort” tolkades generöst.** Den är längre än alla andra docstrings i filen.

Så hade jag gjort: låtit den befintliga raden vara, eller lagt till högst en mening om varför modulen finns, inte om vad den innehåller.

Poängen med övningen: du äger varje rad, även när agenten har skrivit den. De fem frågorna kommer tillbaka i full skala i F6, när `review` bedömer en hel funktion.

## Genomarbetat exempel: Project Document Index

Component: en dialog med id:t `index`, som öppnas från exempellänken på F1-kortet och är uppbyggd som uppvärmningsexemplet. Eyebrow ”F1 · Steg 5”, en Stäng-knapp och sedan innehållet nedan. De två utdragen ur indexet är mörka kodblock. I det andra är anteckningen om vilken skill som lägger till varje rad nedtonad. Hur du läser en post visas som en kort definitionslista.

Efter `init` har `todo-app/CLAUDE.md` ett avsnitt `## Project Document Index`. Agenterna läser det för att hitta projektets dokument, och varje skill lägger till en rad där när den skapar ett nytt dokument.

### Direkt efter init

```markdown
## Project Document Index

Documents here are read whole when their trigger matches, so keep them short ...
Create a document that does not exist yet, and its entry here, from
`project-document-templates.md`, or through a subagent ...

- **Key Dev Commands** – `docs/KEY_DEVELOPMENT_COMMANDS.md`: dev, test, build, deploy commands. Read before running verification; update when a command changes.
- **Agent Temp** – `.agent_temp/`: scratch workspace for reviews, research, and QA; never ship from it.
```

De två styckena är regler för agenten: läs ett dokument bara när dess trigger passar uppgiften, och skapa ett dokument som saknas från AndThens mall, med en egen rad här. Än så länge finns bara två poster, eftersom bara de två dokumenten finns.

### Så läser du en post

- **Namn**, till exempel `Key Dev Commands`: det som skills letar efter, och därför ändras det aldrig.
- **Sökväg**: var filen ligger, relativt `todo-app/`.
- **Innehåll**: en rad om vad filen innehåller.
- **När**: triggern, till exempel ”Read before running verification”. Agenten öppnar filen bara då, inte hela tiden.

### Så växer indexet

Varje skill lägger till sin rad när den skapar ett dokument. Efter F1 till F3 ser listan ut ungefär så här:

```markdown
- **Product** – `docs/PRODUCT.md`: vision, personas, non-goals ...        ← clarify, F2
- **Specs & Plans** – `docs/specs/<version-or-feature>/`: prd.md, plan.json, one FIS per story ...   ← clarify / plan, F2 och F4
- **Decisions** – `docs/DECISIONS.md`: ADR index and Still Current notes ...   ← decide, F3
- **ADRs** – `docs/adrs/`. Read the ADR a decision cites before revisiting it ...   ← decide, F3
- **Ubiquitous Language** – `docs/UBIQUITOUS_LANGUAGE.md`: canonical terms and the synonyms to avoid ...   ← domain --mode glossary, F3
- **Key Dev Commands** – `docs/KEY_DEVELOPMENT_COMMANDS.md`: ...   ← init, F1
- **Agent Temp** – `.agent_temp/`: ...   ← init, F1
```

Formuleringarna kommer från AndThens mallar. De förkortade raderna ovan visar bara formen.

### Kontrollera det

Kontrollpunkten i F1, att sökvägarna finns, betyder att varje sökväg i indexet pekar på något som finns. Kör `ls docs/KEY_DEVELOPMENT_COMMANDS.md` från `todo-app/`. `.agent_temp/` behöver inte finnas än: den första skill som skriver där skapar katalogen.

## Genomarbetat exempel: hur mycket struktur delade listor behöver

Component: en dialog med id:t `dial`, som öppnas från exempellänken på F1-kortet och är uppbyggd som de andra genomarbetade exemplen. Eyebrow ”F1 · Steg 7”, en Stäng-knapp och sedan innehållet nedan. De tre vägarna är en tabell med tre kolumner som rullar i sidled på en smal skärm. Ingångstestet står i en markerad ruta. De två frågorna under ”Hur stort är arbetet?” är en definitionslista.

Det finns tre vägar, och ingångstestet visar var du ska börja. Så här resonerar du för labbets funktion.

### De tre vägarna

| Arbete | Väg | Struktur |
|------|------|-----------|
| En rättelse du kan beskriva i en mening | `implement-fix` → `ship` | Minimal |
| En riktig funktion | [`clarify` →] `plan` → `exec-plan` → `review --fix` → `ship` | En FIS och en `plan.json` med en story |
| Flera funktioner | samma kedja, med `plan <dir>` | En FIS per story. Oberoende stories kan köras parallellt |

Ingångstestet: kan du inte räkna upp tre acceptanskriterier börjar du med `clarify`, annars med `plan`.

### 1. Hur stort är arbetet?

- **Kan du beskriva det som en rättelse i en mening?** Nej. Det berör datamodellen, behörigheterna och gränssnittet.
- **Är det flera separata funktioner?** Nej. Det är en enda sak: att dela en lista.
- **Väg:** en riktig funktion, alltså den mellersta vägen.

### 2. Börja med clarify eller plan?

Fråga dig själv: kan jag räkna upp tre testbara acceptanskriterier just nu? Allt du har är en rad, ”Let people share their lists”. Försöker du skriva tre kriterier stöter du genast på öppna frågor:

- Vem kan du dela med: bara registrerade användare, eller vilken e-postadress som helst?
- Vad får mottagaren göra: läsa, ändra eller ta bort?
- Vad händer om du delar två gånger, eller med dig själv?
- Hur och när upphör delningen?

Så länge de frågorna är obesvarade håller inga tre kriterier. Därför börjar du med `clarify`: den intervjuar dig och skriver en PRD. Hade svaren redan funnits, till exempel i ett ärende i trackern, hade du börjat med `plan`.

### Jämför: en rättelse på en mening

En bugg som ”En ny todo får tom prioritet i stället för låg” ryms i en mening och har ett enda tydligt rätt svar. Det är vägen med minst struktur: `implement-fix` och sedan `ship`, utan spec.

Osäker på vägen? `/andthen:now-what` gör ingångstestet åt dig.

## Genomarbetat exempel: tre acceptanskriterier

Component: en dialog med id:t `criteria`, som öppnas från exempellänken på F2-kortet och är uppbyggd som de andra genomarbetade exemplen. Eyebrow ”F2 · Steg 2”, en Stäng-knapp och sedan innehållet nedan. Kriteriefilen är ett mörkt kodblock med en Kopiera-knapp, så att den kan klistras in direkt i filen.

Så här kan du skriva dem, i `.agent_temp/f2-my-criteria.md`. Dina kan se annorlunda ut. Poängen är att du fattar besluten medvetet, innan någon skill körs.

```markdown
# Share a list – my acceptance criteria

1. Share with a registered user
   Given I own the list "Groceries" and bob@example.com has an account
   When I share "Groceries" with bob@example.com
   Then Bob sees "Groceries" among his lists and can read its todos

2. The recipient can only read
   Given Bob can see my shared list "Groceries"
   When Bob tries to add, change or delete a todo in it,
        in the UI or by sending the request directly
   Then the change is refused and the list stays as it was

3. Awkward edge: an email with no account
   Given no account exists for carol@example.com
   When I share "Groceries" with carol@example.com
   Then I see "No user with that email" and nothing is shared

Out of scope: inviting people without an account, edit rights, notifications.
```

### Lägg märke till

- **Varje kriterium är ett beslut.** Bara registrerade användare, bara läsrätt och ett tydligt svar för en okänd e-postadress. Det var skrivandet som tvingade fram de valen.
- **Vart och ett går att testa.** Given beskriver förutsättningarna, When är en enda handling och Then är något du kan se.
- **Kriterium 2 täcker det direkta anropet**, inte bara en dold knapp. F6 återkommer till just det.
- **Andra kantfall du kan välja:** att dela samma lista två gånger, att dela med dig själv, att återkalla åtkomsten.

Spara filen. I steg 5 jämför du den med PRD:n som `clarify` skriver.

## Genomarbetat exempel: där PRD:n hamnar

Component: en dialog med id:t `prd`, som öppnas från exempellänken på F2-kortet och är uppbyggd som de andra genomarbetade exemplen. Eyebrow ”F2 · Steg 4”, en Stäng-knapp och sedan innehållet nedan. Projektträdet är ett mörkt kodblock med nedtonade anteckningar. Raderna bryts aldrig, och blocket rullar i sidled på en smal skärm.

`clarify` skriver ut sökvägen när den är klar, till exempel `Wrote docs/specs/shared-lists/prd.md`. Den katalogen är din `<feature-dir>`. Skriv upp den, eftersom alla steg från F3 till F7 använder den.

```text
todo-app/
├── CLAUDE.md                          ← indexet får rader för de nya dokumenten
├── docs/
│   ├── KEY_DEVELOPMENT_COMMANDS.md    från init i F1
│   ├── PRODUCT.md                     ny: fas, skala, tekniska icke-mål
│   └── specs/
│       └── shared-lists/              ← din <feature-dir>
│           └── prd.md                 ← PRD:n
├── src/
└── tests/
```

Det är `clarify` som väljer katalognamnet, så ditt kan skilja sig från `shared-lists`. Kör `ls docs/specs/` från `todo-app/` för att se det.

I F4 skriver `plan` in `plan.json` och FIS:en (`s01-….md`) i samma katalog. I F7 tar `ship` bort de två och behåller `prd.md`: PRD:n är den enda planeringsfil som lever kvar efter branchen.

## Genomarbetat exempel: det här skrev plan

Component: en dialog med id:t `plan-files`, som öppnas från exempellänken på F4-kortet och är uppbyggd som de andra genomarbetade exemplen. Eyebrow ”F4 · Steg 1”, en Stäng-knapp och sedan innehållet nedan. Projektträdet är ett mörkt kodblock med nedtonade anteckningar, som trädet i F2. Raderna bryts aldrig, och blocket rullar i sidled på en smal skärm.

`plan` skriver sina filer bredvid `prd.md` i din `<feature-dir>`. När den körs på hela PRD:n avgör den hur många stories arbetet behöver och skriver en FIS per story. En körning delade den här PRD:n i två:

```text
todo-app/
├── docs/
│   ├── adrs/                               från decide i F3
│   ├── DECISIONS.md                        från decide i F3
│   ├── UBIQUITOUS_LANGUAGE.md              från domain i F3
│   └── specs/
│       └── let-people-share-their-lists/   ← din <feature-dir>
│           ├── prd.md                      PRD:n, från F2
│           ├── plan.json                   ← ny: stories och deras dependsOn
│           ├── s01-share-a-list-….md       ← ny: FIS:en för story S01
│           └── s02-recipient-leaves-….md   ← ny: FIS:en för story S02
├── src/
└── tests/
```

Dina stories och deras namn kan skilja sig, eftersom det är `plan` som väljer uppdelningen. Det här steget är bara till för läsning, så öppna filerna men kör dem inte:

- **`plan.json`**: under `stories` varje storys `scope` och `dependsOn`. Här beror S02 på S01, så de två kan inte köras samtidigt.
- **Varje FIS**: dess Intent, dess scenarier och What We're NOT Doing. Se hur uppdelningen i stories förhåller sig till din ADR och din ordlista.
- **Utdata från `plan`**: eventuella `OVERSIZE:`-rader och listorna `Decided:` och `Assumed:` som den avslutar med.

Parkera sedan filerna: flytta `plan.json` och `s*.md`-filerna till `.agent_temp/whole-prd-plan/`. `prd.md` ligger kvar, eftersom steg 3 planerar utifrån den igen.

## Genomarbetat exempel: dit den parkerade planen flyttar

Component: en dialog med id:t `parked`, som öppnas från exempellänken på F4-kortet och är uppbyggd som de andra genomarbetade exemplen. Eyebrow ”F4 · Steg 1”, en Stäng-knapp och sedan innehållet nedan. Kommandona är ett mörkt kodblock med en Kopiera-knapp. Projektträdet är ett mörkt kodblock med nedtonade anteckningar, som trädet i F2. Raderna bryts aldrig, och blocket rullar i sidled på en smal skärm.

Parkera planen för hela PRD:n före steg 3, annars hamnar planen med en story bredvid den. Kör de här kommandona från `todo-app/` och anpassa katalognamnen till din `<feature-dir>`:

```bash
mkdir -p .agent_temp/whole-prd-plan
mv docs/specs/let-people-share-their-lists/plan.json docs/specs/let-people-share-their-lists/s*.md .agent_temp/whole-prd-plan/
```

Efter flytten ser projektet ut så här:

```text
todo-app/
├── .agent_temp/                            ← git ignorerar den (init lade till den i F1)
│   └── whole-prd-plan/                     ← ny: den parkerade planen, bara för läsning
│       ├── plan.json
│       ├── s01-share-a-list-….md
│       └── s02-recipient-leaves-….md
├── docs/
│   └── specs/
│       └── let-people-share-their-lists/   ← din <feature-dir>
│           └── prd.md                      ← ligger kvar: steg 3 planerar utifrån den igen
├── src/
└── tests/
```

Använd `.agent_temp/` inuti `todo-app/`. Git ignorerar just den katalogen, så den parkerade planen hamnar aldrig i en commit. En `.agent_temp/` i repots rot ignoreras inte.

Kontrollera: `ls docs/specs/let-people-share-their-lists/` visar bara `prd.md`.

## Genomarbetat exempel: ett handskrivet FIS-skelett

Component: en dialog med id:t `fis`, som öppnas från exempellänken på F4-kortet och är uppbyggd som de andra genomarbetade exemplen. Eyebrow ”F4 · Steg 2”, en Stäng-knapp och sedan innehållet nedan. Skelettet är ett mörkt kodblock med en Kopiera-knapp, så att det kan klistras in direkt i filen.

Så här kan du skriva det, i `.agent_temp/f4-my-fis.md`, för den vertikala skivan **dela en lista med bara läsrätt**. Ditt kan se annorlunda ut. Formatet är enkelt, och besluten ligger i scenarierna.

```markdown
# Share a list view-only – my FIS skeleton

## Intent
A household member follows another member's list as it is right now, without copying it, while only the owner can change it.

## Expected Outcomes
- [OC1] The owner shares a list with a registered user by email, and can revoke it.
- [OC2] The recipient reads the list and all its todos under "Shared with me".
- [OC3] The recipient can change nothing, in the UI or by a direct request.

## Acceptance Scenarios
S01 [OC1, OC2] Share with a registered user
  Given Alice owns "Groceries" and bob@example.com has an account
  When Alice shares "Groceries" with bob@example.com
  Then Bob sees "Groceries" under "Shared with me", marked with
       Alice's email, and can open it and read every todo

S02 [OC1] Awkward edge: an email with no account
  Given no account exists for carol@example.com
  When Alice shares "Groceries" with carol@example.com
  Then she sees "No user with that email" and no share is stored

S03 [OC3] The recipient cannot change it, even directly
  Given "Groceries" is shared with Bob
  When Bob sends PATCH /api/todos/{id}/toggle for one of its todos,
       outside the UI
  Then he gets 403 and the todo is unchanged

## What We're NOT Doing
- Leave (the recipient drops the list): a later story
- Edit rights, invitations for emails without an account, notifications
- Reordering shared lists in the sidebar

## Tasks
T1 Add ListShare as ADR-001 decides
   Verify: uv run pytest tests/test_sharing.py -k model
           (a duplicate share fails; deleting the list removes its shares)
T2 Add get_owned_list and get_readable_list (ADR-002), and switch
   every list and todo route to one of them
   Verify: grep -n "_verify_list_access" src/app/routes/todos.py finds nothing,
           and uv run pytest is green
T3 Share and revoke routes, and the Share section in list settings
   Verify: uv run pytest tests/test_sharing.py -k share (S01, S02)
T4 "Shared with me" in the sidebar, and a list view with no change controls
   for the recipient
   Verify: uv run pytest tests/test_sharing.py -k recipient (S03);
           inspect: signed in as Bob, no add field, pencil or trash icon
```

### Lägg märke till

- **Varje scenario anger sitt utfall.** [OC]-taggarna visar vad som bevisar vad. OC1 lovar att delningen går att återkalla, men inget scenario bevisar det. Det är en sådan lucka som steg 4 ska fånga.
- **S03 skickar anropet direkt.** En dold knapp är ingen vägran. Servern måste säga nej, och scenariot anger hur du ser det: 403, och todon är oförändrad.
- **Varje uppgift har en Verify som du kan köra eller inspektera.** ”Det fungerar” är ingen Verify. Ett testnamn, ett kommando eller något att titta på är det.
- **Uppgifterna bygger på ADR:erna.** T1 och T2 följer ADR-001 och ADR-002 i stället för att göra om modellen eller åtkomstkontrollen.
- **Att låta bli är också ett beslut.** Leave finns i PRD:n (FR5), men den här skivan parkerar den medvetet.

Spara filen. I steg 4 jämför du den med FIS:en som `plan` skriver. Räkna med att den lägger till scenarier som du hoppade över, som återkallning, att dela två gånger och en tom e-postadress, och ett bevis för varje route som ändrar data, inte bara för en.

## Genomarbetat exempel: en uppgift och dess Verify-rad

Component: en dialog med id:t `task`, som öppnas från exempellänken på F5-kortet och är uppbyggd som de andra genomarbetade exemplen. Eyebrow ”F5 · Steg 2”, en Stäng-knapp och sedan innehållet nedan. Uppgiften är ett mörkt kodblock med nedtonade anteckningar, som trädet i F2. Raderna bryts aldrig, och blocket rullar i sidled på en smal skärm. De tre formerna av Verify är en punktlista.

Öppna FIS:en, `<feature-dir>/s01-<name>.md`, och leta upp `### Implementation Tasks` under Implementation Plan. Agenten tar uppgifterna i ordning och går vidare först när en uppgifts Verify går igenom. Här är TI04 från S01:

```text
- **TI04** Every change route refuses a       ← det som måste gälla
  recipient's direct request and leaves
  the list unchanged
  - Depends on TI02.                          ← ordningen
  - **Verify**: `tests/test_sharing.py#       ← kontrollen
    test_recipient_change_requests_refused`
    – one parametrized case per S11
    request, each asserting its status and
    that the list … match a snapshot taken
    before the request
  - **SATISFIES**: S11                        ← scenariot
```

Läs varje uppgift i fyra delar:

- **Uppgiftsraden** säger vad som måste gälla när uppgiften är klar, inte hur den ska kodas.
- **Depends on** bestämmer ordningen. TI04 behöver de hjälpfunktioner för åtkomst som TI02 lägger till.
- **Verify** är det som agenten kör innan den går vidare. Raden börjar med ett mål och säger efter tankstrecket vad som måste gälla. Här skickar ett enda test alla nio anrop i S11 och jämför listan med en ögonblicksbild.
- **SATISFIES** kopplar uppgiften tillbaka till dess scenarier. Öppna S11 under Acceptance Scenarios: dess Then är det som testet kontrollerar.

Ett mål i Verify har en av tre former. Alla tre finns i S01:

- **Test**: `tests/test_sharing.py#test_duplicate_share_row_is_refused` (TI01) kör just det testet, som antingen går igenom eller misslyckas.
- **Kommando**: `cmd: uv run pytest -x -q` (TI02) körs i ditt skal, och slutkod 0 betyder godkänt.
- **Inspektion**: `inspect: src/app/static/js/app.js#openEditListDialog` (TI09) kör ingenting, utan någon måste läsa koden. Final Validation Checklist i slutet av FIS:en täcker den med en manuell körning.

**Fråga om varje uppgift: skulle du själv kunna köra dess Verify och se den gå igenom eller misslyckas?** En Verify som är skriven som löptext, utan mål, är en lucka som du rättar i FIS:en innan du kör den.

## Genomarbetat exempel: det här ska du peka ut

Component: en dialog med id:t `observations`, som öppnas från exempellänken på F5-kortet och är uppbyggd som de andra genomarbetade exemplen. Eyebrow ”F5 · Steg 4”, en Stäng-knapp och sedan innehållet nedan. Tabellen rullar i sidled på en smal skärm.

En körning av S01 lämnade de här punkterna under `## Implementation Observations` i slutet av `docs/specs/let-people-share-their-lists/s01-shared-lists.md`. Din körning skriver sina egna, men de faller i samma kategorier:

| I FIS:en | Det här pekar du ut | Sedan |
|------------|-------------------|------|
| **Review repair (F1, code-defect, fixed)** | Alla 89 tester var gröna, men en ny granskare hittade ändå en riktig bugg: en snabb växling mellan två listors inställningar kunde dela fel lista. Rättelsen bevisas bara av en körning i webbläsaren, eftersom projektet saknar testkörare för JS. | Godta, och var medveten om att just det beviset är manuellt. |
| **Blank email · TI10 timing** | Tysta omtolkningar. ”Email is required” är ett meddelande som PRD:n aldrig nämner, och tidtagningstestet värmer upp en gång fast FIS:en säger att det mäter tiden för en enda GET. Var och en är en liten avvikelse som står som en vanlig punkt. | Godta, eller ta upp det i F6 om specen borde säga det. |
| **Tidies** | Ändringar som ingen uppgift omfattar: en oanvänd databasfråga borttagen, en uppslagning flyttad bakom hjälpfunktionen för åtkomst och en tipstext för tomma listor dold för mottagare. | Leta upp var och en i storyns commit och kontrollera att den hör hemma i ändringen. |
| **Not run** | Granskningen körde bara kodlinsen. Säkerhetslinsen kördes aldrig, trots att ändringen till största delen handlar om behörighet. | Ta upp det i F6: granskningen på plannivå kör den. |
| **NOTICED BUT NOT TOUCHING** | Två verkliga problem utanför storyn: ett klick kan skicka flera anrop, och tas en användare bort blir användarens delningar kvar utan ägare. | Senare: teknisk skuld, inte den här branchen. |
| **TI09 inspection · Layout** | Bara kontrollerat för hand. Att dialogen förblir öppen och var ”Shared with me” hamnar har inget automatiskt test. | Godta, och titta på dem själv i F6. |

**Att det saknas ett avsnitt `#### DRIFT` är ett påstående, inte ett faktum.** Körningen skriver DRIFT bara för avvikelser som den känner till. Här rymmer två vanliga punkter små omtolkningar, så läs varje punkt som ”specen sa X, körningen gjorde Y”.

## Genomarbetat exempel: falsifiera en kontroll

Component: en dialog med id:t `falsify`, som öppnas från exempellänken på F6-kortet och är uppbyggd som de andra genomarbetade exemplen. Eyebrow ”F6 · Steg 2”, en Stäng-knapp och sedan innehållet nedan. Kod och testutdata är mörka kodblock vars rader aldrig bryts. De rullar i sidled på en smal skärm.

I referenskörningen hämtar varje route som ändrar data listan genom en ägarkontroll. Du gör det i tre moment, alla från `todo-app/`:

**1. Ändra en rad.** Öppna `src/app/routes/todos.py` och leta upp den här raden i `update_todo`:

```text
list_obj = get_owned_list(db, todo.list_id, user_id)
```

Byt `get_owned_list` mot `get_readable_list` och spara. Funktionen är redan importerad överst i filen, så inget annat ändras. `get_owned_list` returnerar listan bara till ägaren, medan `get_readable_list` också returnerar den till alla som listan delas med. Efter bytet släpps en mottagare med läsrätt förbi kontrollen, och uppdateringen genomförs.

**2. Kör testerna:** `uv run pytest`. Ett test måste misslyckas:

```text
FAILED tests/test_sharing.py::test_recipient_change_requests_refused[update todo]
1 failed, 88 passed
```

Spara filen först. Är den inte sparad kör testerna den gamla koden och förblir gröna. Det ser ut som en testsvit som ljuger, men det är det inte.

**3. Återställ kontrollen:** `git restore src/app/routes/todos.py`. Sedan skriver `git status --short src/` inte ut någonting.

I din körning kan kontrollen ha ett annat namn eller ligga på ett annat ställe. Leta efter stället där en route som ändrar data – update, toggle eller delete – hämtar listan och nekar alla som inte äger den. Eller fråga Claude: ”Vilken rad i update-routen nekar en mottagare med läsrätt? Visa mig, men ändra ingenting.”

**Varför inte bara kommentera bort kontrollen?** Då kraschar routen, och en krasch får testerna att misslyckas oavsett om de kontrollerar rätt sak. En kontroll som släpper igenom en mottagare med läsrätt låter koden fortsätta köra, och därför blir bara ett test som verifierar att ändringen nekas rött.

## Genomarbetat exempel: det här lämnade granskningen efter sig

Component: en dialog med id:t `review-output`, som öppnas från exempellänken på F6-kortet och är uppbyggd som de andra genomarbetade exemplen. Eyebrow ”F6 · Steg 3”, en Stäng-knapp och sedan innehållet nedan. Körningens sista rader är ett mörkt kodblock vars rader aldrig bryts. Både blocket och tabellen rullar i sidled på en smal skärm.

I referenskörningen hittade `review --fix` fem saker: ett HIGH-fynd (en ägare kunde injicera CSS på en mottagares sida via listans färg) och fyra LOW. Körningen avslutades så här:

```text
Report: docs/specs/let-people-share-their-lists/let-people-share-their-lists-andthen-mixed-review-claude-2026-11-05.md
Report annotation: written (## Remediation Status)
Tech-debt entries written: 0 entries
Next (fresh session): /andthen:review docs/specs/let-people-share-their-lists/plan.json --fix
```

Varje rad pekar på något som körningen lämnade efter sig:

| Var | Det här lämnade referenskörningen | Sedan |
|-------|-----------------------------|------|
| **Rapporten**, bredvid `plan.json` | Utlåtandet först, `Overall readiness: Needs Fixes`, en etikett per lins (code, gap, security, outcome), en Coverage Matrix och varje fynd märkt Fix eller Note. Git ignorerar rapporten, så den stannar på din dator. | Jämför fynden med det du själv hittade i steg 1–2. |
| **Din arbetskatalog** | De två Fix-fynden tillämpade men inte committade: en färgkontroll i `src/app/routes/todo_lists.py` och tester i `tests/test_sharing.py` som misslyckades före kontrollen. `uv run pytest` gick igenom med 102 tester. | Läs `git diff`. `ship` committar ändringarna. |
| **`## Remediation Status`**, rapportens sista avsnitt | En rad per fynd: de två Fix-fynden RESOLVED med bevis, de tre Note-fynden SURFACED och orörda. Rapportens huvud får en rad `**Remediated**:`. | Ta ställning till varje SURFACED Note i steg 4. |
| **`docs/TECH-DEBT-BACKLOG.md`** | Inget än, eftersom granskningen inte skjuter upp något på egen hand. När de tre Note-fynden sköts upp efteråt blev det tre Low-poster, var och en med det som blockerar den och rapporten som källa, och en rad `Tech Debt` i Project Document Index. | Bara det du godkänner skrivs. |
| **Raden `Next`** | En uppföljande granskning, eftersom körningen rättade ett HIGH-fynd, och sessionen som gjorde en rättelse är inte rätt session att bedöma den. | Kör den i en ny session före `ship`. |

**Needs Fixes är utlåtandet före rättelserna.** Utlåtanderaden visar vad granskaren hittade. Raden `**Remediated**:` säger att rättelser kom efteråt, och först den uppföljande granskningen ger ett nytt utlåtande.

## Härnäst

Component: en avslutande rad och sedan en rad knappar. Den första är fylld, den andra har bara kontur.

Nu har du kört hela Core Loop en gång. I casearbetet kör du samma loop på ett riktigt case, med en kontrollpunkt vid varje artefakt.

- Tillbaka till Core Loop → (loop)
- Läs labböversikten på GitHub → (https://github.com/IT-HUSET/agentic-engineering-2026/blob/main/labs/README.md)

---
title: Foundation Lab
tab: Foundation Lab
token: lab
order: 8
depends_on: [shared/icons.md]
source: labs/foundation.md
---

# Foundation Lab

Eyebrow: Labb · Del 1

## Kör Core Loop för en funktion, en gång

Component: ”Core Loop” i rubriken sätts i accentfärgen.

Du bygger en riktig funktion i kursens todo-app, delade listor, från en idé på en rad till en mergad pull request. Varje steg lämnar en fil på disken som nästa steg läser, och slutar med en checklista och en strukturkontroll.

Component: under ingressen tre fakta som små chips med etikett, sedan en länkknapp.

- Projektrot: `todo-app/`
- Branch: `feat/shared-lists`
- Funktion: delade listor, en ägare låter en annan registrerad användare se en av sina listor

Button: Läs hela labbet på GitHub → (https://github.com/IT-HUSET/agentic-engineering-2026/blob/main/labs/foundation.md)

## Så tar du dig igenom labbet

Component: en kompakt ruta med en punktlista, formulerad som i labs/foundation.md. Varje punkt börjar med en fet inledning. De två kommandona under första punkten är en tät numrerad lista. Inga kort, siffror eller tipsruta.

- **Projektroten är `todo-app/`.** Starta Claude Code där, från repots rot:
  1. `cd todo-app`
  2. `claude`

  Alla sökvägar i labbet, som `docs/specs/...`, är relativa till den.
- **En ny session per steg.** De flesta steg slutar med en rad `Next (fresh session):`. Kör `/clear` och klistra sedan in raden. Varje steg läser filerna som det förra steget skrev, inte chatten.
- **`<feature-dir>`** är mappen som `clarify` skriver ut för din PRD i F2, till exempel `docs/specs/<slug>/`. Skriver den ut `Wrote docs/specs/shared-lists/prd.md` är din `<feature-dir>` alltså `docs/specs/shared-lists/`. Anteckna den, eftersom senare steg använder den. Kopieringsrutorna i stegkorten använder referenskörningens mapp, `docs/specs/let-people-share-their-lists/`: heter din något annat byter du ut den när du klistrar in.
- **Svara på frågorna.** `clarify`, `decide` och `plan` intervjuar dig, och varje fråga har ett rekommenderat svar. Rekommendationen är en utgångspunkt, inte ett standardval att godta oläst.
- **Kommer du in sent eller har kört fast?** Kursledaren har en förberedd PRD, ADR, ordlista och FIS. Be om FIS:en tillsammans med dess `plan.json` för F5.

## De sju stegen (F1–F7)

Interactive component: en stegrad med de sju stegen, F1 till F7, med ”/clear” mellan dem och varje stegs resultat under dess etikett. Piltangenterna flyttar längs raden. När ett steg väljs visas dess kort, tonat efter stegets Tint: stegnumret, Skills, titeln, Input, en grön startlinje, Steps som numrerad lista, sedan en sidokolumn med Output-rutan (ikon, titel, text), en grön startlinje, kommandona med kopieringsknappar, eventuell Prompt som ren text utan kopieringsknapp, eventuell Stop-rad som en röd linje över kolumnen med stoppikonen före texten (Steps-listan har då en ensam röd linje på samma ställe). Startlinjerna är 3 px i den gröna accentfärgen och Stop-linjerna 3 px i rött. När kolumnerna står bredvid varandra ritas varje par i samma höjd, och den högre linjen flyttas ned. Därefter kommer eventuella Example-länkar i sin ordning, sedan, när steget har ett Studio-fält, en lavendelfärgad ruta ”I AndThen Studio · valfritt” med Studio-kommandot och dess kopieringsknapp, texten och en länk till fliken Studio, därefter Verify-checklistan och Structure check, och knapparna Föregående och Nästa. Varje kommandoruta är dold från början bakom en knapp ”Visa kommando”, som på fliken Installation.

Component: Verify-punkterna är kryssrutor. Bockarna sparas bara i den här webbläsaren. En förloppsrad ovanför stegraden räknar bockarna i alla steg och har en knapp Återställ. Varje stegetikett visar sitt eget antal när minst en ruta är ibockad.

Hint under the card: Välj ett steg på raden, eller använd piltangenterna. Bocka av kontrollerna medan du arbetar. De sparas i den här webbläsaren.

### F1 – Orientera dig och installera

- Tint: rust
- Skills: now-what, init, describe
- Input: En klon av din fork, Claude Code inloggat och AndThen installerat enligt fliken Installation.
- Output: folder · Ett projekt som AndThen hittar i · Ett Document Index i CLAUDE.md, dokumentet Key Dev Commands och två rader i .gitignore, committade på din branch.
- Command: `git switch -c feat/shared-lists` (1. Skapa en branch)
- Command: `uv run pytest` (2. Kontrollera att arbetskatalogen är i gott skick)
- Command: `./run.sh` (2. Starta appen i en egen terminal och stoppa den med Ctrl-C)
- Command: `bash run.sh` (2. Eller det här, om ./run.sh inte startar, till exempel på Windows)
- Prompt: Lägg till en kort docstring (kommentar) för modulen i filen `src/app/utils.py` som förklarar vad den är till för. (3. Fråga Claude Code. Det här är en prompt, inte ett skalkommando)
- Command: `git diff --stat` (3. Se hur stor ändringen är)
- Command: `git diff src/app/utils.py` (3. Läs diffen)
- Command: `uv run pytest` (3. Kör testerna igen)
- Example: 3. Genomarbetat exempel: så bedömer du diffen → (warmup)
- Command: `git restore src/app/utils.py` (3. Kasta ändringen när du är klar)
- Stop: **Stopp.** Gå inte vidare förrän `git status --short src/` inte skriver ut något och `uv run pytest` är grönt: från steg 4 läser och skriver AndThen i arbetskatalogen, så börja från ett rent utgångsläge.
- Command: `/andthen:now-what` (4. Låt den peka ut vägen för repot, och svara ja till init)
- Command: `/andthen:init` (5. now-what föreslår init, eller så kör du den själv)
- Command: `ls docs/KEY_DEVELOPMENT_COMMANDS.md` (5. Kontrollera verifieringspunkten i F1: CLAUDE.md har ett Project Document Index, och dess sökvägar finns)
- Example: 5. Genomarbetat exempel: så ser indexet ut → (index)
- Example: 7. Genomarbetat exempel: hur mycket struktur delade listor behöver → (dial)
- Command: `git status --short` (8. Se vad init skrev: bara CLAUDE.md, .gitignore och docs/ ska synas)
- Command: `git add CLAUDE.md .gitignore docs` (8. Stagea per sökväg, aldrig git add -A)
- Command: `git commit -m "Set up AndThen"` (8. Committa installationen)
- Command: `git log --oneline -1` (8. Kontrollera committen: den senaste ska vara Set up AndThen)
- Command: `git status --short` (8. Kontrollera arbetskatalogen: inga M- eller A-rader kvar, bara ?? för lokala filer)
- Studio command: `andthen_studio` (Efter steg 5: starta den i en egen terminal, från todo-app/, och låt den köra under hela labbet)
- Studio: Project home visar vad Document Index pekar på. Fäll ut Project documents och öppna Key Dev Commands från sidopanelen. 0 plans stämmer just nu, och Models förblir tomt: `describe` skrev ingen modell här.

Steps:

1. **Skapa en branch.** Allt slutar i en pull request, och AndThen committar på den aktuella branchen: `git switch -c feat/shared-lists`.
2. **Uppvärmning (A): lär känna terrängen.** Kör `uv run pytest`. Starta sedan appen i en egen terminal med `./run.sh` eller `bash run.sh`, öppna http://localhost:8000 (demo@example.com / demo123) och klicka runt. Varje lista har en enda ägare, och ingenting delas. Stoppa appen med Ctrl-C.
3. **Uppvärmning (B): en ändring, inga skills.** Be agenten om något litet och ofarligt, till exempel en docstring för modulen i `src/app/utils.py`. Läs diffen och kör testerna igen. Kasta sedan ändringen med `git restore src/app/utils.py`.

   Stop line: en ensam röd linje, i höjd med Stop-raden i sidokolumnen.

4. **Låt `now-what` peka ut vägen i ett repo utan AndThen.** Kör `/andthen:now-what` i Claude Code, startat i `todo-app/`. Den skriver ut Core Loop och erbjuder `init`. Svara ja.
5. **`init`.** Den frågar ingenting här. Den lägger till Project Document Index i `CLAUDE.md`, skriver dokumentet Key Dev Commands och lägger till två rader i `.gitignore`. Strunta så länge i de extra erbjudandena i sammanfattningen.
6. **`describe`: läs kartan över koden.** Kör den inte här. Läs det förberedda resultatet i `docs/` medan kursledaren kör den på skärmen. Saknas `todo-app/docs/`, eller är mappen tom, säger du till kursledaren innan du går vidare.
7. **Läs av (bedöm) hur mycket struktur arbetet behöver.** Lär dig de tre vägarna och ingångstestet: kan du inte räkna upp tre acceptanskriterier börjar du med `clarify`, annars med `plan`.
8. **Committa installationen.** Stagea per sökväg, aldrig `git add -A`: `git add CLAUDE.md .gitignore docs`, sedan `git commit -m "Set up AndThen"`.

Verify:

- `uv run pytest` går igenom i en ren arbetskatalog.
- `CLAUDE.md` har ett Project Document Index, och dess sökvägar finns.
- `docs/KEY_DEVELOPMENT_COMMANDS.md` anger ett testkommando, och du har kört det för hand.
- `.gitignore` innehåller `.agent_temp/`.
- Du har valt ett upptäckt krav som du skulle bekräfta och ett som du skulle ifrågasätta.
- Du kan formulera ingångstestet och de tre vägarna.

Structure check: Var appen värd `init` och `describe`? En kodbas som du ska arbeta i under flera veckor är värd båda, en gång, från början. Ett engångsskript är inte värt någotdera.

### F2 – Klargör

- Tint: red
- Skills: clarify
- Input: En rad, ”Let people share their lists.” Inget annat.
- Output: doc · prd.md · PRD:n i mappen för din funktion, plus uppgifterna under Proportionality i docs/PRODUCT.md.
- Text: 2. Skriv tre acceptanskriterier för hand, i .agent_temp/f2-my-criteria.md
- Example: 2. Genomarbetat exempel: tre acceptanskriterier → (criteria)
- Stop: **Stopp.** Gå inte vidare förrän dina tre kriterier ligger i `.agent_temp/f2-my-criteria.md`: när `clarify` väl börjar fråga kan du inte längre skriva dina egna utan att påverkas.
- Command: `/andthen:clarify "let people share their lists"` (3. Kör intervjun, i en ny session)
- Command: `ls docs/specs/` (4. Hitta din <feature-dir>)
- Example: 4. Genomarbetat exempel: var PRD:n hamnar → (prd)
- Command: `git add docs CLAUDE.md` (5. Valfritt: committa PRD:n nu. Stagea per sökväg. CLAUDE.md ligger utanför docs/)
- Command: `git commit -m "Add shared-lists PRD"` (5. Valfritt: committa PRD:n, PRODUCT.md och de nya raderna i indexet)
- Studio: Reader: öppna `prd.md` under Requirements. Hoppa med avsnittslistan till Out of Scope och Open Questions inför steg 5. Fäst en anteckning på ett avsnitt som du tvivlar på. Kopiera dina anteckningar som markdown till jämförelsen, eller skicka dem och låt `clarify` revidera PRD:n. Committa i så fall PRD:n igen.

Steps:

1. **Stanna kvar i den luddiga idén.** Motstå frestelsen att designa. Vem kan du dela med, vad kan de göra och när upphör åtkomsten?
2. **För hand: skriv tre acceptanskriterier.** Spara dem i `.agent_temp/f2-my-criteria.md` innan någon skill körs. Driv ett av dem till ett besvärligt kantfall: en e-postadress utan konto, att dela två gånger, att dela med dig själv, att återkalla. Lägg till en rad om vad du skulle lämna utanför.

   Stop line: en ensam röd linje, i höjd med Stop-raden i sidokolumnen.

3. **Med AndThen: kör intervjun.** Kör `clarify` i en ny session. Svara på frågorna och låt den säga emot. Svara medvetet vagt på en sak och se hur den gräver vidare.
4. **Läs PRD:n.** Den hamnar i `docs/specs/<slug>/prd.md`, och den mappen är din `<feature-dir>`: anteckna den. PRD:n lever längre än branchen, så läs den noga.
5. **Jämför med kriterierna som du skrev för hand.** Vad frågade den om som du missade, och tvärtom? Läs Out of Scope: vad parkerades för att den första skivan ska förbli liten?

Verify:

- Du kan räkna upp tre testbara acceptanskriterier ur PRD:n.
- Du kan säga vad den inte ska göra: inbjudningar, roller, aviseringar.
- En minsta levererbara skiva är namngiven: bara läsrätt, registrerade användare.
- De besvärliga kantfallen har ett förväntat beteende, eller ligger medvetet under Open Questions.
- `docs/PRODUCT.md` anger fas, skala och tekniska icke-mål.

Structure check: Var delade listor värda en fullständig `clarify`? Ja, en enda rad förgrenar sig i ett dussin vägval. En mening utan verkliga frågetecken går till `implement-fix`.

### F3 – Besluta

- Tint: cream
- Skills: decide, domain --mode glossary
- Input: PRD:n från F2 och vägvalet i designen: hur modelleras ”den här användaren får se den listan”?
- Output: seal · ADR + ordlista · En ADR i docs/adrs/ med sin rad i docs/DECISIONS.md, och docs/UBIQUITOUS_LANGUAGE.md.
- Command: `/andthen:decide docs/specs/let-people-share-their-lists` (1. /andthen:decide <feature-dir>: avgör vägvalet, i en ny session)
- Text: 2. Läs ADR:erna i docs/adrs/ och deras rader i docs/DECISIONS.md
- Stop: **Stopp.** Gå inte vidare förrän du kan peka ut ADR:ens Reversal-rad och basalternativet som den valde bort: ordlistan namnger det som ADR:en avgjorde, så en felaktig ADR sprider sig till varje term.
- Command: `/andthen:domain --mode glossary shared lists` (3. Namnge termerna, i en ny session. AndThen kan sedan föreslå plan: hoppa över det, steg 4 och 5 kommer först)
- Text: 4. Läs ordlistan i docs/UBIQUITOUS_LANGUAGE.md och dess Avoid-kolumn
- Command: `git status --short` (5. Se vad F2 och F3 skrev: PRD:n, PRODUCT.md, ADR:en, DECISIONS.md, ordlistan och CLAUDE.md)
- Command: `git add docs CLAUDE.md` (5. Stagea per sökväg. CLAUDE.md ligger utanför docs/, så ange den)
- Command: `git commit -m "Add shared-lists PRD, ADR and glossary"` (5. Committa designartefakterna)
- Command: `git status --short` (5. Kontrollera arbetskatalogen: inga M- eller A-rader kvar, bara ?? för lokala filer)
- Studio: Reader: öppna ADR:en under Architecture decisions och hitta Alternatives Considered i dess avsnittslista, och Reversal-raden under Consequences. Använd Explain på ett avsnitt som du inte kan placera. Decisions och Ubiquitous Language finns i sidopanelen.

Steps:

1. **Avgör vägvalet med `decide`.** Peka den på PRD:n. Bekräfta alternativen, kriterierna och vikterna innan den börjar undersöka dem. Den kontrollpunkten är hela poängen. Du har just fattat beslutet, så ADR:en läggs in som `Accepted`.
2. **Läs ADR:en.** Den hamnar i `docs/adrs/` med en rad i `docs/DECISIONS.md`. Hitta Reversal-raden, en envägsdörr eller en tvåvägsdörr, och Alternatives Considered, där basalternativet ingår.

   Stop line: en ensam röd linje, i höjd med Stop-raden i sidokolumnen.

3. **Namnge termerna.** Kör ordlistan för delade listor i en ny session. (AndThen kan sedan föreslå `plan` som nästa steg. Kör den inte än: läs ordlistan och committa i steg 4 och 5 först. Planeringen är F4.)
4. **Läs ordlistan.** Den hamnar i `docs/UBIQUITOUS_LANGUAGE.md`. Dess Avoid-kolumn förbjuder de synonymer som specen inte får använda.
5. **Committa designartefakterna.** Stagea per sökväg, aldrig `git add -A`: `git add docs CLAUDE.md`, eftersom indexet i `CLAUDE.md` också har fått nya rader. Kör sedan `git commit -m "Add shared-lists PRD, ADR and glossary"`.

Verify:

- ADR:en anger ett alternativ, med de kriterier som avgjorde valet.
- Alternatives Considered innehåller basalternativet, och Reversal anger dörrtypen.
- `docs/DECISIONS.md` har en rad för ADR:en.
- Ordlistan har ett namn per begrepp, med förbjudna synonymer under Avoid.

Structure check: Var det här vägvalet värt en ADR? För delningsmodellen, ja. En fråga som bara körbar kod kan besvara går till `spike` i stället.

### F4 – Planera

- Tint: green
- Skills: plan
- Input: PRD:n, ADR:en och ordlistan. plan hittar dem via indexet, så du klistrar inte in något.
- Output: stack · FIS + plan.json · En FIS för den vertikala skivan och en plan.json med en enda story, där story S01 är pending. En vertikal skiva är en tunn bit av funktionen genom alla lager (data, routes, UI, tester) som du kan demonstrera för sig.
- Command: `/andthen:plan docs/specs/let-people-share-their-lists` (1. /andthen:plan <feature-dir>: planera hela PRD:n, i en ny session. AndThen kan sedan föreslå exec-plan: hoppa över det, den här planen är bara till för att läsas)
- Example: 1. Genomarbetat exempel: vad plan skrev → (plan-files)
- Text: 1. Parkera den sedan: flytta plan.json och FIS-filerna till .agent_temp/whole-prd-plan/ och behåll prd.md
- Example: 1. Genomarbetat exempel: vart den parkerade planen tar vägen → (parked)
- Text: 2. Prova för hand först: skriv ett eget FIS-skelett i .agent_temp/f4-my-fis.md
- Example: 2. Genomarbetat exempel: ett FIS-skelett skrivet för hand → (fis)
- Stop: **Stopp.** Gå inte vidare förrän ditt eget skelett ligger i `.agent_temp/f4-my-fis.md` och planen för hela PRD:n är parkerad: när `plan` väl har skrivit sin FIS kan du inte längre skriva ditt eget utan att påverkas.
- Command: `git status --short` (3. Först, före plan: visar prd.md M har plan skrivit in ett av dina svar i PRD:n i steg 1. Committa det, så att kontrollen efter plan förblir ren)
- Command: `git add docs/specs/let-people-share-their-lists/prd.md` (3. Stagea PRD:n per sökväg)
- Command: `git commit -m "Amend the shared-lists PRD from planning"` (3. Committa ändringen i PRD:n)
- Command: `/andthen:plan "docs/specs/let-people-share-their-lists/ as one story: share a list view-only with a registered user, and revoke"` (3. /andthen:plan "<feature-dir>/ as one story: …": planera den vertikala skivan som en story, i en ny session. Läs listorna Decided: och Assumed: som den avslutar med)
- Command: `git status --short` (3. Kontrollera arbetskatalogen: plan.json och FIS:en för den vertikala skivan är de enda nya filerna under docs/. Visar prd.md M igen har plan ändrat den en gång till: steg 5 committar det)
- Text: 4. Jämför FIS:en med ditt skelett och kontrollera att dess Architecture Decision pekar på din ADR
- Example: 4. Genomarbetat exempel: vilka filer du jämför → (compare)
- Command: `git status --short` (5. Före F5, hoppa inte över det här: visar prd.md M har plan skrivit in ett beslut från steg 3 i PRD:n, till exempel vilket avslag en begäran får. Committa det, annars börjar F5 med en smutsig arbetskatalog)
- Command: `git add docs/specs/let-people-share-their-lists/prd.md` (5. Stagea PRD:n per sökväg)
- Command: `git commit -m "Amend the shared-lists PRD from planning"` (5. Committa ändringen i PRD:n)
- Command: `git status --short` (5. Kontrollera att arbetskatalogen är grön: under docs/ är bara plan.json och FIS:en för s01 ocommittade. __pycache__/ och todo.db kan också synas: håll dem utanför alla commits)
- Text: 5. Bocka sedan av punkterna under Verifiera nedan mot FIS:en, framför allt: varje scenario har ett bevis och kan spåras till ett Expected Outcome, och plan.json har en story, S01, pending
- Studio: Plan board: efter steg 1 visar planen för hela PRD:n sina stories som kolumner med sina dependsOn-kanter. Räkna dem innan du parkerar planen. Parkerad i `.agent_temp/` försvinner den från tavlan. Efter steg 3 visar tavlan en story, S01, pending: öppna den för att läsa FIS:en.

Steps:

1. **Planera hela PRD:n, och läs bara.** Kör `plan` på din `<feature-dir>` i en ny session. Läs hur många stories den skapar, deras `dependsOn`-kanter och eventuella `OVERSIZE:`-rader. Flytta sedan `plan.json` och FIS-filerna till `.agent_temp/whole-prd-plan/`. `prd.md` ligger kvar. (AndThen kan sedan föreslå `exec-plan`. Kör den inte: den här planen är bara till för att läsas.)
2. **Prova för hand först: skriv ett eget FIS-skelett.** I `.agent_temp/f4-my-fis.md`: syfte, utfall, tre scenarier, vad du inte gör och uppgifter med en Verify-rad.

   Stop line: en ensam röd linje, i höjd med Stop-raden i sidokolumnen.

3. **Planera den vertikala skivan som en story.** Kör först `git status --short`: visas `prd.md` som ändrad har `plan` skrivit in ett av dina svar i PRD:n i steg 1, så committa den per sökväg. Kör sedan `plan` med den vertikala skivan i en ny session. Läs listorna `Decided:` och `Assumed:` som den avslutar med. (AndThen kan sedan föreslå `exec-plan`. Det är F5, efter steg 5.)
4. **Jämför FIS:en med ditt skelett.** Vad lade den till som du missade, och tvärtom? Kontrollera att dess Architecture Decision pekar på din ADR.
5. **Lämna arbetskatalogen grön före F5 och bocka av Verifiera.** Kör `git status --short` en gång till. Visas `prd.md` som ändrad har `plan` skrivit in ett beslut från steg 3 i PRD:n, så committa den per sökväg. Då är bara `plan.json` och FIS:en ocommittade under `docs/` (`__pycache__/` och `todo.db` kan också synas: håll dem utanför alla commits). Bocka till sist av punkterna under Verifiera nedan mot FIS:en: varje scenario har ett bevis och kan spåras till ett Expected Outcome, och `plan.json` har en story, S01, `pending`.

Verify:

- Varje acceptansscenario är observerbart och har ett bevis.
- Varje scenario kan spåras till ett Expected Outcome.
- What We're NOT Doing är uttryckligt.
- FIS:en följer din ADR och använder ordlistans termer.
- Inga olösta `OVERSIZE:`, och plan.json har en story, S01, pending.

Structure check: Var en FIS lagom mycket? För delning som berör datamodellen och behörigheterna, ja. Visar den sig vara mycket större än den såg ut delar du upp den i stories i stället för att skriva en större spec.

### F5 – Implementera

- Tint: teal
- Skills: exec-plan
- Input: FIS:en och plan.json från F4, i en grön arbetskatalog där bara de två filerna är ocommittade.
- Output: code · Kod + tester · Den vertikala skivan committad, och story S01 done i plan.json med en verifierad sammanfattning.
- Command: `pwd` (1. Kontrollera var du är: sökvägen ska sluta på todo-app)
- Command: `cd todo-app` (1. Gör den inte det går du dit från repots rot)
- Text: 2. Läs ### Implementation Tasks i FIS:en innan du kör den: en uppgift och dess Verify-rad
- Example: 2. Genomarbetat exempel: en uppgift och dess Verify-rad → (task)
- Stop: **Stopp.** Gå inte vidare förrän du kan säga vad en uppgifts Verify-rad bevisar, och bara FIS:en och `plan.json` är ocommittade: `exec-plan` bygger och committar hela storyn i en enda körning.
- Command: `/andthen:exec-plan docs/specs/let-people-share-their-lists/s01-shared-lists.md` (3. /andthen:exec-plan <feature-dir>/s01-<name>.md: kör FIS:en, i en ny session)
- Text: 4. Läs ## Implementation Observations i slutet av FIS:en, <feature-dir>/s01-<name>.md: granskningsrättelser, DRIFT-rader, NOTICED BUT NOT TOUCHING
- Example: 4. Genomarbetat exempel: vad du ska peka ut → (observations)
- Command: `uv run uvicorn app.main:app --reload` (5. Valfritt: starta appen från todo-app/ och öppna sedan adressen som den skriver ut, oftast http://localhost:8000. Stoppa den med Ctrl-C)
- Text: 5. Eller be Claude i Claudes skrivbordsapp: starta appen här och öppna den i webbläsarpanelen
- Text: 5. Logga in som demo@example.com / demo123. Registrera en andra användare med en @example.com-adress i ett privat fönster i din egen webbläsare
- Text: 5. Dela en lista som demoanvändaren från listans inställningar (pennan). Ladda om det andra fönstret, kontrollera ”Shared with me” och återkalla sedan
- Studio: Plan board, öppen under steg 3: S01 flyttas till done när körningen committar, utan att du laddar om. Öppna sedan S01 för dess FIS och diffen för dess ändringar. Läs och skriv anteckningar, men skicka inga medan körningen pågår.

Steps:

1. **Börja i `todo-app/`.** `exec-plan` körs från projektroten, och sökvägen till FIS:en är relativ till den. Kör `pwd` i den nya sessionen: slutar den inte på `todo-app` kör du först `cd todo-app` från repots rot.
2. Läs FIS:en så som agenten kommer att läsa den: en uppgift och dess Verify-rad.

   Stop line: en ensam röd linje, i höjd med Stop-raden i sidokolumnen.

3. Kör den. Se hur uppgifterna körs i tur och ordning och klarar sin kontroll en i taget, följt av den fullständiga beviskörningen och en ny granskare.
4. **Läs vad körningen lämnade i FIS:en.** Öppna `<feature-dir>/s01-<name>.md`, alltså `docs/specs/let-people-share-their-lists/s01-shared-lists.md` i `todo-app/` – samma fil som du gav till `exec-plan` – och scrolla till dess sista avsnitt, `## Implementation Observations`, med `## Discovered Requirements` ovanför om körningen hittade ett krav som specen missade. Där står vad granskaren hittade och hur det rättades. Där står också varje `#### DRIFT`-rad, om det finns någon, där koden medvetet avviker från specen (inget DRIFT-avsnitt betyder att körningen hävdar att koden stämmer med specen, ett påstående som F6 prövar), de små städningarna på vägen, `NOTICED BUT NOT TOUCHING`-punkter som lämnats till senare och varje kontroll som inte kördes. Läs de vanliga punkterna också: en liten omtolkning kan gömma sig i en av dem. Bestäm för var och en: godta den, ta den till F6 eller lämna den till senare. `ship` i F7 behåller det som är värt att behålla och tar bort FIS:en.
5. **Valfritt: prova appen själv.** Gröna tester är inte samma sak som att se den fungera. Starta appen från `todo-app/` med `uv run uvicorn app.main:app --reload`, eller be Claude i Claudes skrivbordsapp starta den och öppna den i webbläsarpanelen. Använd två användare: logga in som demoanvändaren, `demo@example.com` / `demo123`, i ett fönster och registrera en ny användare i ett privat fönster i din egen webbläsare, eftersom flikarna i webbläsarpanelen delar en inloggning. Ge den nya användaren en `@example.com`-adress: registreringen nekar `.test`. Öppna som demoanvändaren en listas inställningar med pennan och dela listan med den nya användarens e-postadress. Ladda om det andra fönstret: listan ligger under ”Shared with me”, utan kontroller för att ändra. Återkalla, ladda om igen, och listan är borta. Stoppa servern med Ctrl-C, eller be Claude stoppa den om det var Claude som startade den.

Verify:

- Story S01 är done, och verified.summary citerar en kontroll som kördes: kommando, slutstatus, resultatrad.
- Du har kört kommandot själv och fått samma resultat.
- `git log -3` visar trailerraderna `Story-ID: S01` och `Plan:`, och `git status` är ren.
- Ingen uppgift är avbockad utan en godkänd Verify.
- Raden `Reviewed:` säger att en ny granskare har tittat, och du vet vad den lämnade öppet.

Structure check: Att testerna går igenom betyder inte att det fungerar. Gröna tester bevisar de scenarier som du skrev. Om det var rätt scenarier är frågan för F6.

### F6 – Verifiera och granska

- Tint: lav
- Skills: review --fix
- Input: Den committade vertikala skivan (en tunn bit av funktionen genom data, routes, UI och tester), plan.json med S01 done och FIS:ens acceptansscenarier som din egen checklista.
- Output: checklist · Granskningsrapport · Fynd sorterade i Fix och Note, där Fix-fynden är genomförda i din arbetskatalog.
- Text: 1. Verifiera själv: hur skulle en läsare kunna skicka en ändring utan knappen? Hitta sedan det som nekar den, i routes och i tests/test_sharing.py
- Command: `uv run pytest` (2. Låt kontrollen i en route som ändrar data släppa igenom en läsare, och kör sedan testerna från todo-app/: minst ett måste fallera)
- Example: 2. Genomarbetat exempel: de tre dragen i referenskörningen → (falsify)
- Command: `git restore src/app/routes/todos.py` (2. Återställ kontrollen med git restore <file>, där <file> är filen som du ändrade. I referenskörningen:)
- Stop: **Stopp.** Gå inte vidare förrän `git status --short src/` inte skriver ut något: granskningen måste läsa din riktiga kontroll, inte den som du ändrade.
- Command: `/andthen:review --fix docs/specs/let-people-share-their-lists/plan.json` (3. /andthen:review --fix <feature-dir>/plan.json: kör granskningen, i en ny session från todo-app/. Jämför rapporten med det som du hittade)
- Example: 3. Genomarbetat exempel: vad granskningen lämnade efter sig → (review-output)
- Text: 4. Avgör själv varje Note i rapporten: rätta den, för in den som teknisk skuld eller stryk den. Ingen ”när jag ändå är här”-städning
- Command: `/clear` (5. Slutar rapporten med Next (fresh session): /andthen:review …? Starta då en ny session)
- Command: `/andthen:review --fix docs/specs/let-people-share-their-lists/plan.json` (5. /andthen:review --fix <feature-dir>/plan.json: kör sedan uppföljningsgranskningen från todo-app/. Upprepa 5 så länge den skriver ut en ny)
- Command: `uv run pytest` (6. Ingen fixrunda kvar? Kör testerna själv från todo-app/)
- Text: 7. Ready, med en Next-rad för ship? Gå till F7. Inte Ready? Läs vad som fortfarande blockerar
- Studio: Review report: öppna den under Review reports. Där finns utlåtandet, fyndindexet, täckningsmatrisen för stickprov på ett scenario och Remediation Status i slutet. En uppföljningsgranskning visas som en andra rapport bredvid den första.

Steps:

1. **Leta själv efter en lucka:** kan en läsare ändra en lista med bara läsrätt genom att skicka begäran direkt? Kontrollera att servern nekar den, och att det inte bara är en dold knapp.
2. **Falsifiera testet.** Ändra kontrollen på serversidan i en route som ändrar data så att den släpper igenom en läsare – använd till exempel läskontrollen i stället för ägarkontrollen. Låt koden fortsätta fungera: kommenterar du bort kontrollen kraschar bara routen, och en krasch får testerna att fallera av fel anledning. Kör `uv run pytest`: minst ett test måste fallera. Återställ sedan kontrollen med `git restore`. Grönt betyder att testsviten ljuger.

   Stop line: en ensam röd linje, i höjd med Stop-raden i sidokolumnen.

3. **Kör granskningen** och jämför rapporten med det som du hittade. Rapporten är inte allt den lämnar efter sig. Med `--fix` genomför den Fix-fynden i din arbetskatalog, utan att committa, och anger varje fynds utfall under `## Remediation Status` i slutet av rapporten. Ett fynd som du skjuter upp förs in i `docs/TECH-DEBT-BACKLOG.md` när du har godkänt det. Körningen avslutas med en `Next`-rad: en uppföljningsgranskning i en ny session om den rättade ett CRITICAL- eller HIGH-fynd, annars `ship`. Din rapport kommer inte att stämma med referenskörningens: andra fynd, andra allvarlighetsgrader, kanske ingen rättelse alls. Steg 4–7 är desamma vad den än hittade.
4. **Avgör själv varje Note:** rätta den, för in den som teknisk skuld eller stryk den. Motstå ”när jag ändå är här”-städning.
5. **Kör uppföljningsgranskningen om rapporten ber om en.** Slutar körningen med `Next (fresh session): /andthen:review … --fix`? Skriv då `/clear` (eller öppna en ny session) och klistra in raden från `todo-app/`. Sessionen som genomförde en rättelse är inte den som ska bedöma den. Uppföljningen kontrollerar rättelserna, kan rätta mer och kan skriva ut en ny sådan rad: gör då steg 5 igen. Kommer ingen uppföljningsrad hoppar du till steg 6.
6. **Kör `uv run pytest` själv** från `todo-app/` när ingen fixrunda återstår. Agenten körde också testerna. Det här är din egen kontroll av dess påstående, och en körning före en senare fixrunda räknas inte längre.
7. **Gå vidare till F7 när den senaste rapporten säger Ready** och slutar med `Next (fresh session):` för `ship`. Inte Ready? Utlåtandet och `## Remediation Status` säger vad som fortfarande blockerar: ett öppet CRITICAL- eller HIGH-fynd, även ett uppskjutet. Lös det först.

Verify:

- Den senaste rapporten säger Ready, utan öppna CRITICAL- eller HIGH-fynd, och slutar med en Next-rad för ship.
- Varje scenario kan spåras till bevis som kördes, och du har gjort stickprov på ett.
- En direkt begäran från en läsare nekas på serversidan, och ett test skulle fallera utan kontrollen.
- Varje Fix är löst, och varje Note är avgjord av dig.
- Varje uppföljningsgranskning som rapporten bad om har körts, och `uv run pytest` går igenom efter den sista fixrundan.

Structure check: En fullständig granskning passar en ändring av behörigheter på routes som ändrar data. En textjustering på en rad behöver bara `review --quick`.

### F7 – Leverera och lämna över

- Tint: rust
- Skills: ship, handoff
- Input: En granskad branch: plan.json med S01 done, en senaste granskningsrapport som säger Ready och Next-raden för ship som den skrev ut. Pull requesten går till din fork.
- Output: pr · Pull request + överlämning · En mergad pull request, nya lärdomar och en överlämning som en ny session kan fortsätta från.
- Command: `git status --short` (1. Från todo-app/: vad är ocommittat? Bara granskningsrättelser, om några. ship committar dem)
- Command: `git log --oneline main..HEAD` (1. De commits som kommer att lämna din dator)
- Command: `git ls-files docs/specs/let-people-share-their-lists` (1. git ls-files <feature-dir>: spårade är prd.md, plan.json och FIS:en. Granskningsrapporten är gitignorerad)
- Stop: **Stopp.** Gå inte vidare förrän steg 1 ser rätt ut: `ship` committar och tar bort `plan.json` och FIS:en utan att fråga.
- Command: `/clear` (2. Starta en ny session)
- Command: `/andthen:ship docs/specs/let-people-share-their-lists/plan.json` (2. /andthen:ship <feature-dir>/plan.json: klistra in Next-raden från F6:s senaste rapport, från todo-app/)
- Text: 3. Nämner den öppet arbete? Svara nej och gå tillbaka till F6. Läs annars vilka lärdomar den skriver och vad den bara rekommenderar
- Text: 4. Läs PR-texten innan du säger ja: syfte, utfall, bevis för vart och ett, envägsdörr eller tvåvägsdörr och vad den lämnar öppet
- Text: 4. Är din fork målet? Säg ja. Ingen fork? Säg nej: den skriver ut titeln, brödtexten och kommandona att köra senare
- Command: `git ls-files docs/specs/let-people-share-their-lists` (5. git ls-files <feature-dir>: bara prd.md finns kvar)
- Command: `git log --oneline --stat -3` (5. Committen med lärdomarna och borttagningen av plan.json och FIS:en)
- Prompt: Visa Implementation Observations för den borttagna FIS:en ur git-historiken bredvid de nya punkterna i docs/LEARNINGS.md. (5. Fråga Claude Code. Varje ny punkt ska gå att spåra till en observation)
- Stop: **Stopp.** Gå inte vidare förrän varje ny punkt i lärdomarna kan spåras till en observation i den borttagna FIS:en: när branchen väl är mergad och borttagen är den historiken borta ur din klon.
- Text: 6. Merga på github.com: öppna pull requesten, välj Squash and merge, bekräfta och klicka sedan på Delete branch
- Command: `gh pr merge https://github.com/gregthebellringer/agentic-engineering-2026-G/pull/2 --squash --delete-branch` (6. Eller härifrån: gh pr merge <PR URL> --squash --delete-branch, med URL:en som ship skrev ut. I referenskörningen:)
- Command: `git switch main` (6. Efter en merge på github.com uppdaterar du din klon: du står fortfarande på funktionsbranchen)
- Command: `git pull` (6. Hämta squash-committen till din main)
- Command: `git branch -D feat/shared-lists` (6. Ta bort den lokala branchen. -D, eftersom git inte ser squash-committen som samma ändringar)
- Stop: **Stopp.** Gå inte vidare förrän `git status -sb` skriver ut `## main...origin/main` och `git branch` inte längre listar `feat/shared-lists`: överlämningen ska beskriva det mergade arbetet. Ingen fork och därför ingen merge? Gå vidare.
- Command: `/andthen:handoff "next: frame my case repo – init, describe, test command"` (7. Lämna över och öppna sedan filen som den skriver under .agent_temp/handoff/)
- Command: `/clear` (8. Starta en ny session)
- Prompt: Resume from .agent_temp/handoff/handoff-<UTC-ts>.md (8. Klistra in raden för att fortsätta som handoff skrev ut, med dess tidsstämpel)
- Prompt: Vad är läget för arbetet med delade listor, och vad är nästa steg? (8. Fråga sedan, utan att skriva in något sammanhang igen)
- Studio: Walkthroughs: innan du mergar i steg 6 tar du fram en genomgång av pull requesten via dess nummer, eller av intervallet `main...feat/shared-lists`. Det är en agentkörning, så ge den några minuter. Gå sedan igenom dess fokuspunkter och markera varje fil som granskad. Efter `ship` visar startsidan 0 plans: `ship` tog bort `plan.json`.

Steps:

1. **Titta innan du levererar.** Kör `git status --short`, `git log --oneline main..HEAD` och `git ls-files <feature-dir>` från `todo-app/`. De enda ocommittade ändringarna ska vara granskningsrättelser, om några: `ship` committar dem och lämnar allt som den inte kan knyta till branchen i fred. Loggen visar det som kommer att lämna din dator: story-committen och eventuella rättelser som committats efter granskningen. `plan.json` och FIS:en är spårade, eftersom `exec-plan` committade dem med storyn. Granskningsrapporten är det inte, eftersom den är gitignorerad.

   Stop line: en ensam röd linje, i höjd med Stop-raden i sidokolumnen.

2. **Kör `ship` i en ny session.** Skriv `/clear` (eller öppna en ny session) och klistra in raden `Next (fresh session):` från F6:s senaste rapport, från `todo-app/`.
3. **Läs vad den gör innan den frågar.** Först kontrollerar den om det finns öppet arbete: en story som inte är done, eller ett öppet CRITICAL- eller HIGH-fynd, även ett uppskjutet. Nämner den något sådant svarar du nej och går tillbaka till F6. Att leverera trots något som blockerar är ett beslut, inte ett standardval. Sedan för den in det som FIS:en lärde ut: de verkliga fällorna i `## Implementation Observations` blir punkter i `docs/LEARNINGS.md`, och resten rekommenderar den bara, till exempel en `Decisions`-rad eller en `decide`-körning. Den committar lärdomarna och eventuella rättelser som ligger kvar i din arbetskatalog, och tar bort `plan.json` och FIS:en, som styr en enda branch och aldrig mergas. `prd.md` ligger kvar. Ingenting har lämnat din dator än.
4. **Läs PR-texten innan du säger ja.** När FIS:en är borttagen och granskningsrapporten stannar lokalt är det PR:en som bär syftet vidare. Kontrollera att den sätter beslutet om merge först: vad ändringen är till för, utfallen, beviset för vart och ett (`verified.summary` och granskningens utlåtande), om den är en envägsdörr eller en tvåvägsdörr och vad som går sönder om den är fel, och vad den medvetet lämnar öppet, till exempel fynden som du sköt upp till teknisk skuld. Commits som gjorts efter den senaste granskningen är markerade: du ska kunna säga varför de inte behöver en ny granskning. Skulle en granskare som aldrig har sett din chatt förstå vad ändringen är till för och hur den bevisades? Är din fork målet säger du ja. Utan fork säger du nej: `ship` skriver ut titeln, brödtexten och kommandona att köra senare.
5. **Kontrollera vad den lämnade.** `git ls-files <feature-dir>` visar bara `prd.md` (`ls` visar också den gitignorerade granskningsrapporten). `git log --oneline --stat -3` visar committen med lärdomarna och borttagningen av `plan.json` och FIS:en. Öppna `docs/LEARNINGS.md` och läs de nya punkterna. FIS:en är borta från branchen men inte ur historiken, så be Claude visa dess observationer bredvid dem: varje punkt ska gå att spåra till en observation.

   Stop line: en ensam röd linje, i höjd med Stop-raden i sidokolumnen.

6. **Merga pull requesten.** GitHub låter dig inte godkänna din egen pull request, och din fork kräver inget godkännande, så det är mergen som är beslutet. Merga på github.com eller med `gh` härifrån: båda ger samma resultat. Webbsidan är rekommendationen: du ser exakt vad som mergas, du väljer merge-metod med ett klick, och det är så de flesta team arbetar. Välj **Squash and merge**, bekräfta och klicka på **Delete branch**. Branchen blir en enda commit på `main`, och `plan.json` och FIS:en, som lades till och togs bort på branchen, når aldrig historiken på `main`. Därför kommer steg 5 först: när branchen är borta finns FIS:en bara kvar i pull requesten på GitHub. Härifrån gör `gh pr merge <PR URL> --squash --delete-branch` samma sak med URL:en som `ship` skrev ut. Uppdatera sedan din klon, eftersom du fortfarande står på funktionsbranchen: `git switch main`, `git pull` och `git branch -D feat/shared-lists`. Det sista kommandot kräver `-D`, eftersom git inte ser squash-committen som samma ändringar. Mergade du med `gh … --delete-branch`? Då har den redan bytt till `main` och tagit bort den lokala branchen, så kör bara `git pull`. Ingen pull request, eftersom du saknar fork? Hoppa över det här steget.

   Stop line: en ensam röd linje, i höjd med Stop-raden i sidokolumnen.

7. **Lämna över.** Kör `handoff` med nästa fokus. Den skickar varaktig kunskap till `docs/LEARNINGS.md`, rekommenderar en `decide`-körning för ett strukturellt beslut i stället för att skriva en ADR och skriver resten till `.agent_temp/handoff/handoff-<UTC-ts>.md`: nästa fokus, var du står, öppna frågor, vad som har prövats, nästa skill och ett index över artefakter per sökväg. Öppna filen: den ska ange artefakter med sökväg, inte klistra in dem. Hemligheter maskeras, men filen är inte privat.
8. **Testa överlämningen.** Skriv `/clear` (eller öppna en ny session), klistra in raden `Resume from …` som `handoff` skrev ut och fråga vad läget är för arbetet med delade listor och vad nästa steg är. Den nya sessionen ska svara utifrån överlämningen och filerna som den pekar på, utan att du skriver in något igen. Klarar den inte det rättar du överlämningen, inte prompten.

Verify:

- PR-texten anger syfte, utfall, bevis per utfall och dörrtyp med vad som går sönder om den är fel, före alla detaljer per story.
- plan.json och FIS:en är borta från branchen, och prd.md finns kvar.
- Varje ny punkt i lärdomarna kan spåras till en Implementation Observation i FIS:en i git-historiken.
- Pull requesten är squash-mergad, och din klon står på en uppdaterad `main` där funktionsbranchen är borttagen.
- Överlämningen anger artefakter med sökväg i stället för att klistra in dem.
- En ny session kunde fortsätta enbart utifrån överlämningen.

Structure check: En plan är värd hela avslutet. En rättelse som ryms i en mening kör `implement-fix` och sedan `ship`. En kort uppgift som blir klar under ett och samma pass behöver ingen överlämning.


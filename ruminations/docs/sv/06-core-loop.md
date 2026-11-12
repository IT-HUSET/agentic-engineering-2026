---
title: Core Loop i AndThen
tab: Core Loop
token: loop
order: 6
depends_on: [shared/skills.md, shared/icons.md]
---

# Core Loop

Eyebrow: Arbetsflödet du ska öva på

## Från en luddig idé till en verifierad pull request

AndThen kedjar ihop några skills till Core Loop. Varje steg skriver något som nästa steg läser, och avslutar med att skriva ut kommandot du ska klistra in härnäst.

Formula: idé → [clarify] → plan → exec-plan → review --fix → ship

Component: formeln som en rad i mono, med en röd prick före ”idé” och [clarify] nedtonad.

## Hur mycket struktur behöver arbetet?

Interactive component: tre pillerformade knappar, en per väg. Den valda vägen styr texten under knapparna, stegraden och kommandona i stegkortet. Förvald väg: feature, steget plan.

| Path | Label | Start | Steps | Note |
| - | - | - | - | - |
| feature | En funktion | idé | clarify, decide, plan, exec-plan, review, ship | En riktig funktion går igenom hela Core Loop med en enda FIS. Börja med clarify om du inte kan räkna upp tre acceptanskriterier. Annars börjar du med plan. |
| several | Flera funktioner | idé | clarify, decide, plan, exec-plan, review, ship | Flera funktioner går igenom samma Core Loop, men med en plankatalog. plan delar upp arbetet i stories, och exec-plan bygger dem en story i taget, eller hela katalogen i ett svep. |
| fix | En rättelse på en mening | rättelse | triage, implement-fix, ship | En rättelse som du kan beskriva i en mening hoppar över specen. Okänd orsak eller trasigt bygge? Kör triage först. |

Component: stegraden. Startetiketten med en röd prick, sedan varje steg som ett piller med nummer, namn och ”valfritt” när det gäller (streckad ram). Under varje piller en tagg med ikonen och Tag från stegets Result i shared/skills.md. Mellan stegen en markering ”/clear”. Piltangenterna flyttar längs raden.

## Steg

Component: stegkort för det valda steget, tonat med stegets Tint, med nummer, Role, Title, Summary och When, en nedtonad ruta under When när steget har en Note för den valda vägen, sedan en resultatruta (ikon, titel och text från shared/skills.md), Reads, kommandona med kopieringsknappar, en remsa ”I AndThen Studio” när steget har fältet Studio (lavendel, med texten och en länk till fliken Studio), raden ”Kör sedan /clear och klistra in nästa kommando” och knapparna Föregående och Nästa. På sista steget lyder raden ”Det var Core Loop. Pull requesten är öppen.” Varje kommandoruta är dold från början bakom knappen ”Visa kommando”, som på fliken Installation.

Hint under the card: Välj ett steg på raden, eller använd piltangenterna. Streckade steg är valfria.

Kommandona kan skilja sig mellan vägarna. En rad `Command (several): …` gäller bara den vägen, och det gör även `Note (several): …`, vars fetstilta inledning blir rutans etikett. Ett kommando med en anteckning visar anteckningen ovanför kommandot.

### clarify

- Skill: clarify
- Tint: rust
- Optional: yes
- Role: Krav
- Title: Klargör vad du vill
- Summary: Intervjuar dig om en vag idé: luckorna, kantfallen och omfånget. Sedan skriver den PRD:n.
- When: **Valfritt.** Hoppa över steget när kraven redan finns. Ingångstest: kan du inte räkna upp tre acceptanskriterier börjar du här.
- Reads: Din idé, med dina egna ord
- Command: `/andthen:clarify`
- Studio: Reader: öppna PRD:n under Requirements, läs den avsnitt för avsnitt och fäst en anteckning vid det du tvivlar på.

### decide

- Skill: decide
- Tint: red
- Optional: yes
- Role: Beslut
- Title: Avgör de dyra valen
- Summary: Avgör ett tekniskt val som påverkar mer än en story eller är dyrt att backa från, och dokumenterar det som en ADR.
- When: **Valfritt.** Körs mellan clarify och plan. Följeslagaren `domain --mode glossary` slår fast ett namn per begrepp.
- Reads: PRD:n och den öppna tekniska frågan
- Command: `/andthen:decide`; `/andthen:domain --mode glossary` (Ett namn per begrepp)
- Studio: Reader: ADR:en under Architecture decisions, och Decisions och Ubiquitous Language i sidofältet. Använd Explain på ett avsnitt du inte kan placera.

### plan

- Skill: plan
- Tint: cream
- Role: Specifikation
- Title: Skriv specen
- Summary: Skriver Feature Implementation Specification (FIS): vad som ska byggas, beviset för varje acceptansscenario och när arbetet är klart.
- When: **Ingen kod ändras.** Det är plan som avgör om arbetet är en story eller flera.
- Reads: PRD:n, eller krav som du redan har
- Command (feature): `/andthen:plan`
- Command (several): `/andthen:plan <dir>`
- Studio: Plan board: stories som kolumner med sina beroenden. En story öppnar sin FIS.

### exec-plan

- Skill: exec-plan
- Tint: green
- Role: Implementation
- Title: Bygg mot specen
- Summary: Bygger en FIS, eller kör en plankatalog med en ny subagent per story. En story är done först när det finns en citerad rad från en kontroll som faktiskt kördes, och en ny granskare kontrollerar var och en. Varje färdig story får sedan en förenklingsrunda, och det den upptäckte förs in i FIS-filerna för stories som inte har börjat.
- When: **Låt den vara medan den kör.** Redigera inte kod för hand mitt i en körning. Låt den bli klar, eller stoppa och ändra i FIS:en.
- Reads: En FIS, eller en plankatalog
- Command (feature): `/andthen:exec-plan <FIS>`
- Command (several): `/andthen:exec-plan <first ready FIS>` (Raden som plan skriver ut: en story i taget, och varje körning anger nästa); `/andthen:exec-plan <dir>` (Eller alla stories i ett svep); `/andthen:exec-plan <dir> --worktree` (Kör oberoende stories parallellt)
- Studio: Plan board, som du låter stå öppen: storyn flyttar till done när körningen committar, och den öppnar diffen för sina ändringar.

### review --fix

- Skill: review
- Tint: teal
- Role: Granskning
- Title: Granska helheten
- Summary: Granskar det färdiga arbetet som helhet: hur väl det följer specen, kod, säkerhet och utfall. Sedan ger den utlåtandet PASS eller FAIL, genomför fynden som är markerade Fix och committar dem.
- When: **Hela ändringen på en gång.** exec-plan har redan kontrollerat varje story. Det här steget tittar på hur de passar ihop.
- Reads: Den färdiga ändringen och dess spec
- Command: `/andthen:review --fix`
- Studio: Review report: utlåtandet, fyndindexet och `## Remediation Status`, en rapport per granskningsomgång.

### ship

- Skill: ship
- Tint: lav
- Role: Leverans
- Title: Leverera
- Summary: Sparar lärdomarna, öppnar pull requesten efter ett enda ja från dig och erbjuder att ta bort planfilerna när alla stories är klara.
- When: **Du har kontrollen.** Ingenting öppnas förrän du säger ja.
- Reads: Det granskade arbetet och dess planfiler
- Command: `/andthen:ship`
- Note (several): **Är bara en del av planen byggd?** `ship` kontrollerar det först. Finns det stories kvar namnger den dem och frågar en gång om du vill skeppa ändå. Den rekommenderar att planen behålls: `plan.json` och FIS-filerna ligger kvar, följer med i pull requesten tillsammans med arbetet och läses av de stories som återstår. Även steget med Learnings väntar. Pull requesten anger vad som fortfarande är öppet. Den sista `ship`, när alla stories är klara och granskade, för in lärdomarna i Learnings och frågar om planen ska tas bort, och rekommenderar ja. `prd.md` ligger kvar, med en Shipped-rad.
- Studio: Walkthroughs: en guidad tur genom pull requesten innan du mergar den. Efter den sista `ship` är Plan board tom, eftersom den raderar `plan.json`.

### triage

- Skill: triage
- Tint: red
- Optional: yes
- Role: Diagnos
- Title: Hitta orsaken först
- Summary: Undersöker problemet ner till grundorsaken, rättar det under ett test som fallerar och committar rättelsen. --plan-only stannar vid planen för rättelsen.
- When: **Valfritt.** Bara när orsaken är okänd eller bygget är trasigt. Beskriv symptom, inte lösningar.
- Reads: Symptom: fel, tester som fallerar, loggar
- Command: `/andthen:triage`

### implement-fix

- Skill: implement-fix
- Tint: rust
- Role: Liten rättelse
- Title: Gör rättelsen
- Summary: För en rättelse som du kan beskriva i en mening. Den hoppar över specen och går direkt till en verifierad ändring, som den committar.
- When: **Lagom mycket struktur.** Kan du inte säga det i en mening är det en funktion. Använd plan i stället.
- Reads: Det du ber om, i en mening
- Command: `/andthen:implement-fix "<request>"`
- Studio: Walkthroughs: ett git-intervall som `main...HEAD` ger en tur genom rättelsen före ship.

## Produkt och PRD – PRODUCT.md och prd.md: krav på två nivåer

`clarify` skriver båda, men på olika nivåer. `docs/PRODUCT.md` beskriver hela produkten, och det finns ett per projekt. `prd.md` beskriver en enskild funktion, och varje funktion får en egen, i sin mapp under `docs/specs/`.

Component: två tonade kort bredvid varandra med en pil och en etikett emellan (staplade, med en pil nedåt, under 1080 px), i samma stil som korten i Plan, stories och FIS. Varje kort har en eyebrow, filnamnet i monospace, en kort text, sina rader och en anteckning. Under korten hur clarify väljer nivå som en underrubrik och en ingress, och sist tumregeln i en nedtonad ruta.

### Dokumenten

#### docs/PRODUCT.md

- Eyebrow: Produkt · ett per projekt
- Tint: teal
- Arrow: avgör storleken
- Text: Vad produkten är, och hur stort det som byggs får bli. Dokumentet ligger ovanför alla PRD:er.
- Row: Innehåll · vision, principer, målgrupper, värdeerbjudande, icke-mål och mått på framgång
- Row: Proportionality · fas, skala och tekniska icke-mål
- Row: Non-Goals · koncept som är uttryckligen avvisade. Varje `clarify` på funktionsnivå håller dem aktuella åt båda hållen: ett koncept som du avvisar får en daterad punkt, och ett som funktionen nu tillåter snävas in eller tas bort
- Row: Skrivs av · `clarify` på produktnivå, eller den första av `clarify`, `decide`, `plan`, `architecture` och `domain` som behöver uppgifterna under Proportionality
- Row: Läses av · alla skills som föreslår något
- Note: Lever länge. Fasen och skalan ändras sällan, men icke-målen följer med de funktioner som `clarify` skriver.

#### prd.md

- Eyebrow: Funktion · en per funktion
- Tint: cream
- Text: Vad en enskild funktion ska göra, och hur du vet att den är klar. Den ligger i funktionens mapp, `docs/specs/<feature>/`.
- Row: Innehåll · problemet, kraven (FR1, FR2 …) med prioritet, vad som ingår och inte ingår, MVP-gränsen, begränsningar och en beslutslogg
- Row: Skrivs av · `clarify` på funktionsnivå, som är standardläget
- Row: Läses av · `plan`, som gör en FIS av den, och `review` med linsen outcome
- Row: Shipped · `ship` lägger till en Shipped-rad när den tar bort planen. En ändring via `clarify` tar bort raden
- Note: PRD:n förankras i produkten. I labbets PRD om delade listor faller e-post och notifieringar bort, eftersom `docs/PRODUCT.md` anger en prototyp med en enda SQLite-fil och inga externa tjänster. `clarify` stryker eller flaggar förmågor som de uppgifterna inte bär, och hänvisar till dem. En beställning som går emot ett icke-mål lyfts fram i stället för att tyst diskuteras bort: i labbet är delning först ett icke-mål, så att gå emot det är ditt beslut, och du säger det uttryckligen.

### Så väljer clarify nivå

Funktionsnivå är standard och ger en `prd.md`. Produktnivå gäller när du säger det själv (”clarify the product vision”), när indata är en fil som heter `PRODUCT*.md`, eller när beställningen handlar om vision, positionering eller produktstrategi. Då skriver `clarify` Product-dokumentet i stället för en PRD.

### Tumregel

Tip: Det som handlar om vad produkten är, och hur stor den får bli, hör hemma i `PRODUCT.md`. Det som handlar om vad en funktion ska göra, och hur du vet att den är klar, hör hemma i `prd.md`.

## Plan, stories och FIS – Så hänger planen, dess stories och deras specar ihop

`plan` skriver två sorters filer: en `plan.json` för plankatalogen och en FIS per story. En story är en slice av arbetet, och varje FIS hör till exakt en story. Tasks finns bara inuti en FIS. Även en enskild funktion får en `plan.json`, med en enda story, S01.

Component: tre tonade kort med pilar och etiketter emellan (staplade, med pilar nedåt, under 1080 px): PRD:n, sedan plan.json med sina stories som rader (den första markerad) och sist den storyns FIS med sina fyra delar. En streckad ram visar att PRD:n är valfri. Varje kort har en eyebrow, filnamnet i monospace, en kort text, sina rader och en anteckning. Under diagrammet reglerna för slices som fyra vita kort med siffror i rost (två i bredd under 1080 px, ett på en telefon) och sist namntipset i en nedtonad ruta.

### Filerna

#### prd.md

- Eyebrow: Krav · valfri
- Tint: cream
- Arrow: plan
- Text: Vad arbetet ska åstadkomma, från `clarify`. `plan` kan också utgå från krav som du redan har, ett ärende i trackern eller en beskrivning på en rad.

#### plan.json

- Eyebrow: En per plankatalog
- Tint: rust
- Arrow: fis
- Text: Planens tillstånd. För varje story: beroenden (`dependsOn`), status, vilka tasks i FIS:en som är klara (`completedTaskIds`) och en pekare till FIS:en. `plan` skriver filen, och sedan uppdaterar den session som bygger en story storyns rad. Där står inget om hur något ska byggas. Filen finns bara på branchen. `ship` tar bort den när du säger ja. Behåller du den får den en `shipped`-markering som dokumentation.
- Row: S01 · Listor har ägare · `s01-listor-har-agare.md` · done
- Row: S02 · Dela en lista · beror på S01 · in-progress
- Row: S03 · Sortera efter förfallodatum · inga beroenden · done
- Row: S04 · Återkalla en delning · beror på S02 · pending
- Note: Mitt i en körning: S01 och S03 är klara, S02 byggs och S04 väntar på S02. En story blir done bara tillsammans med `verified`: när, och vilken kontroll som faktiskt kördes och visade det. skipped sätter du bara för hand.
- Note: En story är en leveransbit, inte en user story i agil mening (”Som användare vill jag …”). Det som ligger närmast en sådan är acceptansscenarierna i FIS:en.

#### s01-listor-har-agare.md

- Eyebrow: FIS · en per story
- Tint: green
- Text: Specen för en story: vad som ska byggas, hur varje del bevisas och när storyn är klar.
- Row: OC01 … · Expected Outcomes · två till fyra, en mening var
- Row: S01 … · Acceptance Scenarios · Given, When, Then, var och en med sitt bevis (Proof)
- Row: SC01 … · Structural Criteria · det som storyns diff inte får förstöra
- Row: TI01 … · Implementation Tasks · ett tillstånd som ska vara sant, med Verify (kontrollen som visar det) och SATISFIES (de scenarier som tasken för framåt)
- Note: `plan.json` sparar bara vilka tasks som är klara, i `completedTaskIds`, så att en avbruten körning kan fortsätta där den slutade.

### När blir det Vertical Slices

`plan` avgör det i sitt steg 3, One story or several. En story är per definition en vertikal slice: något du kan demonstrera genom alla lager.

1. **En story när arbetet ryms.** Arbetet förblir en story när det är en vertikal slice som ryms i en enda exec-körning med ny kontext och lite marginal, ungefär 12 tasks.
2. **Annars så få slices som möjligt.** `plan` delar upp arbetet i så få stories som täcker källan, utan överlapp. Den delar aldrig upp efter lager, som endpoint, handler och UI var för sig.
3. **För stort delas tunnare.** En story som kommer tillbaka med `OVERSIZE:` delas i tunnare vertikala slices.
4. **Gränser och överlapp.** Där modulgränserna är starka delas arbetet längs dem, och `sharedDecisions` låser gränssnittet. Stories som skulle röra ungefär samma filer slås ihop, utom ett gående skelett: när huvudflödet går genom flera stories är den första dess tunnaste väg genom hela flödet, och de stories som bygger på den beror på den.

### Se upp med namnen

Tip: Två nummerserier börjar med S. Story-id:n i `plan.json` heter `S01`, `S02` …, och det gör även acceptansscenarierna i en FIS. I en FIS anger `**Story-ID**: S03` storyn, medan `S01 [OC01]` längre ner är ett scenario.

## Parallella stories – Så avgör AndThen vad som kan köras samtidigt

Bara en plankatalog kan köra stories parallellt, och bara när du lägger till `--worktree`. En enskild FIS byggs alltid i ett stycke. Två skills delar på beslutet: `plan` drar upp beroendena när den delar upp arbetet i stories, och `exec-plan` läser dem igen före varje omgång.

Component: exempelplanen som en liten tabell och sedan två banor, en per kommando. Varje bana har sitt kommando i monospace, stories som piller med pilar emellan och en nedtonad förklaring. Stories som körs samtidigt ligger staplade i en streckad ruta märkt ”samtidigt”, och banan med --worktree har en markering ”merge” efter varje omgång. Under banorna tre vita kort med siffrorna 01–03 i rost, som reglerna, och förutsättningarna som en nedtonad rad. Staplade på en telefon.

### Exempelplan

| Story | Namn | Beror på |
| - | - | - |
| s01 | Listor har ägare | – |
| s02 | Dela en lista | s01 |
| s03 | Sortera efter förfallodatum | – |
| s04 | Återkalla en delning | s02 |

### Banor

Box label: samtidigt
Merge label: merge

- `/andthen:exec-plan <dir>` · s01 → s03 → s02 → s04 · En story i taget, i planens ordning när var och en blir redo, eftersom alla delar samma arbetskatalog och samma testkörning.
- `/andthen:exec-plan <dir> --worktree` · [s01, s03] → merge → s02 → merge → s04 → merge · s01 och s03 beror inte på något, så de startar samtidigt, var och en i sitt eget worktree. s02 väntar tills s01 är mergad, och s04 väntar på s02.

### Vem avgör

1. **plan drar upp beroendena.** `dependsOn` innehåller bara orsakssamband: en story beror på en annan bara när den använder något som den andra storyn skapar, ett kontrakt eller ett beslut. Stories som skulle röra ungefär samma filer slås ihop till en, och ett gränssnitt som två stories delar låses i `sharedDecisions`. plans sista rad anger `exec-plan` på FIS:en för den första storyn som är redo, och varje körning anger nästa. Att köra hela katalogen, med eller utan `--worktree`, är ditt val.
2. **exec-plan tar en våg i taget.** Före varje omgång läser den `plan.json` igen och tar de stories vars beroenden är klara. Med `--worktree` startar den upp till ungefär fem av dem samtidigt, var och en som en ny subagent på en egen branch, `story/<id>`, i ett eget worktree.
3. **Mergen har sista ordet.** Varje färdig story mergas med `git merge --no-ff` innan nästa omgång startar, så att de stories som beror på den utgår från en bas som har dess arbete. En mergekonflikt gör att storyn misslyckas, utom när båda sidor bara har lagt till rader i ett dokument som bara växer, till exempel Learnings. En misslyckad story behåller sitt worktree, och de stories som beror på den hoppas över. Efter varje mergad omgång körs en förenklingsrunda över dess stories, och det de upptäckte förs in i FIS-filerna för stories som inte har börjat.

Förutsättningar: `--worktree` stoppar före den första storyn om en spårad fil har ändringar som inte är committade, eller om `plan.json` inte är committad. Ett worktree innehåller bara det som är committat.

## Regler för Core Loop – Små steg, rena överlämningar

Component: tre vita kort med siffrorna 01–03 i rost.

1. **Varje skill fungerar fristående.** Börja i det steg som passar. Är kraven redan skrivna? Gå direkt till `plan`.
2. **Varje steg skriver ut nästa kommando.** När ett steg är klart är det sista det visar kommandot du ska klistra in för nästa steg.
3. **En ny session per steg.** Kör `/clear` mellan stegen. Filerna på disken för arbetet vidare, så varje skill utgår från specen i stället för från en lång chatt.

## Nästa

Component: en rad knappar som byter flik. Den första är fylld, de andra har bara kontur.

- Gör Foundation Lab → (lab)
- Andra vägar, och vad varje steg lämnar efter sig → (paths)
- Använd AndThen Studio → (studio)

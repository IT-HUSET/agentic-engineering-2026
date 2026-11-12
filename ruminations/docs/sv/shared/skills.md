---
title: Skills i AndThen
andthen_version: 1.1.0
source: ~/.claude/plugins/marketplaces/andthen/plugin/skills/*/SKILL.md
used_by: [03-init, 04-skills, 06-core-loop]
---

# Skills i AndThen

Förteckningen över alla skills i AndThen 1.1.0. Antalet skills som sidan visar räknas fram ur den här filen och skrivs aldrig in för hand.

## Grupper

Ordningen här är ordningen på skill-kartan och i översiktstabellen. Tint-namnen syftar på tint-tokens i kontraktet.

| Id | Label | Tint |
| - | - | - |
| start | Start & session | cream |
| share | Delning & uppföljning | teal |
| design | Design & utforskning | lav |
| core | Core Loop | rust |
| quality | Kvalitet | green |
| fix | Fixvägen | red |

## Skills

Fält per skill: Group, Role (den korta raden på kartan), Optional, Map (x, y, bredd och höjd på kartan, som är 1280 × 605), Document (artefaktchippet under en ruta i Core Loop), Summary, When, Reads, Command, Works with och Result (ikon · titel · text, plus Tag för den korta etiketten på stegraden i Core Loop).

### now-what

- Group: start
- Role: visar vägen
- Map: 215, 74, 140, 50
- Summary: Vägvisaren du går till först. Den går igenom projektets läge och talar om vilken skill du ska köra härnäst.
- When: Kör den när du inte vet var du ska börja, eller när du har kört fast.
- Reads: Projektet som det ser ut nu
- Command: `/andthen:now-what`
- Works with: init, clarify, plan, implement-fix, triage
- Result: compass · Nästa steg · Vilken skill du ska köra härnäst, utifrån läget i projektet. Ingenting skrivs till disk.

### init

- Group: start
- Role: lägger grunden
- Map: 375, 74, 140, 50
- Summary: Lägger upp strukturen för AndThens arbetsflöde, i ett nytt projekt, i ett projekt som är delvis förberett eller i en befintlig kodbas.
- When: En gång per projekt, före det första riktiga steget.
- Reads: Projektmappen
- Command: `/andthen:init`
- Works with: now-what, describe
- Result: folder · Arbetsflödets struktur · De mappar och dokument från AndThen som övriga skills förutsätter.

### handoff

- Group: start
- Role: sparar till senare
- Map: 535, 74, 140, 50
- Summary: Komprimerar konversationen till ett överlämningsdokument som en ny session kan fortsätta från.
- When: Före /clear, när kontexten börjar ta slut eller när du avslutar ett arbetspass.
- Reads: Den pågående konversationen
- Command: `/andthen:handoff`
- Works with: now-what
- Result: handoff · Överlämningsdokument · Det en ny session behöver för att fortsätta där du slutade.

### visualize

- Group: share
- Role: ritar artefakter
- Map: 740, 74, 150, 50
- Summary: Ritar en AndThen-artefakt som en HTML-sida med SVG-figurer: en plan, en spec, en rapport, en ADR, Domain Map eller ordlistan.
- When: När ett dokument är lättare att diskutera som en bild.
- Reads: Vilken AndThen-artefakt som helst
- Command: `/andthen:visualize <artifact>`
- Works with: plan, decide, domain, describe, review
- Result: image · HTML-sida · En fristående sida som ritar artefakten med SVG-figurer.

### tracker

- Group: share
- Role: ärenden
- Map: 910, 74, 150, 50
- Summary: Sköter ärendena i trackern. publish gör om en PRD och dess plan till ett huvudärende med ett underärende per story, triage sätter etiketter på inkommande ärenden och skickar dem rätt, och setup skriver dokumentet om trackern.
- When: När arbetet finns i ärenden. Dess triage sorterar ärenden. Skillen triage felsöker när något fallerar.
- Reads: En PRD, en plan.json eller inkommande ärenden
- Command: `/andthen:tracker publish <plan.json>`
- Works with: clarify, plan
- Result: ticket · Ärenden i trackern · Ett huvudärende för PRD:n och ett underärende per story.

### describe

- Group: design
- Role: kartlägger koden
- Map: 215, 194, 180, 50
- Summary: Dokumenterar vad ett befintligt projekt redan är: arkitekturdokument och de krav som går att läsa ut ur koden. --model lägger till en typad arkitekturmodell.
- When: I en befintlig kodbas (brownfield), innan du ändrar den.
- Reads: Den befintliga kodbasen
- Command: `/andthen:describe`
- Works with: init, architecture, domain, visualize
- Result: map · Arkitekturdokument · Hur koden är byggd i dag, plus de krav som går att läsa ut ur den. --model lägger till en typad modell.

### domain

- Group: design
- Role: namn & kontexter
- Map: 422, 194, 180, 50
- Summary: Modellerar domänen: subdomäner, bounded contexts, event storming och ordlistan som slår fast ett namn per begrepp.
- When: När samma sak har flera namn, eller när en produkt spänner över flera kontexter.
- Reads: PRD, kod och samtal
- Command: `/andthen:domain --mode glossary`
- Works with: decide, plan, describe, visualize
- Result: book · Domain Map + ordlista · Bounded contexts och hur de hänger ihop, och ett namn per begrepp.

### architecture

- Group: design
- Role: råd om struktur
- Map: 629, 194, 180, 50
- Summary: Arkitekturråd och strukturanalys: hur något ska struktureras eller delas upp, hälsogranskningar och fitness functions.
- When: När frågan är ”hur ska det här struktureras?” snarare än ”vilket alternativ väljer vi?”.
- Reads: Kod, dokument och frågan
- Command: `/andthen:architecture --mode advise`
- Works with: decide, describe, domain
- Result: layers · Arkitekturrapport · Råd om struktur, en hälsogranskning eller fitness functions.

### spike

- Group: design
- Role: prövar en idé
- Map: 836, 194, 180, 50
- Summary: Besvarar en namngiven designfråga med en körbar spike som slängs efteråt, och lämnar ett utlåtande. Det är belägg, inte produkt.
- When: När du behöver veta om ett angreppssätt fungerar innan du specificerar det.
- Reads: En designfråga
- Command: `/andthen:spike "<question>"`
- Works with: decide, plan
- Result: flask · Utlåtande · Ett svar på en designfråga, grundat på belägg. Spike-koden slängs.

### ui-ux-design

- Group: design
- Role: skärmar & flöden
- Map: 1043, 194, 180, 50
- Summary: UI- och UX-design: research, designsystem, wireframes och klickbara mockups, var för sig eller i en kedja.
- When: När funktionen har skärmar eller flöden som är värda att skissa innan de specificeras.
- Reads: Krav och befintligt UI
- Command: `/andthen:ui-ux-design`
- Works with: plan, visual-validation
- Result: wireframe · Wireframes · Skärmar och flöden som wireframes, eller som klickbara mockups när det finns ett designsystem.

### clarify

- Group: core
- Role: krav
- Optional: yes
- Map: 215, 318, 140, 64
- Document: prd.md
- Summary: Intervjuar dig i flera omgångar om luckor, kantfall, omfång och alternativ tills förståelsen är gemensam, och skriver sedan PRD:n. --brief stannar vid intent.md.
- When: Valfritt. Börja här om du inte kan räkna upp tre acceptanskriterier.
- Reads: Din idé, en fil eller ett ärende i trackern
- Command: `/andthen:clarify "<idea>"`
- Works with: plan, decide, tracker, now-what
- Result: doc · prd.md · Product Requirements Document, kravdokumentet för produkten. Med --brief blir det en kortare intent.md.
- Tag: prd.md

### decide

- Group: core
- Role: dokumenterar val
- Optional: yes
- Map: 389, 318, 140, 64
- Document: ADR:er
- Summary: Intervjuar dig om de tekniska val som lösningen kräver, rekommenderar ett alternativ för varje val, väger ett omstritt val i en avvägning och skriver ADR:er.
- When: Valfritt. För ett val som påverkar mer än en story eller är dyrt att backa från.
- Reads: PRD:n eller den öppna frågan
- Command: `/andthen:decide`
- Works with: clarify, plan, architecture, domain, spike
- Result: seal · ADR · En Architecture Decision Record för varje val som är avgjort, och PRD-raderna som den avgör hänvisar nu till den. domain lägger till en ordlista.
- Tag: ADR

### plan

- Group: core
- Role: specen
- Map: 563, 318, 140, 64
- Document: FIS + plan.json
- Summary: Skriver Feature Implementation Specification: vad som ska byggas, beviset för varje acceptansscenario och när arbetet är klart. En story, eller en plan.json med en FIS per story.
- When: Alltid. Här ändras ingen kod.
- Reads: PRD, kravfil, ärende i trackern eller det du ber om
- Command: `/andthen:plan <prd.md>`
- Works with: clarify, decide, exec-plan, domain, ui-ux-design, spike, tracker
- Result: stack · FIS + plan.json · En Feature Implementation Specification per story, och en plan.json som listar alla stories.
- Tag: FIS + plan.json

### exec-plan

- Group: core
- Role: bygger
- Map: 737, 318, 140, 64
- Document: kod + tester
- Summary: Bygger en FIS, eller kör en plankatalog med en ny subagent per story. En story är done först när ett bevis faktiskt har körts, och en ny granskare kontrollerar var och en.
- When: Alltid. --worktree kör oberoende stories parallellt. Stories skrivs test först där teststrategin eller din beställning kräver det. Redigera inte för hand mitt i en körning.
- Reads: En FIS eller en plankatalog
- Command: `/andthen:exec-plan <FIS | dir>`
- Works with: plan, review, testing, simplify-code, visual-validation
- Result: code · Kod + tester · Fungerande kod, där varje story är markerad done på en kontroll som faktiskt kördes.
- Tag: kod + tester

### review

- Group: core
- Role: granskar helheten
- Map: 911, 318, 140, 64
- Document: granskningsrapport
- Summary: Den enda granskningsskillen. Den har linserna code, gap (mot FIS:en), security och outcome (mot PRD:n), plus granskning av PR:er. Fynden sorteras i Fix eller Note, och --fix genomför dem.
- When: Alltid, efter exec-plan.
- Reads: Ändringen, dess FIS och dess PRD
- Command: `/andthen:review --fix`
- Works with: exec-plan, ship, implement-fix, simplify-code, visual-validation
- Result: checklist · Granskningsrapport · Fynd sorterade i Fix och Note, med utlåtandet PASS eller FAIL. --fix genomför och committar Fix-fynden.
- Tag: granskningsrapport

### ship

- Group: core
- Role: öppnar PR:en
- Map: 1085, 318, 140, 64
- Document: pull request
- Summary: Sparar det som är värt att behålla ur Implementation Observations och committar. Efter en enda fråga pushar den, öppnar pull requesten och raderar eller behåller planpaketet.
- When: Sist. Ingenting pushas förrän du säger ja.
- Reads: Branchen och dess plan
- Command: `/andthen:ship`
- Works with: review, implement-fix
- Result: pr · Pull request · Lärdomarna sparade, och efter ditt ja är PR:en öppnad och planfilerna borttagna. prd.md ligger kvar, märkt Shipped.
- Tag: pull request

### testing

- Group: quality
- Role: tester & TDD
- Map: 215, 499, 180, 50
- Summary: Teststrategi, täckning och testskrivande på alla nivåer, test först där det krävs, och Prove-It-flödet för buggrättningar.
- When: När du vill ha en teststrategi, eller ett test som fallerar innan du rättar.
- Reads: Kod och FIS-scenarier
- Command: `/andthen:testing --mode prove-it`
- Works with: exec-plan, triage
- Result: checksq · Tester · Tester på rätt nivå, skrivna test först när du eller teststrategin kräver det, plus en strategi.

### visual-validation

- Group: quality
- Role: UI mot design
- Map: 410, 499, 190, 50
- Summary: Jämför skärmbilder av UI:t med mockups, wireframes eller designspecar och kör visuella regressionskontroller.
- When: När ändringen har ett UI som måste stämma med en design.
- Reads: Skärmbilder, mockups och wireframes
- Command: `/andthen:visual-validation`
- Works with: ui-ux-design, exec-plan, review
- Result: eye · Valideringsrapport · Var det byggda UI:t skiljer sig från funktionens mockup eller wireframe, eller från designsystemet.

### simplify-code

- Group: quality
- Role: slankare kod
- Map: 620, 499, 180, 50
- Summary: Förenklar kod för tydlighet, återanvändning och slankhet, och behåller exakt samma beteende.
- When: När fungerande kod har blivit mer komplex än den behöver vara.
- Reads: Koden inom omfånget
- Command: `/andthen:simplify-code`
- Works with: review, exec-plan
- Result: simplify · Enklare kod · Mindre komplexitet, exakt samma beteende, committat när kontrollerna är gröna.

### triage

- Group: fix
- Role: ställer diagnos
- Optional: yes
- Map: 860, 499, 160, 50
- Summary: Undersöker, diagnostiserar och rättar byggfel, konfigurationsfel, buggar vid körning, regressioner och tester som fallerar.
- When: Valfritt. När orsaken är okänd eller bygget är trasigt. Beskriv symptom, inte lösningar.
- Reads: Symptom: fel, loggar, tester som fallerar
- Command: `/andthen:triage`
- Works with: implement-fix, testing, now-what
- Result: search · Diagnos · Grundorsaken, hittad innan något ändras, och rättelsen committad när testerna är gröna.
- Tag: diagnos

### implement-fix

- Group: fix
- Role: liten ändring
- Map: 1060, 499, 165, 50
- Summary: Implementerar en liten funktion eller rättelse, eller de fynd i en granskningsrapport som går att åtgärda, med minimala verifierade ändringar.
- When: När du kan beskriva ändringen i en mening.
- Reads: Det du ber om, en granskningsrapport eller ett ärende i trackern
- Command: `/andthen:implement-fix "<request>"`
- Works with: triage, review, ship
- Result: check · Verifierad rättelse · En minimal ändring, kontrollerad med det riktiga bygget och testerna och sedan committad.
- Tag: verifierad rättelse

---
title: AndThen Studio
tab: Studio
token: studio
order: 9
depends_on: []
source: https://github.com/IT-HUSET/andthen-studio (README)
---

# AndThen Studio

Eyebrow: Kompletterande app

## Se vad AndThen skriver, live

Component: ”live” i rubriken sätts i accentfärgen.

AndThen lämnar sitt arbete i filer: PRD:n, ADR:er, plan.json, FIS:en och granskningsrapporter. Studio visar filerna i din webbläsare, live från arbetskatalogen och git, så att du kan läsa, kontrollera och diskutera dem medan Core Loop pågår. Du arbetar kvar i Claude Code och tittar i Studio.

Component: under ingressen fyra fakta som små chips med etikett, sedan två länkknappar: den första fylld, den andra med bara kontur.

- Körs på: bara din dator, `http://127.0.0.1:7420`
- Läser: artefakterna från AndThen `1.0.0-rc.6` och senare
- Skärm: webbläsare på dator, ingen mobillayout
- Status: privat repo, före 1.0

Button: Installera Studio på fliken Installation → (setup)
Button: AndThen Studio på GitHub → (https://github.com/IT-HUSET/andthen-studio)

## Starta Studio – En egen terminal

Component: numrerade vita kort (01, 02, 03), vart och ett med rubrik, text och ett valfritt kommando i en mörk ruta med en kopieringsknapp, som stegen på fliken Installation. Varje kommandoruta är dold från början bakom en knapp ”Visa kommando”, som på fliken Installation.

1. **Starta Studio i projektets rotkatalog.** I Foundation Lab är det `todo-app/`, samma mapp som Claude Code körs i. Använd en egen terminal bredvid Claude Code och appen: Studio håller terminalen tills du stoppar den.
   Command: `andthen_studio`
2. **Låt Studio öppna webbläsaren.** Studio serverar projektet på `http://127.0.0.1:7420`, eller på nästa lediga port upp till 7429, och skriver ut vilken agent-CLI den kommer att använda. Startar du Studio igen för samma projekt öppnas den som redan körs, inte en till. Sidorna uppdateras av sig själva när en fil eller git ändras, så låt fliken vara öppen.
3. **Stoppa Studio med Ctrl-C** när du är klar. Det finns inget att städa upp: Studios eget tillstånd ligger i `.agent_temp/`, som `init` lägger i `.gitignore`.

Note: Startar du Studio i repots rot i stället hittar den inget Document Index och letar själv efter `plan.json`-filer. Starta den i `todo-app/`, eller ange mappen: `andthen_studio todo-app`.

## Vyerna – Det här visar Studio

Studio hittar alla artefakter genom det Project Document Index som `init` skriver in i `CLAUDE.md`. Utan Index ingen karta: kör `init` först.

Component: en tabell med tre kolumner. Vyns namn i fetstil, sedan vad vyn visar, sedan var den hjälper i Foundation Lab, som små stegchips (F1–F7) som byter till fliken Foundation Lab och väljer det steget.

| Vy | Vad den visar | I labbet |
| - | - | - |
| **Project home** | Alla artefakter som Studio har hittat, grupperade efter typ: projektdokument, ADR:er, krav, granskningsrapporter, modeller och tavlor, och dessutom git-worktrees. Sidofältet länkar till de dokument som Index nämner. | F1 |
| **Reader** | PRD:er, ADR:er, ordlistan och annan markdown, med en lista över avsnitten och avsnitt som går att länka till. | F2, F3 |
| **Plan board** | En plans stories som statuskolumner, med beroenden och hur långt uppgifterna har kommit. En story öppnar sin FIS och diffen för sina ändringar, som Studio hittar via storyns commit-trailers, dess branch eller ändringar som inte är committade. | F4, F5 |
| **Review report** | En granskningsrapport med lins, granskningsobjekt, utlåtande, fyndindex, täckningsmatris och `## Remediation Status`. | F6 |
| **Walkthroughs** | En guidad genomgång som en agent har skrivit av en pull request eller ett git-intervall, till exempel `main...feat/shared-lists`. Den har fokuspunkter för granskaren och en ”reviewed”-markering per fil. | F7 |
| **Notes** | Anteckningar som du fäster vid ett avsnitt i vilken vy som helst. Kopiera dem som markdown eller skicka dem till en agent. | F2–F4 |
| **Atlas and boards** | Arkitektur- eller ordlistemodellen, event storms och kontextkartor från `docs/models/`. Tom i Foundation Lab: de kräver `describe --model` eller `architecture`, som fördjupningslabbarna använder. | – |

## AI-åtgärder – Tre saker en agent kan göra från Studio

Med Claude Code (eller Codex) i `PATH` kan Studio starta en agentkörning, en i taget. Utan något av dem startar Studio med AI-åtgärderna avstängda och säger det.

Component: tre vita kort bredvid varandra (staplade på mobil), vart och ett med en rubrik, en rad i rost om vad åtgärden ändrar, och texten.

1. **Explain** · Ändrar ingenting. Välj ett avsnitt, så läser agenten bara det avsnittet och förklarar vad det betyder och varför det finns där. Bra för en ADR:s Reversal-rad eller ett FIS-scenario som du inte får grepp om.
2. **Send notes** · Ändrar en artefakt. Agenten får dina anteckningar om en artefakt och reviderar den med den AndThen-skill som äger den: en PRD med `clarify`, en FIS med `plan`. Om körningen misslyckas eller lämnar filen oförändrad hamnar anteckningarna i din lista med öppna anteckningar igen.
3. **Produce walkthrough** · Ändrar ingenting i projektet. Agenten läser en pull request eller ett git-intervall och skriver en genomgång under `.agent_temp/walkthrough/`. Agenten rör inte källkoden.

## Regler för Studio – Titta här, arbeta där

Component: tre vita kort med siffrorna 01–03 i rost, som reglerna i Core Loop.

1. **Det är filerna som gäller.** Studio är en vy av det som AndThen har skrivit. När vyn och en fil inte stämmer överens gäller filen: läs den i din editor eller med `git diff`.
2. **Skicka inga anteckningar medan `exec-plan` körs.** Send notes ändrar en artefakt, och att ändra en FIS mitt i en körning är detsamma som att redigera den för hand. Läs och skriv anteckningar fritt, och skicka dem efter körningen.
3. **Send notes lämnar en ändring att granska.** Det är den enda åtgärden som ändrar en projektfil. Kontrollera ändringen med `git diff` och committa den med uttrycklig sökväg, som vilken annan ändring som helst, före labbets nästa kontroll med `git status`.

## Felsökning

Component: en hopfälld detaljruta per fråga.

Summary: Startsidan visar 0 planer

`plan.json` finns under `docs/specs/` bara mellan F4 och F7. Före F4 finns ingen än, och `ship` tar bort den i F7, så då är 0 planer rätt svar. En plan som du har parkerat i `.agent_temp/` visas inte heller. Om en plan borde synas: kontrollera raden Specs & Plans i Index, eller starta Studio med `--specs-dir docs/specs`.

Summary: Modeller, tavlor och genomgångar är tomma

Det är väntat i Foundation Lab. Atlasen kräver `andthen:describe --model`, event storms och kontextkartor kräver `andthen:architecture`, och en genomgång dyker upp först när du har skapat en.

Summary: AI-åtgärderna är avstängda

Studio kräver Claude Code `2.1.273` eller senare, eller Codex `0.154.0` eller senare, i `PATH`. Utskriften vid start visar vilken av dem Studio hittade. Peka på en annan körbar fil med `--agent claude --agent-bin <path>`.

Summary: Är min version aktuell?

`andthen_studio --version` skriver ut den installerade releasen. Studio letar aldrig själv efter uppdateringar: jämför med releasesidan och kör installationskommandot igen för att uppdatera.

## Vart du går härnäst

Component: en rad knappar som byter flik. Den första är fylld, de andra har bara kontur.

- Gör Foundation Lab → (lab)
- Gå igenom Core Loop → (loop)

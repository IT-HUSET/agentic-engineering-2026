---
title: Claudes minne
tab: Claudes minne
token: memory
order: 10
depends_on: []
---

# Claudes minne

Eyebrow: Minnet i Claude Code

## Vad Claude läser in och vad Claude kommer ihåg

Claude Code läser instruktionsfiler från flera platser när en session startar och sparar egna anteckningar mellan sessionerna. Nedan ser du var varje fil finns och när den läses in, och sedan hur du öppnar och hanterar filerna med `/memory`. Filerna som andthen:init skriver har märket ”init”.

## Var minnet finns – Globalt eller projekt: var Claudes minne finns

Claude Code läser instruktioner från flera ställen. En del följer med dig in i varje projekt, en del följer med repot och en del stannar hos dig. Klicka på en ruta för att se sökvägen och när den läses in.

Interactive component: ett diagram på 680 × 512 bredvid ett detaljkort som stannar kvar när du scrollar. Ett band ORGANISATION (cream) överst, sedan tre kolumner: GLOBALT · DU, ALLA PROJEKT (teal), PROJEKT · DELAS I GIT (green), PROJEKT · BARA DU (lavender). Under dem INLÄSNINGSORDNING VID SESSIONSSTART: Central policy → Globala filer → Projekt, rot → här, + MEMORY.md, med bildtexten ”Ingen fil skriver över en annan: alla läggs ihop i kontexten, och den som ligger närmast din mapp läses sist.” Kortet tar kolumnens tint. Börjar på b1.

Hint below 960 px: Scrolla i sidled för att se hela diagrammet.

Legend: Läses in vid sessionsstart (heldragen) · Läses in vid behov (streckad) · Skrivs av andthen:init (bricka ”init” i rust)

Source: Bygger på [How Claude remembers your project](https://code.claude.com/docs/en/memory) i dokumentationen för Claude Code, oktober 2026.

| Id | Label | Subtitle | Box (x, y, w, h) | Border | Badge |
| - | - | - | - | - | - |
| org | CLAUDE.md med central policy | Sätts av IT · vid sessionsstart | 32, 62, 616, 48 | solid |  |
| a1 | ~/.claude/CLAUDE.md | Vid sessionsstart | 32, 162, 176, 48 | solid |  |
| a2 | ~/.claude/rules/ | Vid sessionsstart | 32, 220, 176, 48 | solid |  |
| b1 | ./CLAUDE.md | Vid sessionsstart | 252, 162, 176, 48 | solid | init |
| b2 | .claude/rules/ | Vid sessionsstart | 252, 220, 176, 48 | solid |  |
| b3 | Sökvägsbundna regler | När filer matchar | 252, 278, 176, 48 | dashed |  |
| b4 | sub/CLAUDE.md | När Claude arbetar där | 252, 336, 176, 48 | dashed | init |
| c1 | CLAUDE.local.md | Vid sessionsstart | 472, 162, 176, 48 | solid |  |
| c2 | MEMORY.md | Claude skriver · 200 rader | 472, 220, 176, 48 | solid |  |
| c3 | Minnesfiler per ämne | Claude läser vid behov | 472, 278, 176, 48 | dashed |  |

### Detaljer

Format: id · Title · Kind · Tint · Path · Text.

- **org** · CLAUDE.md med central policy · Organisation · vid sessionsstart · cream · `macOS: /Library/Application Support/ClaudeCode/CLAUDE.md · Linux och WSL: /etc/claude-code/CLAUDE.md · Windows: C:\Program Files\ClaudeCode\CLAUDE.md` · Instruktioner för hela organisationen som IT eller DevOps hanterar, för alla användare på datorn. Den läses in först, före dina egna filer.
- **a1** · ~/.claude/CLAUDE.md · Globalt · vid sessionsstart · teal · `~/.claude/CLAUDE.md` · Dina personliga preferenser för alla projekt på den här datorn. Den läses in efter den centrala policyn och före alla projektfiler. Du skriver den själv.
- **a2** · ~/.claude/rules/ · Globalt · vid sessionsstart · teal · `~/.claude/rules/*.md` · Personliga regelfiler för alla projekt, ett ämne per fil. De läses in före projektets regler. Ingen av uppsättningarna går före den andra, så håll dem samstämmiga.
- **b1** · ./CLAUDE.md · Projekt · delas i git · vid sessionsstart · green · `./CLAUDE.md eller ./.claude/CLAUDE.md` · Teamets instruktioner, incheckade i git: byggkommandon, konventioner, arkitektur. Claude läser också in CLAUDE.md i varje mapp ovanför den du startar i. andthen:init skriver den här filen. Finns det ingen CLAUDE.md alls läser Claude AGENTS.md i stället.
- **b2** · .claude/rules/ · Projekt · delas i git · vid sessionsstart · green · `.claude/rules/*.md` · Regelfiler per ämne, som hittas rekursivt. Utan ett paths-fält läses de in vid start, med samma prioritet som .claude/CLAUDE.md.
- **b3** · Sökvägsbundna regler · Projekt · delas i git · vid behov · green · `.claude/rules/*.md med paths: i frontmattern` · Regler med ett filmönster, till exempel src/api/**/*.ts. De läses in bara när Claude arbetar med matchande filer, vilket håller kontexten liten.
- **b4** · sub/CLAUDE.md · Projekt · delas i git · vid behov · green · `<subfolder>/CLAUDE.md` · Instruktionsfiler i mappar under den där du startade. Var och en läses in så fort Claude läser, skriver eller redigerar en fil i den mappen. andthen:init kan skriva dem för ett monorepo.
- **c1** · CLAUDE.local.md · Projekt · bara du · vid sessionsstart · lav · `./CLAUDE.local.md, listad i .gitignore` · Dina privata anteckningar för det här projektet, till exempel sandbox-URL:er eller testdata. Den läses in direkt efter CLAUDE.md i samma mapp och läses därför sist på den nivån. Den finns bara i det worktree där du skapade den.
- **c2** · MEMORY.md · Automatiskt minne · Claude skriver · vid sessionsstart · lav · `~/.claude/projects/<project>/memory/MEMORY.md` · Indexet för det automatiska minnet, som Claude sköter själv, en rad per minne. De första 200 raderna eller 25KB läses in i varje session. Alla worktrees i repot delar det, men det stannar på den här datorn.
- **c3** · Minnesfiler per ämne · Automatiskt minne · Claude skriver · vid behov · lav · `~/.claude/projects/<project>/memory/*.md` · En fil per minne, av typen user, feedback, project eller reference. De läses inte in vid start, utan Claude läser dem när de behövs. Bläddra bland dem, redigera eller ta bort dem med /memory.

## Hantera ditt minne – Öppna och hantera det med /memory

Skriv `/memory` i en Claude Code-session för att se alla minnesfiler för det här projektet och för dig, öppna en av dem i din editor och slå på eller av det automatiska minnet. Välj vad du vill göra.

Interactive component: en lista med målknappar som var och en visar kommandot till höger (”säg det bara” när kommandot är en mening), bredvid ett kort i rust med eyebrow ”Kommando”, målet som rubrik, kommandot med en kopieringsknapp, texten och en dämpad anteckning. Börjar på det första målet. Varje kommandoruta är dold från början bakom knappen ”Visa kommando”, som på fliken Installation.

| Goal | Command | Text | Note |
| - | - | - | - |
| Se och redigera mina minnesfiler | `/memory` | Kommandot listar din CLAUDE.md, CLAUDE.local.md och andra minnesfiler för dig och för det här projektet. Välj en för att öppna den i din editor. En CLAUDE.md för användaren eller projektet som inte finns än listas också, och den skapas när du väljer den. | En grafisk editor som VS Code öppnas i ett eget fönster, och du kan fortsätta arbeta. En terminaleditor som Vim tar över terminalen tills du avslutar den. |
| Se vad Claude har sparat om mig | `/memory` | Välj alternativet som öppnar mappen för det automatiska minnet. MEMORY.md är indexet, och varje minne är en egen markdownfil som du kan redigera eller ta bort. | Mappen är ~/.claude/projects/<project>/memory/. När Claude skriver ”Saved 2 memories” eller ”Recalled 2 memories” skriver eller läser den där. |
| Slå på eller av automatiskt minne | `/memory` | Använd reglaget för automatiskt minne. Det sparar autoMemoryEnabled i dina användarinställningar, ~/.claude/settings.json, så det gäller alla dina projekt. | Vill du stänga av det för bara ett projekt sätter du "autoMemoryEnabled": false i det projektets inställningar. |
| Se vilka filer som lästes in | `/context` | Kommandot visar vad som finns i kontexten just nu. Titta under Memory files för att se vilka CLAUDE.md- och regelfiler som lästes in när sessionen startade. | Filer i undermappar och sökvägsbundna regler läses in senare, när Claude arbetar med matchande filer. |
| Få Claude att komma ihåg något | `kom ihåg att vi använder pnpm, inte npm` | Säg det bara. När du ber Claude komma ihåg något sparas det i det automatiska minnet, som bara du har. | För en instruktion som hela teamet ska följa säger du i stället ”lägg till det här i CLAUDE.md”, eller redigerar filen via /memory. |
| Hitta inaktuella eller motstridiga instruktioner | `/doctor prompt-audit` | Claude går igenom dina instruktionsfiler och letar efter instruktioner skrivna för äldre modeller, hänvisningar till filer som inte längre finns och filer som motsäger varandra. Du får en rapport med föreslagna ändringar. | Inget ändras förrän du ber Claude att genomföra ändringarna. Kräver Claude Code v2.1.283 eller senare. |

## Nästa

Component: en rad med en fylld knapp som byter flik.

- Tillbaka till vad andthen:init skriver → (init)

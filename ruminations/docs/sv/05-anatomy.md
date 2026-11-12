---
title: AndThens anatomi
tab: Anatomi
token: anatomy
order: 5
depends_on: []
source: AndThen 1.0.0-rc.7 – plugin/README.md, skills/init/references/offers.md, skills/init/templates/, hooks/README.md, permissions/README.md (https://github.com/IT-HUSET/andthen); the plugin folders under ~/.claude/plugins/
---

# AndThens anatomi

Eyebrow: Var allt finns

## Alla delar av AndThen och var de finns

Component: ”var de finns” i rubriken sätts i accentfärgen.

AndThen finns på tre ställen: Claude Codes mapp på din dator, pluginet som Claude Code installerade och projektet du arbetar i. Den här fliken kartlägger alla tre, visar var du ställer in vad och hur AndThen väljer modell för varje sorts arbete.

Component: under ingressen en rad länkknappar som skrollar till de tre avsnitten nedan, den första fylld, de andra med kontur.

- Kartan → (#an-map)
- Var ställer jag in…? → (#an-set)
- Modeller → (#an-models)

## Kartan — Tre platser på disken

Klicka på en fil eller mapp för att se vad den är, vem som skriver den och när du själv rör den. Sökvägarna visas som i macOS och Linux. I Windows är `~` din användarmapp, till exempel `C:\Users\<you>`.

Interactive component: tre vita kort bredvid varandra (staplade på en telefon), ett per plats, vart och ett med en eyebrow, en rubrik och ett träd av klickbara noder som är indragna efter Level, med en mapp- eller filikon före varje namn (ett namn som slutar på ”/” är en mapp). Under korten finns ett detaljkort för den valda noden: hela sökvägen, vad den är, vem som skriver den och när du rör den. Kortet börjar på projektets `CLAUDE.md`. Upp- och nedpilarna flyttar genom alla noder i ordning.

### machine

- Eyebrow: Din dator
- Title: Claude Codes mapp
- Root: ~/.claude/

| Node | Level | What it is | Written by | When you touch it |
| - | - | - | - | - |
| `~/.claude/` | 0 | Claude Codes hemkatalog på din dator: dina personliga inställningar, plugins och agenter, som alla projekt delar på. | Claude Code | Sällan, och aldrig för hand i `plugins/`. |
| `settings.json` | 1 | Dina personliga inställningar: de plugins du har aktiverat, de marketplaces du har lagt till, svarsstilen (output style), hooks och behörigheter. | Claude Code och `/plugin`-kommandona. `init` lägger till `outputStyle` när du ber om det | När marketplacen du lägger till krockar med en gammal post (se Installation), eller för att sätta `"outputStyle": "andthen:concise-critical"`. |
| `agents/` | 1 | Rollagenter för alla projekt (användarnivå): `oracle`, `implementer`, `reviewer` och `worker`, som var och en låser en modell och en effortnivå. Mappen är tom tills du tackar ja till erbjudandet från `init` eller kopierar mallarna hit. | `init`, när du tackar ja till erbjudandet om rollagenter på användarnivå | För att ändra vilken modell en roll använder överallt. Se Modeller. |
| `output-styles/` | 1 | Dina egna svarsstilar. Behövs bara om din version av Claude Code inte listar `andthen:concise-critical`. | du | Sällan. |
| `plugins/` | 1 | Alla plugins och marketplaces som Claude Code känner till. | `/plugin`-kommandona | Aldrig för hand. Läs de två JSON-filerna för att se vad du kör. |
| `known_marketplaces.json` | 2 | Varje marketplace och källan den följer: för AndThen är det `IT-HUSET/andthen` på `develop` eller en release-tagg. | `/plugin marketplace add` | Läs den för att se vilken branch eller tagg du följer. |
| `installed_plugins.json` | 2 | Varje installerat plugin, dess version och mappen det laddas från. | `/plugin install` | Läs den för att se vilken AndThen-version som är installerad. |
| `marketplaces/andthen/` | 2 | En klon av hela AndThen-repot: pluginet plus README, COOKBOOK, CHANGELOG, hooks och behörigheter. | `/plugin marketplace add` och varje uppdatering | Läs COOKBOOK här, och kopiera hooks eller behörigheter därifrån. |
| `COOKBOOK.md` | 3 | Recept: vilken väg som passar i vilken situation, och artefakttabellen som fliken Vägar bygger på. | AndThens författare | När du undrar hur skills passar ihop. |
| `hooks/` | 3 | Valfria hooks för Claude Code: en stoppar destruktiva shell-kommandon, en säger till när kontexten börjar bli stor och två skickar notiser till dig. | AndThens författare | Kopiera dem du vill ha till dina inställningar. Inget installeras åt dig. |
| `permissions/` | 3 | Exempel på behörighets- och sandboxinställningar som håller shell-kommandon borta från dina hemligheter och från nätverket. | AndThens författare | Kopiera det du behöver. Inget installeras åt dig. |
| `cache/andthen/andthen/1.0.0-rc.7/` | 2 | Den installerade kopia som Claude Code faktiskt laddar, en mapp per version. Innehållet visas i mittenkortet. | `/plugin install` och varje uppdatering | Aldrig. En uppdatering ersätter den. |

### plugin

- Eyebrow: Pluginet
- Title: Vad AndThen består av
- Root: plugins/cache/andthen/andthen/<version>/

| Node | Level | What it is | Written by | When you touch it |
| - | - | - | - | - |
| `<version>/` | 0 | Pluginet som det är installerat. Du läser det men redigerar det aldrig: en uppdatering ersätter mappen. | AndThen-releasen | Läs det för att se exakt vad en skill gör. |
| `.claude-plugin/plugin.json` | 1 | Manifestet: pluginets namn och version, och mappen med svarsstilar som pluginet registrerar. | AndThen-releasen | Läs versionen. |
| `skills/` | 1 | Alla 21 skills, en mapp per skill. `/andthen:<skill>` kör mappen med det namnet. | AndThen-releasen | Aldrig för hand. |
| `<skill>/SKILL.md` | 2 | Själva skillen: en beskrivning av när den triggas, argumenttipset, reglerna, arbetsflödet och uppföljningsraden som den avslutar med. | AndThen-releasen | Läs den när en skill överraskar dig: svaret står här. |
| `<skill>/references/` | 2 | Detaljerade procedurer som skillen läser bara när den behöver dem, till exempel `trade-off.md` för `decide` eller `mode-wireframes.md` för `ui-ux-design`. | AndThen-releasen | Läs den för detaljerna bakom ett steg. |
| `<skill>/agents/openai.yaml` | 2 | Skillens visningsnamn och standardprompt i Codex. Det är ingen modellinställning. | AndThen-releasen | Aldrig. |
| `init/templates/` | 2 | Det som `init` kopierar till ditt projekt eller din dator. | AndThen-releasen | Läs den för att se vad ett erbjudande installerar. |
| `CLAUDE.template.md` | 3 | Utgångspunkten för ett projekts `CLAUDE.md`: Project Document Index, projektregler och Conventions. | AndThen-releasen | Aldrig: `init` kopierar den. |
| `agents/claude/` | 3 | De fyra rollagenterna med låst modell och effortnivå, klara att kopiera. `agents/codex/` innehåller samma sak för Codex. | AndThen-releasen | Aldrig: `init` kopierar dem, och du redigerar kopiorna. |
| `guidelines/CRITICAL-RULES-AND-GUARDRAILS.md` | 3 | Startmallen med kritiska regler som `init` erbjuder för din `CLAUDE.md`. | AndThen-releasen | Aldrig: när du har tagit in den är kopian i `CLAUDE.md` din. |
| `output-styles/concise-critical.md` | 3 | Korta, raka och kritiska svar, med svaret först. Pluginet registrerar den som `andthen:concise-critical`. | AndThen-releasen | Aldrig: du slår på den i `settings.json`. |
| `references/` | 1 | Kontrakt som flera skills delar: `plan.schema.json`, `fis-contract.md`, `review-calibration.md`, `unattended-runs.md`, `project-document-templates.md`. | AndThen-releasen | Läs den när du undrar vad en `plan.json` eller en FIS måste innehålla. |

### project

- Eyebrow: Ditt projekt
- Title: Vad AndThen lägger till i ett repo
- Root: todo-app/

| Node | Level | What it is | Written by | When you touch it |
| - | - | - | - | - |
| `todo-app/` | 0 | Projektets rot, där du startar Claude Code och där alla skills körs. | du | Börja alltid här. |
| `CLAUDE.md` | 1 | Claudes minne för det här projektet: Project Document Index, som talar om för alla skills var dokumenten finns, dina projektregler och de Conventions som `describe` lägger till. | `init`, och sedan lägger varje skill som skapar ett dokument till sin indexrad | För att flytta ett dokument, lägga till en regel eller ta in de kritiska reglerna. Fliken Init & minne visar den i detalj. |
| `.claude/agents/` | 1 | Rollagenter bara för det här projektet (projektnivå), som du delar med teamet via git. En projektagent går före en användaragent med samma namn. | `init`, när du tackar ja till erbjudandet om rollagenter på projektnivå, eller du, när du kopierar mallarna | För att låsa modeller för hela teamet. Se Modeller. |
| `docs/` | 1 | Dokumenten som indexet pekar ut. Varje dokument skapas av den första skill som skriver till det. | skills | Läs dem, och redigera dem när projektet ändras. |
| `KEY_DEVELOPMENT_COMMANDS.md` | 2 | Kommandona för utveckling, test och bygge, bland dem kontrollnivåerna `fast` och `full` som `exec-plan` kör. | `init` | När ett test- eller byggkommando ändras. |
| `PRODUCT.md` | 2 | Vision, icke-mål och uppgifterna under Proportionality (fas, skala, tekniska icke-mål) som avgör hur stort varje förslag blir. | den första av `clarify`, `decide`, `plan` och `architecture` som behöver dem | När fasen eller skalan ändras. |
| `DECISIONS.md` och `adrs/` | 2 | ADR-indexet, Still Current-raderna och själva ADR:erna. | `decide` | Läs innan du öppnar ett val på nytt. |
| `UBIQUITOUS_LANGUAGE.md` | 2 | Ett namn per begrepp, och synonymerna du ska undvika. | `domain --mode glossary`, `clarify` | När en term har satt sig. |
| `LEARNINGS.md` | 2 | Fällor som är värda att minnas: ”se upp för X”, ett fel som inte var uppenbart och som någon har råkat ut för. Varför ett val gjordes hör hemma i `DECISIONS.md`. | `ship`, `triage`, `handoff` | Läs den när du börjar på en uppgift. |
| `TECH-DEBT-BACKLOG.md` | 2 | Uppskjutna rättelser med det som blockerar dem, ordnade efter allvarlighetsgrad, så att ett fynd du skjuter upp inte glöms bort. | `review --fix` och `implement-fix` för fynd du skjuter upp, `triage` | Läs den när du arbetar i ett område som har en post i listan. En post som du kan beskriva i en mening är en `implement-fix`. |
| `specs/<feature>/` | 2 | PRD:n och, så länge branchen lever, `plan.json`, FIS-filerna och granskningsrapporterna. | `clarify`, `plan`, `exec-plan`, `review` | Läs PRD:n och låt skills sköta resten. |
| `research/`, `models/`, `wireframes/`, `design-system/` | 2 | Avvägningsanalyser, typade modeller, wireframes och designsystemet, vart och ett när dess skill körs. | `decide`, `describe --model`, `domain`, `ui-ux-design` | Committa dem. Läs dem innan du tar upp frågan igen. |
| `REVIEW-POLICY.md`, `ISSUE-TRACKER.md`, `VISUAL-VALIDATION.md`, `TESTING-STRATEGY.md` | 2 | Valfria inställningsdokument för granskningar, trackern, skärmdumpar och tester. | du (Review Policy), `tracker setup`, `visual-validation --mode setup`, `testing --mode strategy` | När du vill ändra hur den skillen beter sig. |
| `.agent_temp/` | 1 | Arbetsyta för tillfälliga filer, som aldrig committas: `reviews/`, `handoff/`, `spike/`, `visualize/` och Studios anteckningar. | skills och Studio | Läs överlämningar och rapporter, och rensa den när du vill. |
| `.gitignore` | 1 | `init` lägger till `.agent_temp/` och mönstret för granskningsrapporter. | `init` | Ta bort raden för granskningsrapporter om du vill committa rapporterna. |

## Var ställer jag in — Var ställer jag in…?

Varje inställning som AndThen följer har en enda plats, och alla skills läser den därifrån. En ändring som du gör en gång gäller alltså för alla senare körningar.

Component: en tabell med tre kolumner, Fråga, Var och Hur, i en vit ruta som går att skrolla i sidled på en smal skärm. Kod i kolumnen Var sätts i monospace.

| Fråga | Var | Hur |
| - | - | - |
| Vilken modell en sorts arbete använder | `.claude/agents/<role>.md` (projektet) eller `~/.claude/agents/<role>.md` (du) | Ändra `model` och `effort` i frontmattern och starta sedan en ny session. Finns ingen sådan fil än? Kopiera filerna från pluginets mallar, som under Modeller. |
| Vilken modell som körs utan rollagenter | din session | `/model` i Claude Code, eller modellväljaren i appen. Alla subagenter ärver den. |
| Hur kortfattat Claude svarar | `~/.claude/settings.json` | Sätt `"outputStyle": "andthen:concise-critical"` och starta en ny session. En projektinställning går före. |
| Var ett dokument finns | `CLAUDE.md`, Project Document Index | Flytta filen och ändra dess indexrad. Skills hittar dokument via postens namn, så behåll namnen. |
| Vilka kommandon som bevisar att koden fungerar | `docs/KEY_DEVELOPMENT_COMMANDS.md` | Ändra raderna `fast` och `full`. `exec-plan` kör `fast` för varje story och `full` på det färdiga trädet. |
| Regler som varje session måste följa | `CLAUDE.md` | Lägg till dem under Project-Specific Guidelines and Rules, eller ta in avsnittet Critical Rules som `init` erbjuder. |
| Vilken AndThen-version du kör | `~/.claude/plugins/known_marketplaces.json` och `installed_plugins.json` | Byt version med `/plugin marketplace add IT-HUSET/andthen@<ref>` och `/plugin install andthen@andthen`, som på fliken Installation. |
| Vad en granskning hoppar över eller lägger till | `docs/REVIEW-POLICY.md` | Skriv den utifrån startmallen i AndThens README och kör sedan `/andthen:init seed Review Policy` för att lägga till dess indexrad. |
| Ditt ärendesystem, och var kraven finns efter en merge | `docs/ISSUE-TRACKER.md` | Kör `/andthen:tracker setup`. Med `Record: repo` behålls `prd.md`, med `Record: tracker` ligger kraven kvar i ärendena. |
| Om granskningsrapporter committas | `.gitignore` | Ta bort raden för granskningsrapporter som `init` lade till. |
| Stoppa farliga shell-kommandon | `hooks` i din `settings.json` | Kopiera `block-dangerous-commands.py` från `hooks/` i AndThen-repot och registrera den som en PreToolUse-hook. |
| Köra en skill utan frågor | själva kommandot | Lägg till `--auto`: öppna beslut blir `ASSUMPTION:`-rader. `clarify` går inte att köra obevakat. |

## Modeller — Vilken modell gör vad

AndThen namnger aldrig en modell i en prompt. Varje skill lämnar över arbetet till en roll: den installerade rollagenten om det finns en, annars en subagent på din sessions modell. Arbete som kräver omdöme stannar i din session.

Component: fyra vita kort bredvid varandra (två och två på en surfplatta, staplade på en telefon), ett per roll: rollnamnet i monospace, modell och effortnivå som två små chips, och vad rollen används till.

| Role | Model | Effort | Used for |
| - | - | - | - |
| `oracle` | opus | xhigh | Omdömesarbete som du ger den, till exempel en design eller en andra bedömning, och svåra problem som en annan agent lämnar över för att de ligger över dess nivå. |
| `implementer` | sonnet | high | En medelstor eller stor, avgränsad arbetsuppgift: bygga en story, skriva FIS:en för en story i en plan eller göra research som väger källor mot varandra. |
| `reviewer` | opus | medium | Alla granskningar, oavsett vad som granskas, med fynd och ett utlåtande som resultat. |
| `worker` | haiku | high | Små, väldefinierade deluppgifter: uppslag, genomsökningar och mekaniska ändringar. |

### Installera och ändra dem

Component: numrerade vita kort (01–05), som stegen på fliken Installation, där varje kommando är dolt bakom knappen ”Visa kommando”.

1. **Se efter vad du har.** Om varken `~/.claude/agents/` eller projektets `.claude/agents/` finns körs alla skills på din sessions modell. Den byter du med `/model` i Claude Code eller med modellväljaren i appen. Från `todo-app/`:
   Command: `ls ~/.claude/agents .claude/agents`
2. **Hämta filerna: låt `init` erbjuda dem.** Kör `init` igen. I ett projekt som redan är installerat kompletterar den bara det som saknas, behåller allt du har och erbjuder rollagenterna bland sina tillval. Välj projektnivå för att dela låsningarna med teamet, eller användarnivå för att bara använda dem själv.
   Command: `/andthen:init`
3. **Eller kopiera mallarna själv.** De följer med pluginet. Kommandot kopierar alla fyra till projektet och körs från `todo-app/` i Git Bash:
   Command: `mkdir -p .claude/agents && cp ~/.claude/plugins/cache/andthen/andthen/{andthen_version}/skills/init/templates/agents/claude/*.md .claude/agents/`
4. **Ändra en låsning.** Öppna rollens fil, till exempel `.claude/agents/reviewer.md`, och ändra `model` och `effort` i frontmattern. Låt `name` vara som det är: en skill frågar efter rollen med det namnet.
5. **Starta en ny session i `todo-app/`.** Agentdefinitioner laddas när en session startar, och projektets agenter gäller bara sessioner som startas i `todo-app/`, där dess `.claude/agents/` ligger.

Note: Redigera aldrig mallarna i pluginet, eftersom en uppdatering ersätter dem. Redigera dina kopior, och kontrollera låsningarna igen när modellutbudet ändras.

## Next

Component: en rad knappar som byter flik. Den första är fylld, de andra har bara kontur.

- Se vad andthen:init skriver → (init)
- Tillbaka till Installation → (setup)
- Utforska alla skills → (skills)

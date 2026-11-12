---
title: Termer och ordval för den svenska guiden
used_by: [alla filer i docs/sv/]
---

# Termer och ordval

Den svenska guiden är samma sida som den engelska, i svenska meningar. Den här filen låser ordvalen, så att alla flikar kallar samma sak samma sak. Språkregler i övrigt: skill `it-huset-skills:ith-svenska`, registerprofil 2 (teknisk text), tilltal `du`.

## Grundregler

- **Översätt inte** det som är ett namn, ett kommando eller något läsaren skriver eller ser på skärmen i ett engelskt verktyg:
  - kommandon, sökvägar, filnamn, flaggor, kodblock, filträd och exempelinnehåll i filer (allt i `` `kod` `` och i kodblock står kvar ordagrant)
  - skillnamn (`clarify`, `plan`, `exec-plan`, `review`, `ship` …) och kommandon som `/andthen:init`, `/memory`, `/clear`
  - produktnamn: AndThen, AndThen Studio, Claude Code, IT-HUSET, GitHub
  - knapp- och menyetiketter i Claude Code, Studio och andra engelska verktyg (skriv dem som de står där)
  - taggar som AndThen skriver i sina filer: `Fix`, `Note`, `done`, `kept` och liknande
- **Översätt** all löpande text, rubriker, eyebrows, bildtexter, alt-texter, `aria-label`, knappar och etiketter på själva guidesidan.
- **Promptar** som man skriver till Claude Code (fältet `Prompt:`) översätts till svenska. Claude förstår svenska, och guiden ska gå att köra på svenska.
- Svenska citattecken ”…”, tankstreck – (aldrig —), meningsversaler i rubriker, inga utropstecken.
- Behåll all formatering: länkar, `**fet**`, `` `kod` ``, `{skill_count}`, `{andthen_version}`, tabellernas kolumner och alla rader som `Component:`, `Command:`, `Source:` och liknande. Raderna som beskriver komponenter (`Component:` och `Interactive component:`) är instruktioner, inte sidtext: översätt dem också, men ändra aldrig vad de säger.
- Frontmatter: översätt `title` och `tab`, rör aldrig `token`, `order`, `depends_on`, `source` och andra tekniska fält.
- Fältnamn i strukturerade block (`Group:`, `Role:`, `Command:`, `Situation:`, `Chain:`, `Tint:` …) står kvar på engelska, så att filen har samma struktur som den engelska. Bara fältens värden översätts, och bara när värdet är text (inte en tint, en position, ett kommando eller ett id).

## Namn som står kvar på engelska

| Term | Så skrivs den | Kommentar |
| - | - | - |
| Core Loop | Core Loop | Huvudflödets namn, även fliken |
| Foundation Lab | Foundation Lab | Labbets namn. ”labbet” i löpande text |
| AndThen Studio | AndThen Studio, Studio | |
| FIS | FIS, en FIS, FIS:en, flera FIS:ar | Feature Implementation Specification |
| PRD | PRD, en PRD, PRD:n | |
| ADR | ADR, en ADR, ADR:en, ADR:er | |
| Domain Map | Domain Map | Artefaktens namn |
| Ubiquitous Language | Ubiquitous Language | Begreppets namn; ”ordlistan” går bra för filen |
| Project Document Index | Project Document Index | Avsnittets namn i CLAUDE.md |
| Implementation Observations | Implementation Observations | Avsnittets namn i en FIS |
| Agentic Engineering 2026 | Agentic Engineering 2026 | Kursens namn |

## Lånord med svensk böjning

| Engelska | Svenska | Böjning |
| - | - | - |
| skill | skill | en skill, skillen, skills, alla skills (undvik ”skillsen”, skriv om) |
| story | story | en story, storyn, stories |
| spec | spec | en spec, specen, specar |
| pull request | pull request | en pull request, PR, PR:en |
| branch | branch | en branch, branchen, brancher |
| commit | commit | en commit, committen, commits; verb `committa` |
| worktree | worktree | ett worktree, worktreet |
| repo | repo | ett repo, repot |
| prompt | prompt | en prompt, prompten, promptar |
| plugin | plugin | ett plugin, pluginet, plugins |
| hook | hook | en hook, hooken, hooks |
| subagent | subagent | en subagent, subagenten, subagenter |
| agent | agent | en agent, agenten, agenter |
| session | session | en session, sessionen |
| diff | diff | en diff, diffen |
| token (i URL) | token | |
| frontmatter | frontmatter | |
| spike | spike | en spike, spiken |
| wireframe | wireframe | en wireframe, wireframes |
| design system | designsystem | ett designsystem |
| checklist | checklista | |
| backlog | backlog | |
| glossary | ordlista | |

## Svenska ord för guidens begrepp

| Engelska | Svenska |
| - | - |
| requirements | krav |
| acceptance criteria | acceptanskriterier |
| acceptance scenario | acceptansscenario |
| proof | bevis |
| verify, verification | verifiera, verifiering |
| review (verksamheten) | granskning, granska (skillen heter fortfarande `review`) |
| reviewer | granskare |
| finding | fynd |
| fix (substantiv, en liten rättelse) | rättelse, fix går bra i sammansättningar som ”fixvägen” |
| path (vägval i guiden) | väg |
| step | steg |
| tab | flik |
| memory (Claudes minne) | minne |
| set up / setup | installera, installation; ”din miljö” för ”your setup” |
| feature | funktion |
| codebase | kodbas |
| working tree | arbetskatalog |
| artifact (fil som ett steg lämnar) | artefakt |
| learnings | lärdomar |
| handoff | överlämning |
| decision | beslut |
| trade-off | avvägning |
| right-size | anpassa, ”lagom mycket struktur” |
| judgment | omdöme |
| ship (verbet) | leverera; skillen heter `ship` |
| merge | slå ihop, merga |
| scope | omfång |
| edge case | kantfall |
| fresh session | ny session |
| role agents | rollagenter |
| worked example | genomarbetat exempel |
| structure check | strukturkontroll |

## Etiketter på sidan

Samma engelska etikett blir alltid samma svenska.

| Engelska | Svenska |
| - | - |
| Copy | Kopiera |
| Copied | Kopierat |
| Selected | Vald |
| Show command | Visa kommando |
| Hide command | Dölj kommando |
| Close | Stäng |
| Previous / Next | Föregående / Nästa |
| Next step | Nästa steg |
| Reset | Återställ |
| Where to go next | Vart du går härnäst |
| Steps | Steg |
| Result | Resultat |
| Reads | Läser |
| Writes | Skriver |
| Command | Kommando |
| Works with | Samarbetar med |
| Written by | Skrivs av |
| You get | Du får |
| What to notice | Lägg märke till |
| Worked example | Genomarbetat exempel |
| Optional | Valfritt |
| Note | Obs |
| Session start | Vid sessionsstart |
| After ship | Efter ship |
| Your setup | Din miljö |
| Your machine | Din dator |
| Your project | Ditt projekt |

## Flikar

Länktoken (`#init`, `#lab` …) är densamma på båda språken, så att växlaren kan behålla fliken.

| Token | Engelska | Svenska |
| - | - | - |
| start | Start | Start |
| setup | Setup | Installation |
| init | Init | Init |
| skills | Skills | Skills |
| anatomy | Anatomy | Anatomi |
| loop | Core Loop | Core Loop |
| paths | Paths | Vägar |
| lab | Foundation Lab | Foundation Lab |
| studio | Studio | Studio |
| memory | Claude’s memory | Claudes minne |

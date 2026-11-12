---
title: Skills i AndThen
tab: Skills
token: skills
order: 4
depends_on: [shared/skills.md, shared/icons.md]
---

# Skills i AndThen

Eyebrow: Skills i AndThen · {andthen_version}

## Översikt över AndThens {skill_count} skills

Varje ruta är en skill, grupperad efter vad den gör. Klicka på en för att se vad den läser, vad den skriver och vilka skills den samarbetar med.

Component: förklaring med fem poster: Skill (heldragen ruta) · Valfritt steg (streckad ruta) · Artefakt som skillen skriver (dokumentchip) · Överlämning (pil) · Du (fylld prick).

## Skill-kartan

Interactive component: containerkarta i C4-stil, 1280 × 605, i ett kort som skrollar. En person, ”Du [utvecklare]”, står utanför AndThens streckade gräns (med etiketten ”ANDTHEN · PLUGIN TILL CLAUDE CODE · {skill_count} SKILLS”). Varje grupp är ett tonat band med etiketten i versaler. Varje skill står på sin plats enligt Map i shared/skills.md. Valfria skills har streckad ram, och skills i Core Loop har sitt Document-chip under sig på en prickad linje. Klickar du på en skill väljs den, de skills som står i dess Works with-lista framhävs och resten tonas ned. Pilar som rör den förblir tända. Tangentbord: Tab och Enter.

Hint below 960 px: Skrolla i sidled för att se hela kartan.

### Band

| Group | x | y | Width | Height | Label |
| - | - | - | - | - | - |
| start | 195 | 40 | 505 | 100 | START & SESSION |
| share | 720 | 40 | 525 | 100 | DELNING & UPPFÖLJNING |
| design | 195 | 160 | 1050 | 100 | DESIGN & UTFORSKNING · VALFRITT, GER UNDERLAG TILL PLAN |
| core | 195 | 290 | 1050 | 150 | CORE LOOP · VARJE STEG SKRIVER DET SOM NÄSTA STEG LÄSER |
| quality | 195 | 465 | 625 | 100 | KVALITET · ANVÄNDS AV EXEC-PLAN OCH REVIEW |
| fix | 840 | 465 | 405 | 100 | FIXVÄGEN · EN RÄTTELSE PÅ EN MENING |

### Pilar

From och To är skill-id:n, `you` för personen eller `group:<id>` för ett helt band. Path är SVG-sökvägsdata på kartan.

| From | To | Path | Label |
| - | - | - | - |
| you | now-what | `M142 99 H211` | frågar (vid 177, 91) |
| clarify | decide | `M357 350 H385` |  |
| decide | plan | `M531 350 H559` |  |
| plan | exec-plan | `M705 350 H733` |  |
| exec-plan | review | `M879 350 H907` |  |
| review | ship | `M1053 350 H1081` |  |
| group:design | plan | `M633 262 V314` | underlag (vid 662, 285) |
| triage | implement-fix | `M1022 524 H1056` |  |
| implement-fix | ship | `M1227 524 H1255 V350 H1229` |  |

## Vald skill

Component: detaljkort under kartan, tonat i skillens gruppfärg. Kortet visar gruppen (och ”valfri”), skillens namn i mono, dess Role, Summary och When, sedan en resultatruta med ikon, titel och text, Reads, Command med en kopieringsknapp och ”Samarbetar med” som knappar som väljer den skillen. Kortet visar plan från början. Varje kommandoruta är dold från början bakom knappen ”Visa kommando”, som på fliken Installation.

## Alla {skill_count} skills och vad de ger

Eyebrow: Översikt

Component: tabell med en rad per skill i kartans ordning: Skill (en knapp som väljer skillen på kartan och skrollar upp, med ”valfri” under namnet när det gäller) · Grupp (en prick i gruppens färg och etiketten) · Resultat (ikon och titel) · Vad du får (texten i Result). Raden för den valda skillen är tonad.

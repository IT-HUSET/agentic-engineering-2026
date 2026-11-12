---
title: AndThen-guiden
version: 1.54
date: 2026-11-12
status: published
html: html/andthen-guide.sv.html
artifact: https://claude.ai/artifact/HAVpWj74fHd8ZMU5xyUJyT
description: Kursguide till AndThen: installation, hur andthen:init går till steg för steg, en klickbar karta över alla 21 skills, Core Loop från idé till pull request, de andra vägarna och vad varje steg lämnar efter sig, Foundation Lab steg för steg, var AndThen Studio hjälper till var alla delar av AndThen finns och, på en sidoflik, var Claudes minne finns och hur du hanterar det.
icon: workflow
tabs: [01-start, 02-setup, 03-init, 04-skills, 05-anatomy, 06-core-loop, 07-paths, 08-foundation-lab, 09-studio, 10-memory]
depends_on: [shared/skills.md, shared/icons.md, TERMS.md]
---

# AndThen-guiden

Ramen runt de tio flikarna på den svenska sidan. Samma ram som den engelska (`../00-guide.md`), med svensk text. En HTML-sida, en flik per markdownfil, i ordningen i `tabs` ovan. Den sista fliken, Claudes minne, är ett sidospår om Claude Code snarare än AndThen och ligger därför efter AndThen-flikarna. `08-foundation-lab` består av två delar, `08-foundation-lab.part1.md` och `08-foundation-lab.part2.md`, som läses som en fil. Ordvalen står i `TERMS.md`.

## Header

- Logo: IT-HUSETs ordmärke, svart på ljust, vitt på mörkt.
- Metatext, högerställd: Agentic Engineering 2026 · AndThen
- Språkväxlare till höger om metatexten: EN och SV som en tvådelad pill, där det aktuella språket är ifyllt. EN öppnar `html/andthen-guide.html`, SV öppnar `html/andthen-guide.sv.html`. Växlaren behåller den öppna fliken, och webbläsaren kommer ihåg valet till nästa besök.

## Tabs

Component: en flikrad under sidhuvudet. Före flikarna, en gång för alla, en liten etikett ”AndThen” i rubriktypsnittet och accentfärgen, avskild med en tunn skiljelinje; fliketiketterna utelämnar ordet. Varje fliks etikett är fältet `tab` i dess fil och länktoken är fältet `token`, samma token som på den engelska sidan. Vänster- och högerpil flyttar mellan flikarna. Den aktiva fliken har en rostfärgad understrykning. Den sista fliken, Claudes minne, är ett sidospår om Claude Code, så en tunn lodrät linje i samma färg som skiljelinjen efter etiketten skiljer den från AndThen-flikarna. På smal skärm scrollar flikraden i sidled i sin egen rad.

## Footer

Component: skogsgrönt band med den vita logotypen.

Byggd på [AndThen](https://github.com/IT-HUSET/andthen) · specdriven agentisk utveckling

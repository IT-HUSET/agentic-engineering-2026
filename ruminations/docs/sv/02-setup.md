---
title: Installation
tab: Installation
token: setup
order: 2
depends_on: []
---

# Installation

Eyebrow: Installation

## Installera AndThen som plugin i Claude Code

Component: ”AndThen” i rubriken sätts i accentfärgen.

Berätta om din miljö, så visar stegen nedan exakt de kommandon du behöver. Kopiera in dem i Claude Code i tur och ordning.

## Din miljö

Interactive component: en dämpad ruta med rubriken ”Din miljö” och två kontroller. Stegen nedan byggs om så fort någon av dem ändras.

- Checkbox: Jag har en äldre AndThen (0.x) installerad
- Text field: Releasetagg från din kursledare, visas som `v1.0.0-rc.` följt av ett kort fält för N (bara siffror, platshållaren N). Tomt fält betyder kursens branch `develop`.

## Steg

Component: numrerade vita kort (01, 02 …), vart och ett med rubrik, text och kommandot i en mörk ruta med en kopieringsknapp. Kommandorutan är dold från början: en liten knapp med kontur, terminalikon och texten ”Visa kommando” visar den, och sedan står det ”Dölj kommando” på knappen. En ruta som har visats förblir öppen när stegen byggs om. Ett villkorat steg har streckad kant och etiketten ”bara om du har 0.x”. Numreringen följer de steg som faktiskt visas.

1. **Ta bort den gamla versionen** – bara när rutan för 0.x är ikryssad. AndThen 0.x och 1.0 har samma marketplace-namn, andthen, så den gamla marketplacen måste bort först.
   Command: `/plugin marketplace remove andthen`
2. **Lägg till AndThens marketplace.**
   - With no tag: Kommandot talar om för Claude Code var AndThen finns. @develop följer kursens branch. Får du en releasetagg av din kursledare skriver du in den ovan.
     Command: `/plugin marketplace add IT-HUSET/andthen@develop`
   - With tag N: Kommandot talar om för Claude Code var AndThen finns, låst till den release som din kursledare gav dig.
     Command: `/plugin marketplace add IT-HUSET/andthen@v1.0.0-rc.N`
3. **Installera pluginet.** Kommandot installerar pluginet från den marketplace du just lade till. Namnet läses plugin@marketplace:
   Component: annoterat namn, `andthen` märkt ”plugin”, `@`, `andthen` märkt ”marketplace”.
   Command: `/plugin install andthen@andthen`
4. **Fråga var du ska börja.** Kör now-what när du är osäker på var du ska börja. Den undersöker projektet och skickar dig vidare till rätt skill.
   Command: `/andthen:now-what`

## Var du skriver kommandona

Det här är slash-kommandon. Skriv dem ett i taget vid prompten i Claude Code, i en terminalsession som du har startat med `claude`.

## Felsökning

Component: en hopfälld detaljruta.

Summary: Det går inte att lägga till marketplacen: ”its source doesn’t match its extraKnownMarketplaces entry”

Dina användarinställningar har redan en marketplace som heter `andthen`, men den pekar på en annan källa. Öppna `~/.claude/settings.json` och se till att posten stämmer med raden du lägger till. För kursens branch lägger du till `"ref": "develop"`:

```json
"extraKnownMarketplaces": {
  "andthen": {
    "source": { "source": "github", "repo": "IT-HUSET/andthen", "ref": "develop" }
  }
}
```

Kör sedan stegen igen från början.

## AndThen Studio

Eyebrow: Installera också

Component: lavendelfärgat kort med en rand överst.

Studio är ett visuellt komplement till AndThen. Den visar filerna som AndThen skriver som tavlor du kan bläddra i, så att specar, planer och beslut blir lättare att granska tillsammans. Studio är en enda binärfil som bara körs på din dator.

Note (med låsikon): Repot är privat. Be din kursledare om åtkomst om länken ger 404.

Installera Studio med GitHub CLI. Du behöver vara inloggad (`gh auth login`) och ha åtkomst till repot. Kör kommandot i en terminal, inte i Claude Code. Välj ditt system:

Interactive component: två små växlingsknappar, ”macOS / Linux” och ”Windows (PowerShell)”, som väljer vilket kommando som visas. Standard: Windows när webbläsaren rapporterar Windows, annars macOS / Linux. Kommandorutan är dold från början bakom samma knapp ”Visa kommando” som i stegen ovan.

- macOS / Linux: Skriptet installerar i `~/.local/bin`. Om mappen inte finns i din `PATH` skriver skriptet ut raden som du ska lägga till i din skalprofil.
  Command: `gh release download -R IT-HUSET/andthen-studio -p install.sh -O - | sh`
- Windows (PowerShell): Skriptet installerar i `%LOCALAPPDATA%\Programs\andthen-studio` och lägger till mappen i `PATH` för din användare. Öppna en ny terminal efteråt.
  Command: `gh release download -R IT-HUSET/andthen-studio -p install.ps1 -O - | Out-String | Invoke-Expression`

Kontrollera: `andthen_studio --version` skriver ut den installerade releasen.

Button: Så använder du Studio i kursen → (studio)
Button: [Öppna AndThen Studio på GitHub →](https://github.com/IT-HUSET/andthen-studio)

## Vart du går härnäst

Component: en rad knappar som byter flik, i flikordning. Den första är fylld, de andra har bara kontur.

- Se vad andthen:init gör → (init)
- Utforska alla skills → (skills)
- Se var AndThen finns → (anatomy)
- Gå igenom Core Loop → (loop)
- Se de andra vägarna → (paths)
- Gör Foundation Lab → (lab)
- Använd AndThen Studio → (studio)

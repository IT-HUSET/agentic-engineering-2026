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

Berätta om din miljö, så visar stegen nedan exakt de kommandon du behöver. Kör dem i tur och ordning.

## Din miljö

Interactive component: en dämpad ruta med rubriken ”Din miljö” och två kryssrutor. Den andra går bara att kryssa i när den första är ikryssad. Stegen nedan byggs om så fort någon av dem ändras.

- Checkbox: AndThen är redan installerat
- Checkbox: Jag lade till det från en tagg eller `@develop`

## Steg

Component: numrerade vita kort (01, 02 …), vart och ett med rubrik, text och kommandot i en mörk ruta med en kopieringsknapp. Kommandorutan är dold från början: en liten knapp med kontur, terminalikon och texten ”Visa kommando” visar den, och sedan står det ”Dölj kommando” på knappen. En ruta som har visats förblir öppen när stegen byggs om. Ett villkorat steg har streckad kant och sitt villkor som etikett. Numreringen följer de steg som faktiskt visas.

1. **Skapa ditt eget repo.** Öppna kursens repo på GitHub och välj Use this template och sedan Create a new repository. Välj ditt konto och kryssa i Include all branches. Klona repot och arbeta där: dina ändringar sparas, och din pull request öppnas i ditt eget repo.
   Command: `gh repo clone <your-account>/<your-repo>`
2. **Ta bort den gamla marketplacen** – bara om AndThen redan är installerat och lades till från en tagg eller `@develop`. En marketplace ligger kvar på den ref den lades till med, så en tagg eller @develop måste bort innan du lägger till den senaste releasen.
   Command: `/plugin marketplace remove andthen`
3. **Uppdatera marketplacen** – bara om AndThen redan är installerat, inte från en tagg. Hämtar den senaste releasen av AndThen.
   Command: `/plugin marketplace update andthen`
4. **Uppdatera pluginet** – bara om AndThen redan är installerat, inte från en tagg. Uppdaterar AndThen från marketplacen. Starta om Claude Code efteråt.
   Command: `/plugin update andthen@andthen`
5. **Lägg till AndThens marketplace** – om du inte just har uppdaterat. Kommandot talar om för Claude Code var AndThen finns. Det följer den senaste releasen. Kursen bygger på AndThen 1.0.0 och är avstämd mot 1.1.0, så en senare release kan skilja sig i detaljer.
   Command: `/plugin marketplace add IT-HUSET/andthen`
6. **Installera pluginet** – om du inte just har uppdaterat. Kommandot installerar pluginet från den marketplace du just lade till. Namnet läses plugin@marketplace:
   Component: annoterat namn, `andthen` märkt ”plugin”, `@`, `andthen` märkt ”marketplace”.
   Command: `/plugin install andthen@andthen`
7. **Kontrollera din miljö.** I en terminal, från repots rot. Den kontrollerar git, gh, Claude Code med AndThen och testerna i todo-app, och slutar med GREEN eller RED. Åtgärda varje FAIL före dag 1.
   Command: `uv run check.py`
8. **Fråga var du ska börja.** Kör now-what när du är osäker på var du ska börja. Den undersöker projektet och skickar dig vidare till rätt skill.
   Command: `/andthen:now-what`

## Var du skriver kommandona

Kommandon som börjar med `/` är slash-kommandon: skriv dem ett i taget vid prompten i Claude Code, i en terminalsession som du har startat med `claude`. De andra, som `uv run check.py`, kör du i en vanlig terminal från repots rot.

## Felsökning

Component: en hopfälld detaljruta.

Summary: Det går inte att lägga till marketplacen: ”its source doesn’t match its extraKnownMarketplaces entry”

Dina användarinställningar har redan en marketplace som heter `andthen`, men den pekar på en annan källa. Öppna `~/.claude/settings.json` och se till att posten stämmer med raden du lägger till. För den senaste releasen utelämnar du `ref`:

```json
"extraKnownMarketplaces": {
  "andthen": {
    "source": { "source": "github", "repo": "IT-HUSET/andthen" }
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

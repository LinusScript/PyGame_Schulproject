<file name=0 path=README.md>> Tipp: Wenn ihr noch keine Assets nutzt, lasst `assets/` einfach weg.

---

## 🕹️ Steuerung

- **Bewegen:** Pfeiltasten oder **WASD**
- **Pause:** `P` (optional)
- **Restart:** `R` (optional)
- **Quit:** `ESC`

---

## 🤝 Zusammenarbeit (Team / Repo Zugriff)

### 1) Zugriff für Teammitglieder (Push/Pull)
Damit dein Kollege **pushen & pullen** kann, musst du ihn auf GitHub als **Collaborator** hinzufügen:

1. Repo öffnen: `LinusScript/PyGame_Schulproject`
2. **Settings** → **Collaborators** (oder **Manage access**)
3. **Add people** → GitHub-Username/E-Mail eingeben
4. Rolle: **Write** (reicht für Push/Pull)
5. Kollege nimmt die Einladung an (Glocke/Email)

> Hinweis: **Public** = jeder kann *clonen/pullen*, aber **pushen nur Collaborators**.

### 2) Code im Browser öffnen (github.dev)
- Repo auf GitHub öffnen und **`.`** (Punkt) drücken
  - oder URL so öffnen: `https://github.dev/LinusScript/PyGame_Schulproject`

### 3) Lokal arbeiten (Clone)
```bash
git clone https://github.com/LinusScript/PyGame_Schulproject.git
cd PyGame_Schulproject
```

### 4) Team-Workflow (empfohlen)
**Immer zuerst updaten:**
```bash
git checkout main
git pull
```

**Neues Feature in Branch bearbeiten:**
```bash
git checkout -b feature/mein-feature
# Änderungen machen
git add .
git commit -m "Add feature"
git push -u origin feature/mein-feature
```

Danach auf GitHub einen **Pull Request** erstellen und in `main` mergen.

### 5) Häufigster Fehler: README geändert, aber nicht gepusht
Wenn `README.md` geändert wurde, musst du **stagen → committen → pushen**:
```bash
git add README.md
git commit -m "Update README"
git push
```

## 🚀 Installation & Start

### 1) Repository klonen
```bash
git clone https://github.com/LinusScript/PyGame_Schulproject.git
cd PyGame_Schulproject</file>
> Tipp: Wenn ihr noch keine Assets nutzt, lasst `assets/` einfach weg.

---

## 🕹️ Steuerung

- **Bewegen:** Pfeiltasten oder **WASD**
- **Pause:** `P` (optional)
- **Restart:** `R` (optional)
- **Quit:** `ESC`

---

## 🤝 Zusammenarbeit (Kollegen: Zugriff + Pull/Push)

### 1) Zugriff geben (du als Repo-Owner)
Damit dein Kollege **pullen & pushen** kann, musst du ihn auf GitHub hinzufügen:

1. GitHub Repo öffnen: `LinusScript/PyGame_Schulproject`
2. **Settings** → **Collaborators** (oder **Manage access**)
3. **Add people** → GitHub-Username oder E-Mail eingeben
4. Berechtigung: **Write**
5. Kollege nimmt die Einladung an (Glocke/Email)

> Public Repo: Jeder kann **clonen/pullen**, aber **pushen nur Collaborators**.

### 2) Was der Kollege im Terminal macht (1:1)

#### Repo holen (einmalig)
```bash
git clone https://github.com/LinusScript/PyGame_Schulproject.git
cd PyGame_Schulproject
```

#### Vor jeder Arbeit (Updates holen)
```bash
git checkout main
git pull
```

#### Änderungen hochladen (Push)
```bash
git add .
git commit -m "Kurze Beschreibung"
git push
```

### 3) Empfehlung: Branch statt direkt auf main
So überschreibt ihr euch nicht gegenseitig:
```bash
git checkout -b feature/mein-feature
# Änderungen machen
git add .
git commit -m "Add feature"
git push -u origin feature/mein-feature
```
Dann auf GitHub einen **Pull Request** erstellen und nach `main` mergen.

### 4) Wichtigste Git-Kommandos (Cheat Sheet)
- Status prüfen: `git status`
- Änderungen sehen: `git diff`
- Remote prüfen: `git remote -v`
- Update holen: `git pull`
- Hochladen: `git push`

## 🚀 Installation & Start

### 1) Repository klonen
```bash
git clone https://github.com/LinusScript/PyGame_Schulproject.git
cd PyGame_Schulproject</code></pre>
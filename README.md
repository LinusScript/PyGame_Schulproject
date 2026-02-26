> Tipp: Wenn ihr noch keine Assets nutzt, lasst `assets/` einfach weg.

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
#### Änderungen hochladen (Push)
```bash
git add .
git commit -m "Kurze Beschreibung"
git push


Test 
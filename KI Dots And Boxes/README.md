# Künstliche Intelligenz Praktikum





# Ablauf 

Willkommen zum KI-/Abtestat-Projekt!  
Jedes Team arbeitet in einem eigenen GitLab-Repository.  
 - Dieses Dokument erklärt, wie ihr Aufgaben bearbeitet, Merge Requests erstellt und Updates vom zentralen Repository übernehmt.
 - Halten Sie sich an die vorgegebenen Strukturen und Konventionen.
---

## Grundprinzip

- **`main (remote)` ist geschützt:**  
  Sie könnten dort nicht direkt pushen – nur Merge Requests.
- **Ihr arbeitet in eigenen Branches:**  
  z. B. `aufgabe_1`, `aufgabe_2_3`, `aufgabe_4`, …
- **Neue Aufgaben oder Bugfixes** kommen aus dem *Parent-Repository* („upstream“).

---

## Einrichtung

Nach dem ersten Klonen Ihres Team-Repos:
```bash
git clone https://git.fh-muenster.de/labki-lehre-studierende/sose26/<team-repo>.git
cd <team-repo>
```
<!-- TODO: Links Anpassen!(muss sein damit die Studis pullen können)-->

Fügen Sie einmalig das zentrale Repository als Upstream hinzu:
```bash
git remote add upstream https://git.fh-muenster.de/labki-lehre-studierende/sose26/ki-praktikum
git fetch upstream
```

---

## Workflow pro Aufgabe oder Aufgaben 
<!-- (TODO: Branch pro Aufgabe oder pro Arbeitsblatt?)-->

###  Neuen Branch anlegen
```bash
git checkout -b aufgabe_x
```

###  Änderungen umsetzen
Bearbeitet die entsprechenden Dateien, fügt neue Skripte oder Ergebnisse hinzu.

### Commit erstellen 
```bash
git add .
git commit -m "Lösung Aufgabe X"
git push origin aufgabe_x
```

### Merge Request erstellen
> Achtung:
> Der Merge Request muss im Remote Repository erfolgen.

Erstellen Sie in GitLab einen **Merge Request** von `aufgabe_x` → `main`.
Dieser Merge Request ist die Vorraussetzung für ein Abtestat.

---

## Updates vom Parent Repository synchronisieren

Wenn im zentralen Repository ("upstream") etwas geändert oder ergänzt wurde (z. B. neue Aufgaben, Bugfixes), können Sie diese Änderungen übernehmen:

```bash
git fetch upstream
git merge upstream/main
```

Wenn es Konflikte gibt, lösten Sie diese bitte lokal und pushen danach wieder auf ihren Branch.

---

## Tipps

- Nutzen Sie sprechende Commit-Messages  
- Arbeiten Sie als Team auf demselben Branch pro Aufgabe  
- Der Merge Request wird zur Bewertung genutzt  
- Ein Merge Request besteht üblicherweise aus mehren Commits. 


---

## Mitwirken
Weiterentwicklungen zu diesem Projekt sind willkommen.
Bitte verwenden Sie Pull Requests für Änderungen.

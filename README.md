README File - Karteikartensystem (Carl,David,Yilllind)

Funktionen beschrieb:
1) Lernen: Das ist der Lernteil des Karteikarten-Programms. Er arbeitet wie ein persönlicher Lern-Trainer für den Benutzer. Die Aufgabe dieses Skripts ist es, dafür zu sorgen, dass der Benutzer das Wissen wirklich abrufen kann. Zuerst werden alle Karten gesammelt. Wenn der Benutzer nur ein bestimmtes Thema üben möchte (zum Beispiel "Erdkunde"), kann er das über die Stichwörter (Tags) einstellen, und alle anderen Karten werden ausgeblendet. Um den Lerneffekt zu steigern, werden die Karten komplett durchgemischt, damit sich der Benutzer nicht die Reihenfolge merkt. Dann beginnt die Übung: Der Benutzer sieht die Frage, denkt nach, drückt die Eingabetaste und sieht dann die Antwort. Er bewertet sich selbst sofort (Richtig oder Falsch). Diese Information über den Erfolg speichert das Programm sofort ab. Das Allerwichtigste: Am Ende des Lernens wird der gesamte Fortschritt und die Lernstände des Benutzers fest gesichert. Das Programm schreibt diese Daten auf die Festplatte, damit sie dauerhaft gespeichert sind. Wenn der Benutzer das Programm beendet oder der Computer ausgeschaltet wird, sind die Erfolge nicht verloren, sondern warten sicher auf den Benutzer, wenn er das nächste Mal weitermacht.
   
3) Prüfungsmodus
   
4) Bearbeiten
Die Funktion hinzufügen() dient dazu, eine neue Karteikarte in das bestehende Karteikartensystem aufzunehmen. Bei der Nutzung dieser Funktion wird der Benutzer zunächst dazu aufgefordert, eine Frage und eine dazugehörige Antwort einzugeben. Diese beiden Felder müssen zwingend ausgefüllt werden, da das System sicherstellt, dass keine leeren Einträge angelegt werden können. Zusätzlich besteht die Möglichkeit, Tags zu vergeben, die optional sind und durch Semikolons getrennt eingegeben werden können. Tags dienen der thematischen Zuordnung der Karteikarten und erleichtern dem Benutzer später das Filtern oder themenspezifische Lernen. Nachdem alle Eingaben vorgenommen wurden, erstellt das Programm ein neues Datenobjekt, welches die Frage, die Antwort, die vergebenen Tags sowie die Zähler für richtige und falsche Antworten enthält. Diese Werte werden initial auf null gesetzt. Anschliessend wird die neue Karteikarte der bestehenden Liste hinzugefügt und dauerhaft in der Datei gespeichert. Damit erweitert die Funktion hinzufügen() das Karteikartensystem um neue Inhalte und stellt sicher, dass diese auch nach Beenden des Programms erhalten bleiben.



6) Löschen
Die Funktion löschen() ermöglicht es dem Benutzer, eine vorhandene Karteikarte dauerhaft aus dem Karteikartensystem zu entfernen. Zunächst zeigt das Programm alle gespeicherten Karteikarten an, damit der Benutzer eine klare Übersicht erhält und die gewünschte Karte eindeutig auswählen kann. Die Auswahl erfolgt über die Eingabe der entsprechenden Kartennummer, wobei eine Sicherheitsabfrage eingebaut ist, um versehentliches Löschen zu verhindern. Nachdem der Benutzer eine Karte ausgewählt hat, wird er ausdrücklich gefragt, ob er diese wirklich löschen möchte. Erst wenn diese Frage mit „j“ bestätigt wird, entfernt das Programm die Karte endgültig aus der Liste. Anschliessend wird der aktualisierte Kartenbestand sofort in der Datei gespeichert, sodass die gelöschte Karte auch nach einem Neustart des Programms nicht mehr verfügbar ist. Die Funktion löschen() stellt damit sicher, dass der Benutzer jederzeit Kontrolle über seine Daten hat und nicht mehr benötigte oder fehlerhafte Karteikarten unkompliziert und sicher aus dem System entfernen kann.

7) Hinzufügen
   
0) Prgramm Beenden

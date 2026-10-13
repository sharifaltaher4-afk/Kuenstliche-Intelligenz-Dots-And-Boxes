# Aufgabe P1: Demo von Python-Konzepten


# 1. ------------------------Dynamische Typisierung & Duck Typing------------------------
class Duck:
    def quack(self):
        print("Quack! Ich bin eine Ente")
    def fly(self):
        print("Fly! Ich bin eine Ente")
class Person:
    def quack(self):
        print("Ich imitiere eine Ente: Quack!")

# Diese Mathode kann mit jedem Obj. arbeiten der die Methode .quack besitzt
def make_it_quack(obj):
    #Duck Typing: Es ist egal welche klasse das Obj. hat,
    #solange dieses obj. die Methode .quack() besitzt
    obj.quack()

# Diese Mathode kann mit jedem Obj. arbeiten der die Methode .fly() besitzt
def make_it_fly(objek):
    objek.fly()
# 2. --------------------------Listen-Comprehension------------------------
#Eine Listen Comprehension ist eine kompakte, ausdrucksstarke Schreibweise in Python, um
# aus einer vorhandenen Sequenz (Liste, Range, String, etc.) eine neue Liste zu erzeugen, indem
# man auf jedes Element einen Ausdruck anwendet und optional eine Bedingung filtert.
# [ausdruck for element in iterierbares_objekt if bedingung]
# ausdruck:  Was mit jedem Element passieren soll (z.B. x*2, x.upper())
# Für jedes El. x aus einer Liste 'lst' : füre einen Ausdruck aus abhängig von x &  gebe eine neue Ergebnis-Liste zurück
ersteGanzZahlenListe = [0,1,-1,2,-2,3,-3,4,-4,5,-5,6,-6,7,-7]

#Quadrate Zahlen
ergebnisListe=[x**2 for x in ersteGanzZahlenListe]
#Gerade Quadrate Zahlen
geradeErgebnisListe = [x**2 for x in ersteGanzZahlenListe if x%2 == 0]



#3.--------------------------Funktion als Objekte------------------------
#Hier werden Funktionen wie Variablen behandelt (First-Class Citizens)
# Sie können in Listen gespeichert und als Parameter an andere Funktionen übergeben werden

def plus(x,y):
    return x+y
def minus(x,y):
    return x-y

rechenarten =[plus,minus]

def berechnen(rech,x,y):
    return rech(x,y)





if __name__ == '__main__':
    print("-------- P1.1 Duck Typing---------")
    make_it_quack(Duck())
    make_it_quack(Person())
    print("-------- Person--------")
    listOfObjectsToTestDetectingTypesToRuntim = [Duck(),Person()]
    for obj in listOfObjectsToTestDetectingTypesToRuntim:
        make_it_quack(obj)
        #make_it_fly(obj)#Nachteil von der dynamischen Typisierung; erst zur Laufzeit zu entdecekn. bei anderen statisch typisierten Sprachen z.BJava wäre das bereits beim kompilieren aufgefallen

    print("--------P1.2 Listen-Comprehension  ---------")
    print(ergebnisListe)
    print(geradeErgebnisListe)

    print("--------P1.3 Funktion als Objekte  ---------")

    rechenart=plus
    print("Addition:",rechenart(11,10))
    for op in rechenarten:
        print("Ergebis:",berechnen(op,5,2))



    print("-------- P1.4 Lambdas ---------")
    # Lambdas sind anonyme Funktionen die direkt verwendet werden können

    zahlen = [1, 2, 3, 4, 5, 6, 7, 8]

    # Lambda mit map (alle Zahlen werden verdoppelt)
    double = list(map(lambda x: x * 2, zahlen))
    print("Verdoppelte Zahlen:", double)

    # Lambda mit filter (nur gerade Zahlen behalten)
    gerade_zahlen = list(filter(lambda x: x % 2 == 0, zahlen))
    print("Gerade Zahlen:", gerade_zahlen)

    # Lambda mit sorted (Wörter nach dem ersten Buchstaben sortieren)
    woerter = ["eins", "zwei", "drei", "vier", "fünf"]
    woerter_sortiert = sorted(woerter, key=lambda x: x[0])
    print("Sortierte Wörter:", woerter_sortiert)
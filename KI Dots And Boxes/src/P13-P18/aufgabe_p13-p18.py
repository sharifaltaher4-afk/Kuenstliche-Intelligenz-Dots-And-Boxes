from nltk.sem import Expression
from nltk.sem.logic import (
    LogicParser,
    AndExpression,
    OrExpression,
    ImpExpression,
    IffExpression,
    NegatedExpression
)
from nltk.sem.evaluate import Valuation, Model


# ==========================================
# Hilfsfunktion Rekrusive Baumausgabe
# ==========================================
def print_tree(node, level=0):
    """
    Traversiert den syntaktischen Baum (Parse Tree) rekursiv und
    gibt die internen NLTK-Klassennamen hierarchisch aus.
    """
    indent = "  " * level
    print(f"{indent}{type(node).__name__}: {node}")
    if hasattr(node, "first"):
        print_tree(node.first, level + 1)
    if hasattr(node, "second"):
        print_tree(node.second, level + 1)
    if hasattr(node, "term"):
        print_tree(node.term, level + 1)


# ==========================================
# Aufgabe p14: Logik Parser
# ==========================================
def aufgabe_p14():
    print("\n" + "=" * 40)
    print("=== Aufgabe P14: Logic Parser ===")
    print("=" * 40)
    read_expr = Expression.fromstring
    # Repräsentiert die Konjunktive Normalform (KNF)
    formula = read_expr("((A | B | C) & (A | B | -C) & (-A | B | C) & (-A | -B | C))")
    print(f"Geparste Formel:\n{formula}\n")
    print("Hierarchische Baum-Struktur (Parse Tree):")
    print_tree(formula)


# ==========================================
# Aufgabe P15: KB
# ==========================================
class KnowledgeBase:
    def __init__(self):
        """Initialisiert eine KB als Menge/Liste von Sätzen (Folie 35)."""
        self.sentences = []
        self.parser = LogicParser()

    def tell(self, sentence_string):
        """Fügt der KB einen neuen Satz hinzu (TELL)."""
        parsed_expr = self.parser.parse(sentence_string)
        self.sentences.append(parsed_expr)
        print(f"KB TELL: Satz erfolgreich hinzugefügt -> {parsed_expr}")

    def show(self):
        """Zeigt den aktuellen Speicherinhalt an."""
        print(f"\nInhalt der Knowledge Base ({len(self.sentences)} Sätze):")
        for i, sentence in enumerate(self.sentences, start=1):
            #print(f"  Satz {i}: {sentence.__dict__}")
            print(f"  Satz {i}: {sentence}")

    #Aufgabe 18 zusatz
    #----------------------------------------------------------------------

    def tt_entails(self, alpha_string):
        """Prüft universell, ob die KB die übergebene Aussage impliziert."""

        #String umwandlung
        alpha = self.parser.parse(alpha_string)
        symbols = set()

        for sentence in self.sentences:
            symbols.update(get_symbols(sentence))

        symbols.update(get_symbols(alpha))

        return self.tt_check_all(
            alpha,
            list(symbols),
            {}
        )

    def tt_check_all(self, alpha, symbols, model):
        # Basisfall: Wenn keine Symbole mehr übrig sind, bewerte das Modell
        # Zeile 2
        if len(symbols) == 0:
            kb_true = all(pl_true(sentence, model) for sentence in self.sentences)
            if kb_true:
                return pl_true(alpha, model)
            return True

        P = symbols[0]
        rest = symbols[1:]
        model_true = model.copy()
        model_true[P] = True
        model_false = model.copy()
        model_false[P] = False
        # Rekursiver Aufruf: Die Implikation muss in beiden Zweigen halten
        return (self.tt_check_all(alpha, rest, model_true) and
                self.tt_check_all(alpha, rest, model_false))

#------------------------------------------------------------------------
def aufgabe_p15():
    print("\n" + "=" * 40)
    print("=== Aufgabe P15: Knowledge Base ===")
    print("=" * 40)
    kb = KnowledgeBase()

    #  aus dem Aufgabenblatt
    kb.tell("(A & C) -> (B | D)")
    kb.tell("(A & C) <-> (B | D)")
    kb.tell("(A -> C) <-> (B -> D)")

    # 2 zusätzliche nicht-triviale Sätze
    kb.tell("(-A & -B) -> -C")
    kb.tell("(A | B) -> (C & D)")

    kb.show()
    return kb  # Wir geben die KB zurück, um sie in P16 nutzen zu können


# ==========================================
# Aufgabe p16: Logic Kalkulator und PL-True
# ==========================================
def pl_true(sentence, model):
    """
    Evaluiert eigenständig den Wahrheitswert eines NLTK Logik Satzes
    auf Basis eines gegebenen Modells (Syntax Knoten Traversierung).
    """
    # Dynamische Ermittlung der NotExpression-Klasse zur Umgehung von Importfehlern
    NotExpressionTypes = (Expression.fromstring("-A").__class__, NegatedExpression)

    # Fall 1: Atomare Variable / Symbol (Blatt des Baumes)
    # Jedes Blatt in NLTK (egal ob ConstantExpression oder FunctionVariableExpression)
    # besitzt das Attribut 'variable', das seinen Namen hält.
    if hasattr(sentence, 'variable'):
        variable_name = str(sentence.variable)#holt zb A

        # Kompatibilität für NLTK-Modellobjekte
        if hasattr(model, 'valuation'):
            from nltk.sem.logic import Variable
            var_obj = Variable(variable_name)
            if var_obj in model.valuation:
                return model.valuation[var_obj]
            elif variable_name in model.valuation:
                return model.valuation[variable_name]

        # Kompatibilität für native Python-Dictionaries
        elif isinstance(model, dict) and variable_name in model:
            return model[variable_name]

        raise ValueError(f"Variable '{variable_name}' nicht im Modell definiert!")

        # Fall 2: Negation (-A)
    elif isinstance(sentence, NotExpressionTypes):
        return not pl_true(sentence.term, model)

        # Fall 3: Konjunktion (A & B)
    elif isinstance(sentence, AndExpression):
        return pl_true(sentence.first, model) and pl_true(sentence.second, model)

        # Fall 4: Disjunktion (A | B)
    elif isinstance(sentence, OrExpression):
        return pl_true(sentence.first, model) or pl_true(sentence.second, model)

        # Fall 5: Implikation (A -> B)
    elif isinstance(sentence, ImpExpression):
        return (not pl_true(sentence.first, model)) or pl_true(sentence.second, model)

        # Fall 6: Äquivalenz (A <-> B)
    elif isinstance(sentence, IffExpression):
        return pl_true(sentence.first, model) == pl_true(sentence.second, model)

    else:
        raise TypeError(f"Unbekannter Ausdruckstyp: {type(sentence)} bei Knoten: {sentence}")



def aufgabe_p16():
    print("\n" + "=" * 40)
    print("=== Aufgabe P16: Logic-Kalkulator & PL-True ===")
    print("=" * 40)

    # 1. Wir holen uns eine befüllte KB aus P15
    kb = KnowledgeBase()
    kb.tell("(A & C) -> (B | D)")
    kb.tell("(A & C) <-> (B | D)")
    kb.tell("(A -> C) <-> (B -> D)")
    kb.tell("(-A & -B) -> -C")
    kb.tell("(A | B) -> (C & D)")

    # 2. Definiere das Modell m
    # m := { A : true, B : true, C : false } -> wir ergänzen D: false, damit alle Sätze auswertbar sind
    val = Valuation([('A', True), ('B', True), ('C', False), ('D', False)])
    dom = val.domain  #set()
    modell_m = Model(dom, val)

    print(f"\nGegebenes Modell m (Belegung): A=True, B=True, C=False, D=False\n")
    print("Berechnete Wahrheitswerte (Eigenes PL-True):")

    # 3. Iteriere über alle Sätze der KB und evaluiere sie eigenständig
    for i, satz in enumerate(kb.sentences, start=1):
        wahrheitswert = pl_true(satz, modell_m)
        print(f"  Satz {i}: {str(satz):<25} -> PL-True(s, m) = {wahrheitswert}")

def aufgabe_p17():
    print("\n" + "=" * 40)
    print("=== Aufgabe P17: NLTK PL-True & Vergleich ===")
    print("=" * 40)

    #1. KB identisch zu p15/p16 aufbauen
    kb = KnowledgeBase()
    kb.tell("(A & C) -> (B | D)")
    kb.tell("(A & C) <-> (B | D)")
    kb.tell("(A -> C) <-> (B -> D)")
    kb.tell("(-A & -B) -> -C")
    kb.tell("(A | B) -> (C & D)")

    #2. modell m identisch zu p16 definieren
    val = Valuation([('A', True), ('B', True), ('C', False), ('D', False)])
    dom = val.domain#set()
    modell_m = Model(dom, val)

    # Für nltk.evaluate() ist eine Assignment-Objekt (g) zwingend erfoderlich
    #um Variablenbelegungen im logischen Universum zu tracken(Folie 35)
    from nltk.sem.evaluate import Assignment
    g = Assignment(dom)
    print(f"\nGegebenes Modell m (Belegung): A=True, B=True, C=False, D=False")
    print(f"{'Satz':<25} | {'Eigenes PL-True':<15} | {'NLTK Model.evaluate':<20} | {'Identisch?'}")
    print("-" * 75)

    #3. Schleife über allw Sätze zum direkten mathematischen Abgleich
    for satz in kb.sentences:
        # A) Wert über die eigene Funktion aus p16
        wert_eigen = pl_true(satz, modell_m)

        # B) Wert über die native NLTK-Funktionalität
        # .evaluate() gibt ein Dictionary oder Set zurück. Bei Aussagenlogik
        # liefert es direkt den Wahrheitswert für die Formel.
        wert_nltk = modell_m.evaluate(str(satz), g)

        # C) Analyse auf Gleichheit
        match = (wert_eigen == wert_nltk)

        print(f"{str(satz):<25} | {str(wert_eigen):<15} | {str(wert_nltk):<20} | {match}")


# ==========================================
# Aufgabe P18
# ==========================================

def get_symbols(expr):
    symbols = set()
    #holt die Variable
    if hasattr(expr, 'variable'):
        symbols.add(str(expr.variable))
    #links
    if hasattr(expr, 'first'):
        symbols.update(get_symbols(expr.first))
    #rechts
    if hasattr(expr, 'second'):
        symbols.update(get_symbols(expr.second))
    #vorzeichen
    if hasattr(expr, 'term'):
        symbols.update(get_symbols(expr.term))
    return symbols




def aufgabe_p18():
    print("\n" + "=" * 40)
    print("=== Aufgabe P18: TT-Entails ===")
    print("=" * 40)

    kb=KnowledgeBase()

    kb.tell("A & B")
    kb.tell("(A & B) -> C")
    kb.tell("D | C")
    #kb.tell("A->C")
    #kb.tell("B->D")
    #kb.tell("(A & C) -> (B | D)")
    #kb.tell("(A & C) <-> (B | D)")
    #kb.tell("(A -> C) <-> (B -> D)")
    #kb.tell("(-A & -B) -> -C")
    #kb.tell("(A | B) -> (C & D)")

    queries = [

        "A",
        "B",
        "C",
        "D",
        "A & B",
        "C & D",
        "A & C",
        "C | D",


    ]


    for query in queries:
        result = kb.tt_entails(query)
        print(f"KB |= {query:<20}: {result}")


def aufgabe_p20():
    print("\n" + "=" * 65)
    print("=== Aufgabe P20: Vollständige Wahrheitstafel ===")
    print("=" * 65)

    kb = KnowledgeBase()

    # Alle Sätze in dieselbe KB laden
    kb.tell("(A | B | C) & (A | B | -C) & (-A | B | C) & (-A | -B | C)")
    kb.tell("(A | B | C) & (A | -C) & (-A | B | C | D) & (-A | -B | C)")
    kb.tell("(A | B | C) & (A | -C) & (-A | (B & C) | D) & (-A | -B | C)")
    kb.tell("(A | B | C) & (A | -C) & ((-A | B ) & (C | D)) & (-A | -B | C)")
    kb.tell("(A | B | C) & (A | -C) & (((-A | B ) & C) | D ) & (-A | -B | C)")

    # Queries außerhalb der rekursiven Schleife parsen
    alpha1 = kb.parser.parse("A -> B -> C -> D")
    alpha2 = kb.parser.parse("A -> (B -> (C -> D))")

    # Symbole fixieren für eine deterministische Tabellenreihenfolge
    symbols = ["A", "B", "C", "D"]
    row_counter = 1

    print(f"\n{'Nr.':<4} | {'A':<6} {'B':<6} {'C':<6} {'D':<6} || {'KB Status':<12} || {'α1':<6} || {'α2':<6}")
    print("-" * 75)

    def tt_check_all_p20(model, depth):
        nonlocal row_counter  # Ermöglicht Modifikation der äußeren Variable
        if depth == len(symbols):
            # Evaluierung gegen alle Sätze in der KB
            kb_true = all(pl_true(sentence, model) for sentence in kb.sentences)
            a1_true = pl_true(alpha1, model)
            a2_true = pl_true(alpha2, model)

            # Markierung der Modelle, bei denen die KB wahr ist mit (*)
            kb_marker = "True  (*)" if kb_true else "False"
            print(
                f"{row_counter:<4} | "
                f"{str(model['A']):<6} {str(model['B']):<6} {str(model['C']):<6} {str(model['D']):<6} || "
                f"{kb_marker:<12} || {str(a1_true):<6} || {str(a2_true):<6}"
            )
            row_counter += 1
            return

        P = symbols[depth]
        # Generiere systematisch True- und False-Zweige
        for value in [True, False]:
            model[P] = value
            tt_check_all_p20(model, depth + 1)

    # Generierung starten
    tt_check_all_p20({}, 0)



if __name__ == "__main__":
    #aufgabe_p14()
    #aufgabe_p15()
    #aufgabe_p16()
    #aufgabe_p17()
    #aufgabe_p18()
    aufgabe_p20()
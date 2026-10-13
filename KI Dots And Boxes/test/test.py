import sys
import os

# hat nicht anders geklappt :/
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from controller import GraphController


# Kontrolltest
def test_edge_selection():
    gc = GraphController()
    assert gc.select_edge_point_number(0, 1, "red") is True
    print("Verbindungen funktionieren")


# falsche Verbindung
def test_invalid_edge():
    gc = GraphController()
    assert gc.select_edge_point_number(0, 8, "red") is False
    print("Keine Verbindung")


# ungültige Nummer (nicht im Grid)
def test_edge_wrong_number():
    gc = GraphController()
    assert gc.select_edge_point_number(10, 1, "red") is False
    print("Zu große Nummer")

## überprüfen, ob die Box richtig erkannt wird
def test_no_box_created():
    gc = GraphController()

    gc.select_edge_point_number(0, 1, "red")
    gc.select_edge_point_number(1, 2, "red")

    gc.check_box()

    assert len(gc.boxes) == 0
    print("Keine Box")


# keine Zahl
def test_edge_no_number():
    gc = GraphController()
    try:
        result = gc.select_edge_point_number("dennis", 1, "red")
        assert result is False
        print("Nicht abgefangen")
    except:
        print("Fehler abgefangen (keine Zahl)")


# Box Kontrolle
def test_box_detection():
    gc = GraphController()

    gc.select_edge_point_number(0, 1, "red")
    gc.select_edge_point_number(1, 4, "red")
    gc.select_edge_point_number(3, 4, "red")
    gc.select_edge_point_number(0, 3, "red")

    gc.check_box()

    assert len(gc.boxes) == 1
    print("Box wurde erkannt")

def test_double_box_detection():
    gc = GraphController()
    #Baue zwei Boxen vor, die eine gemeinesame Mittellinie haben (1,4)
    #Box 1 Links
    gc.select_edge_point_number(0, 1, "red")
    gc.select_edge_point_number(0, 3, "red")
    gc.select_edge_point_number(3, 4, "red")
    #Box 2 Rechts
    gc.select_edge_point_number(1,2,"red")
    gc.select_edge_point_number(2,5,"red")
    gc.select_edge_point_number(4,5,"red")

    # Sicherstellen, dass bis hierhin noch nichts gezählt wurde
    # (Wir haben check_box() noch nicht aufgerufen)
    assert len(gc.boxes) == 0
    #jetzt die entscheidende Mittellinie ziehen
    gc.select_edge_point_number(1, 4, "red")

    points_won = gc.check_box() #sollte 2 zurückgeben

    assert points_won == 2
    assert len(gc.boxes) == 2
    print("Double box wurden erkannt")

# Spielende Test
def test_game_finishing():
    gc = GraphController()

    # Box 1
    gc.select_edge_point_number(0, 1, "red")
    gc.select_edge_point_number(1, 4, "red")
    gc.select_edge_point_number(3, 4, "red")
    gc.select_edge_point_number(0, 3, "red")
    gc.check_box()

    # Box 2
    gc.select_edge_point_number(1, 2, "red")
    gc.select_edge_point_number(2, 5, "red")
    gc.select_edge_point_number(4, 5, "red")
    gc.select_edge_point_number(1, 4, "red")
    gc.check_box()

    # Box 3
    gc.select_edge_point_number(3, 4, "red")
    gc.select_edge_point_number(4, 7, "red")
    gc.select_edge_point_number(6, 7, "red")
    gc.select_edge_point_number(3, 6, "red")
    gc.check_box()

    # Box 4
    gc.select_edge_point_number(4, 5, "red")
    gc.select_edge_point_number(5, 8, "red")
    gc.select_edge_point_number(7, 8, "red")
    gc.select_edge_point_number(4, 7, "red")
    gc.check_box()

    assert len(gc.boxes) == 4
    print("Alle Boxen wurden erkannt")


if __name__ == "__main__":
    test_edge_selection()
    test_invalid_edge()
    test_edge_wrong_number()
    test_edge_no_number()
    test_box_detection()
    test_game_finishing()
    test_double_box_detection()
    print("Alle Tests bestanden!")
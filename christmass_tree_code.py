import random
0

# ==============================================================================
# CZĘŚĆ 1: KLASA WĘZŁA (Node)
# ==============================================================================
class Node:
    __slots__ = ('key', 'left', 'right')

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

    @property
    def is_bauble(self):
        """Zwraca True, jeśli węzeł jest bombką (klucz nieparzysty)."""
        return self.key % 2 != 0

    @property
    def is_light(self):
        """Zwraca True, jeśli węzeł jest światełkiem (klucz parzysty)."""
        return self.key % 2 == 0

    @property
    def light_color(self):
        """Zwraca kolor światełka ('yellow' lub 'red') lub None."""
        if not self.is_light:
            return None
        if self.key % 4 == 0:
            return "yellow"
        return "red"


# ==============================================================================
# CZĘŚĆ 2: KLASA CHOINKI (ChristmasTree)
# ==============================================================================
class ChristmasTree:
    __slots__ = ('root',)

    def __init__(self):
        self.root = None

    # --------------------------------------------------------------------------
    # METODY PODSTAWOWE
    # --------------------------------------------------------------------------
    def insert(self, key):
        """
        Wstawia klucz tylko jeśli nie istnieje w drzewie.
        Akceptuje tylko liczby naturalne (int >= 0).
        """
        if not isinstance(key, int) or key < 0:
            print(f"Błąd: '{key}' - Dozwolone są tylko liczby naturalne.")
            return

        if self.member(key):
            # print(f"Pominięto: Element {key} już istnieje w drzewie.")
            return

        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if key < node.key:
            if node.left is None:
                node.left = Node(key)
            else:
                self._insert_recursive(node.left, key)
        else:
            if node.right is None:
                node.right = Node(key)
            else:
                self._insert_recursive(node.right, key)

    def delete(self, key):
        if not isinstance(key, int) or key < 0:
            print("Dozwolone są tylko liczby naturalne.")
            return
        if self.root is None:
            print("Nie ma nic do usunięcia (drzewo puste).")
            return
        if not self.member(key):
            print(f"Element {key} nie istnieje w drzewie.")
            return

        self.root = self._delete_recursive(self.root, key)
        print(f"Usunięto element {key}.")

    def _delete_recursive(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            min_larger_node = self._get_min(node.right)
            node.key = min_larger_node.key
            node.right = self._delete_recursive(node.right, min_larger_node.key)
        return node

    def _get_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    def member(self, key):
        curr = self.root
        while curr is not None:
            if key == curr.key:
                return True
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return False

    # --------------------------------------------------------------------------
    # METODY POMOCNICZE
    # --------------------------------------------------------------------------
    def _count_descendants(self, node):
        if node is None:
            return 0
        return 1 + self._count_descendants(node.left) + self._count_descendants(node.right)

    def _count_lights(self, node):
        if node is None:
            return 0
        current_val = 1 if node.is_light else 0
        return current_val + self._count_lights(node.left) + self._count_lights(node.right)

    def _has_red_light(self, node):
        if node is None:
            return False
        if node.light_color == "red":
            return True
        return self._has_red_light(node.left) or self._has_red_light(node.right)

    # --------------------------------------------------------------------------
    # METODY PROJEKTOWE
    # --------------------------------------------------------------------------
    def is_illuminated(self):
        return self._check_illuminated(self.root)

    def _check_illuminated(self, node):
        if node is None:
            return True
        is_leaf = (node.left is None and node.right is None)
        if not is_leaf:
            lights_below = self._count_lights(node.left) + self._count_lights(node.right)
            if lights_below == 0:
                return False
        return self._check_illuminated(node.left) and self._check_illuminated(node.right)

    def is_evenly_illuminated(self):
        if not self.is_illuminated():
            return False
        return self._check_evenly_illuminated(self.root)

    def _check_evenly_illuminated(self, node):
        if node is None:
            return True
        left_lights = self._count_lights(node.left)
        right_lights = self._count_lights(node.right)
        if abs(left_lights - right_lights) > 1:
            return False
        return self._check_evenly_illuminated(node.left) and self._check_evenly_illuminated(node.right)

    def is_stylish(self):
        return self._check_stylish(self.root)

    def _check_stylish(self, node):
        if node is None:
            return True
        if node.is_bauble:
            has_red_left = self._has_red_light(node.left)
            has_red_right = self._has_red_light(node.right)
            if has_red_left or has_red_right:
                return False
        return self._check_stylish(node.left) and self._check_stylish(node.right)

    def is_stable(self):
        return self._check_stable(self.root)

    def _check_stable(self, node):
        if node is None:
            return True
        count_left = self._count_descendants(node.left)
        count_right = self._count_descendants(node.right)
        if abs(count_left - count_right) > 2:
            return False
        return self._check_stable(node.left) and self._check_stable(node.right)

    def the_longest_colourful_path(self):
        lancuchy = self._colourful_paths()
        if not lancuchy:
            return 0
        dlugosci_lancuchow = []
        for i in range(len(lancuchy)):
            dlugosci_lancuchow.append(len(lancuchy[i]))
        return max(dlugosci_lancuchow)

    def _colourful_paths(self):
        if self.root is None:
            return []
        lancuchy = []

        def _dfs(node, curr_path):
            curr_path.append(node.key)
            # Kolorowy łańcuch to tylko światełka (przerywany przez bombki)
            if node.left is None and node.right is None and node.is_light:
                lancuchy.append(list(curr_path))

            # Idziemy dalej tylko jeśli to światełko (lub korzeń)
            if node == self.root or node.is_light:
                if node.left is not None:
                    _dfs(node.left, curr_path)
                if node.right is not None:
                    _dfs(node.right, curr_path)
            curr_path.pop()

        _dfs(self.root, [])
        return lancuchy

    def _monochromatic_paths(self):
        if self.root is None:
            return []
        lancuchy = []

        def _dfs(node, curr_path, n_of_yellow=0, n_of_red=0):
            curr_path.append(node.key)
            if node.light_color == 'yellow':
                n_of_yellow += 1
            if node.light_color == 'red':
                n_of_red += 1

            # Monochromatyczny może zawierać bombki
            if node.left is None and node.right is None:
                if (n_of_red == 0 and n_of_yellow != 0) or (n_of_yellow == 0 and n_of_red != 0):
                    lancuchy.append(list(curr_path))

            if node.left is not None:
                _dfs(node.left, curr_path, n_of_yellow, n_of_red)
            if node.right is not None:
                _dfs(node.right, curr_path, n_of_yellow, n_of_red)
            curr_path.pop()

        _dfs(self.root, [])
        return lancuchy

    def _traditional_paths(self):
        if self.root is None:
            return []
        lancuchy = []

        def _dfs(node, curr_path, n_of_yellow=0, n_of_red=0):
            curr_path.append(node.key)
            if node.light_color == 'yellow':
                n_of_yellow += 1
            if node.light_color == 'red':
                n_of_red += 1

            # Tradycyjny może zawierać bombki
            if node.left is None and node.right is None:
                if n_of_red == n_of_yellow:
                    lancuchy.append(list(curr_path))

            if node.left is not None:
                _dfs(node.left, curr_path, n_of_yellow, n_of_red)
            if node.right is not None:
                _dfs(node.right, curr_path, n_of_yellow, n_of_red)
            curr_path.pop()

        _dfs(self.root, [])
        return lancuchy

    def is_elegant(self):
        if len(self._colourful_paths()) >= len(self._monochromatic_paths()):
            return True
        return False

    def is_traditional(self):
        if not self.is_stable():
            return False
        if not self.is_illuminated():
            return False
        if not self._traditional_paths():
            return False
        return True

    def is_ready(self):
        if not self.is_stable():
            return False
        if not self.is_illuminated():
            return False
        if not self._colourful_paths():
            return False
        if not self._monochromatic_paths():
            return False
        return True

    # --------------------------------------------------------------------------
    # WIZUALIZACJA
    # --------------------------------------------------------------------------
    def print_tree(self):
        if self.root is None:
            print("Drzewo jest puste!")
            return
        print("\n--- STRUKTURA CHOINKI ---")
        self._print_recursive(self.root, 0)
        print("-------------------------")

    def _print_recursive(self, node, level):
        if node is not None:
            self._print_recursive(node.right, level + 1)
            indent = "    " * level
            typ = "Światło" if node.is_light else "Bombka"
            kolor = f" ({node.light_color})" if node.is_light else ""
            print(f"{indent}-> {node.key} [{typ}{kolor}]")
            self._print_recursive(node.left, level + 1)


# ==============================================================================
# MODUŁ TESTOWY DLA RAPORTU
# ==============================================================================
def run_report_tests():
    print("\n" + "#" * 60)
    print("      AUTOMATYCZNE TESTY DO RAPORTU")
    print("#" * 60)

    def build(keys):
        t = ChristmasTree()
        for k in keys:
            t.insert(k)
        return t

    # --- KONSTRUKCJA DRZEW TESTOWYCH ---

    # 1. Drzewo Idealne (31 węzłów) - same żółte światła
    # Gwarantuje wynik TRUE dla większości cech dzięki idealnej symetrii i braku bombek.
    keys_perfect_yellow = [
        64, 32, 96, 16, 48, 80, 112, 8, 24, 40, 56, 72, 88, 104, 120,
        4, 12, 20, 28, 36, 44, 52, 60, 68, 76, 84, 92, 100, 108, 116, 124
    ]

    # 2. Drzewo "Lekko Niestabilne" (FALSE dla Stable)
    # Różnica potomków = 3 (Limit = 2). Testuje granicę tolerancji algorytmu.
    keys_borderline_unstable = [
        100,
        90, 80, 70, 60, 50, 40, 30, 20, 10, 5,  # Lewa strona: 10 elementów
        110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230  # Prawa strona: 13 elementów
    ]

    # 3. Drzewo "Prawie Równo Oświetlone" (FALSE dla Evenly Illuminated)
    # Różnica świateł = 2 (Limit = 1). Testuje precyzję zliczania świateł.
    keys_borderline_uneven = [
        100,
        50, 25, 4, 8, 12, 16,  # Lewo: 4 światła
        150, 152, 154, 156, 158, 160, 175, 177, 179, 181, 183, 185  # Prawo: 6 świateł
    ]

    # 4. Drzewo "Podstępnie Niestylowe" (FALSE dla Stylish)
    # Drzewo wygląda poprawnie na górze, ale głęboko w strukturze
    # bombka (51) znajduje się nad czerwonym światłem (2).
    keys_sneaky_unstylish = [
                                100, 200, 300, 400, 500,
                                50, 25, 40,
                                10, 5,
                                51, 2
                            ] + [600 + x for x in range(10)]

    # 5. Drzewo "Tradycyjne" (TRUE dla Traditional)
    # Drzewo jest stabilne, oświetlone i posiada ścieżkę do węzła '2',
    # która ma idealny balans kolorów (3 żółte, 3 czerwone).
    keys_traditional = [
        # Baza góry
        100, 50, 150,
        # Poziom 2
        24, 76, 124, 176,
        # Poziom 3
        10, 38, 62, 90, 110, 138, 162, 190,
        # Wydłużenie ścieżki po lewej (dla balansu kolorów Y-R-Y-R-Y-R)
        4, 2, 36,
        # Balans dla węzła 50 (prawa strona)
        80,
        # Balans dla węzła 150 (lewa i prawa strona)
        130, 192, 194, 164
    ]

    # 6. Drzewo "Nieeleganckie" (FALSE dla Elegant)
    # Bombki umieszczone w kluczowych miejscach przerywają ciągłość łańcuchów kolorowych,
    # ale są wliczane do łańcuchów monochromatycznych, co zmienia wynik porównania.
    keys_unelegant = [
                         100, 51, 4, 151, 152, 201, 204
                     ] + [301 + x * 2 for x in range(15)]

    # --- TEST 1: OŚWIETLONA ---
    print("\n" + "=" * 40)
    print("1. Test cechy: OŚWIETLONA")
    t1 = build(keys_perfect_yellow)
    print(f"CASE A (TRUE) [Drzewo Idealne - same światła] -> {t1.is_illuminated()}")
    t1.print_tree()

    t2 = build([100, 50, 25, 15, 35] + [200 + x for x in range(15)])
    print(f"\nCASE B (FALSE) [Węzeł wewnętrzny (25) ma pod sobą same bombki] -> {t2.is_illuminated()}")
    t2.print_tree()

    # --- TEST 2: RÓWNO OŚWIETLONA ---
    print("\n" + "=" * 40)
    print("2. Test cechy: RÓWNO OŚWIETLONA")
    t3 = build(keys_perfect_yellow)
    print(f"CASE A (TRUE) [Idealna symetria] -> {t3.is_evenly_illuminated()}")
    t3.print_tree()

    t4 = build(keys_borderline_uneven)
    print(f"\nCASE B (FALSE) [Różnica świateł = 2 (Limit=1)] -> {t4.is_evenly_illuminated()}")
    t4.print_tree()

    # --- TEST 3: STYLOWA ---
    print("\n" + "=" * 40)
    print("3. Test cechy: STYLOWA")
    t5 = build(keys_perfect_yellow)
    print(f"CASE A (TRUE) [Brak bombek = stylowa] -> {t5.is_stylish()}")
    t5.print_tree()

    t6 = build(keys_sneaky_unstylish)
    print(f"\nCASE B (FALSE) [Ukryty błąd głęboko: Bombka(51) -> Czerwone(2)] -> {t6.is_stylish()}")
    t6.print_tree()

    # --- TEST 4: STABILNA ---
    print("\n" + "=" * 40)
    print("4. Test cechy: STABILNA")
    t7 = build(keys_perfect_yellow)
    print(f"CASE A (TRUE) [Idealny balans] -> {t7.is_stable()}")
    t7.print_tree()

    t8 = build(keys_borderline_unstable)
    print(f"\nCASE B (FALSE) [Różnica potomków = 3 (Limit=2)] -> {t8.is_stable()}")
    t8.print_tree()

    # --- TEST 5: NAJDŁUŻSZY ŁAŃCUCH ---
    print("\n" + "=" * 40)
    print("5. Test: DŁUGOŚĆ ŁAŃCUCHA")
    t9 = build(keys_perfect_yellow)
    print(f"Drzewo Idealne (wysokość 5). Wynik: {t9.the_longest_colourful_path()}")
    t9.print_tree()

    # --- TEST 6: ELEGANCKA ---
    print("\n" + "=" * 40)
    print("6. Test cechy: ELEGANCKA (Kolorowe >= Mono)")
    t10 = build(keys_perfect_yellow)
    print(f"CASE A (TRUE) [Bez bombek: Kolorowe == Mono] -> {t10.is_elegant()}")
    t10.print_tree()

    t11 = build(keys_unelegant)
    print(f"\nCASE B (FALSE) [Bombki blokują łańcuchy Kolorowe, ale nie Mono] -> {t11.is_elegant()}")
    t11.print_tree()

    # --- TEST 7: TRADYCYJNA ---
    print("\n" + "=" * 40)
    print("7. Test cechy: TRADYCYJNA")
    t12 = build(keys_traditional)
    print(f"CASE A (TRUE) [Istnieje ścieżka z równą liczbą Y i R] -> {t12.is_traditional()}")
    t12.print_tree()

    t13 = build(keys_perfect_yellow)
    print(f"\nCASE B (FALSE) [Brak czerwonych świateł -> brak równowagi] -> {t13.is_traditional()}")
    t13.print_tree()

    # --- TEST 8: GOTOWA ---
    print("\n" + "=" * 40)
    print("8. Test cechy: GOTOWA")
    t14 = build(keys_perfect_yellow)
    print(f"CASE A (TRUE) [Spełnia wszystkie warunki] -> {t14.is_ready()}")
    t14.print_tree()

    t15 = build(keys_borderline_unstable)  # Niestabilna
    print(f"\nCASE B (FALSE) [Niestabilna, więc niegotowa] -> {t15.is_ready()}")
    t15.print_tree()

    print("\n" + "#" * 60)
    input("Naciśnij ENTER, aby wrócić do menu...")


# ==============================================================================
# MENU GŁÓWNE
# ==============================================================================
def main():
    tree = ChristmasTree()
    #print("Program uruchomiony. Choinka jest pusta.")

    while True:
        print("\n" + "=" * 45)
        print("🎄 SYSTEM OBSŁUGI CHOINKI 🎄")
        print("=" * 45)
        print("METODY ANALITYCZNE:")
        print("1. Sprawdź: Oświetlona")
        print("2. Sprawdź: Równo oświetlona")
        print("3. Sprawdź: Stylowa")
        print("4. Sprawdź: Stabilna")
        print("5. Sprawdź: Długość najdłuższego łańcucha kolorowego")
        print("6. Sprawdź: Elegancka")
        print("7. Sprawdź: Tradycyjna")
        print("8. Sprawdź: Gotowa")
        print("-" * 45)
        print("EDYCJA DRZEWA:")
        print("9. RESET (Wyczyść drzewo)")
        print("10. USUŃ element")
        print("11. WYLOSUJ nowe elementy (Dodaj 20 unikalnych liczb)")
        print("12. DODAJ RĘCZNIE (Wpisz własne liczby naturalne)")
        print("13. SPRAWDŹ, czy klucz jest w drzewie")
        print("-" * 45)
        print("INNE:")
        print("14. POKAŻ DRZEWO")
        print("15. GENERUJ RAPORT (Testy Automatyczne + Wizualizacja)")
        print("0. Wyjście")

        wybor = input("\nWybierz opcję: ")

        if wybor == "1":
            wynik = tree.is_illuminated()
            print(f"\nWynik: Choinka {'JEST' if wynik else 'NIE JEST'} oświetlona.")
        elif wybor == "2":
            wynik = tree.is_evenly_illuminated()
            print(f"\nWynik: Choinka {'JEST' if wynik else 'NIE JEST'} równo oświetlona.")
        elif wybor == "3":
            wynik = tree.is_stylish()
            print(f"\nWynik: Choinka {'JEST' if wynik else 'NIE JEST'} stylowa.")
        elif wybor == "4":
            wynik = tree.is_stable()
            print(f"\nWynik: Choinka {'JEST' if wynik else 'NIE JEST'} stabilna.")
        elif wybor == "5":
            wynik = tree.the_longest_colourful_path()
            print(f"\nWynik: Długość najdłuższego łańcucha kolorowego to {wynik}.")
        elif wybor == "6":
            wynik = tree.is_elegant()
            print(f"\nWynik: Choinka {'JEST' if wynik else 'NIE JEST'} elegancka.")
        elif wybor == "7":
            wynik = tree.is_traditional()
            print(f"\nWynik: Choinka {'JEST' if wynik else 'NIE JEST'} tradycyjna.")
        elif wybor == "8":
            wynik = tree.is_ready()
            print(f"\nWynik: Choinka {'JEST' if wynik else 'NIE JEST'} gotowa.")
        elif wybor == "9":
            tree = ChristmasTree()
            print("\n>> Drzewo zostało wyczyszczone.")
        elif wybor == "10":
            value = input("\nWybierz element do usunięcia: ")
            try:
                if not value:
                    print("Nie podano elementu.")
                else:
                    tree.delete(int(value))
            except ValueError:
                print("Dozwolone są tylko liczby naturalne.")
        elif wybor == "11":
            print("\n>> Losuję 20 unikalnych liczb naturalnych...")
            unique_numbers = set()
            # Losujemy unikalne liczby
            while len(unique_numbers) < 20:
                unique_numbers.add(random.randint(1, 100))
            # Dodajemy je w losowej kolejności
            shuffled_numbers = list(unique_numbers)
            random.shuffle(shuffled_numbers)

            for val in shuffled_numbers:
                tree.insert(val)
                print(val, end=" ")
            print("\n>> Gotowe! Dodano 20 unikalnych elementów w losowej kolejności.")

        elif wybor == "12":
            raw_input = input("\nWpisz liczby naturalne oddzielone spacją: ")
            try:
                parts = raw_input.split()
                if not parts:
                    print("Nie podano żadnych liczb.")
                else:
                    valid_numbers = []
                    for part in parts:
                        val = int(part)
                        if val < 0: raise ValueError
                        valid_numbers.append(val)
                    for v in valid_numbers: tree.insert(v)
                    print(f">> Przetwarzanie zakończone.")
            except ValueError:
                print("Dozwolone sa tylko liczby naturalne.")
        elif wybor == "13":
            wartosc = input("\nWybierz klucz do sprawdzenia: ")
            try:
                if not wartosc:
                    print("Nie podano klucza.")
                else:
                    wynik = tree.member(int(wartosc))
                    print(f"\nWynik: W choince {'JEST klucz' if wynik else 'NIE MA klucza'} {wartosc}.")
            except ValueError:
                print("Dozwolone są tylko liczby naturalne.")
        elif wybor == "14":
            tree.print_tree()
        elif wybor == "15":
            run_report_tests()
        elif wybor == "0":
            print("Zamykanie programu...")
            break
        else:
            print("\nNieznana opcja.")


if __name__ == "__main__":
    main()
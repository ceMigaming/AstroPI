## Generalny opis projektu

Pliki:

1. main.py - funkcje:
   - main() - Szymon i Maciek
     1. co 15 sekund odpala update_display()
     2. co 30 sekund odpala:
        - collect_data.magnetometer()
        - collect_data.location()
        - collect_data.calculate()
        - collect_data.save()
   - update_display() - Szymon i Maciek
     1. zmienia zawartość wyświetlacza
2. collect_data.py - funkcje:
   - magnetometer() - Antek
     1. Zbiera dane z magnetometru
   - location() - Antek
     1. Zbiera dane o lokalizacji stacji
   - calculate() - Feliks
     1. Przelicza dane  z magnetometru na kąty( w poziomie, i w pionie)
   - save() - Antek
     1. Zapisuje dane do plików:
        - data01.csv - dane z czujników
        - data02.csv - dane przeliczone
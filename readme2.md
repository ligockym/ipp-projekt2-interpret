Implementační dokumentace k 2. úloze do IPP 2021/2022

Jméno a příjmení: Marián Ligocký

Login: xligoc04

## Interpret

Interpret slúži na vykonanie inštrukcií jazyka IPPCode22 načítaných zo zdrojového súboru vo formáte XML.

### Načítanie inštrukcií, náveští

Inštrukcie načítavame zo zdrojového súboru ak je zadaný, inak zo vstupu. Na čítanie zdrojového XML súboru využívame
knižnicu **ElementTree**. Všetky inštrukcie uložíme do slovníka (dictionary), kde kľúč je parameter `order` a hodnota je
samotný objekt `Instruction`, ktorý obsahuje zoznam argumentov typu `Symbol`.

Následne vyhľadáme inštrukcie `LABEL` a príslušné **náveštia** uložíme opäť do slovníka, kde kľúč je názov náveštia a
hodnota je číslo inštrukcie kam náveštie ukazuje.

### Metódy na vykonávanie inštrukcií

Vytvorili sme viaceré triedy kde sa vykonávajú už konkrétne inštrukcie. Odkaz na konkrétnu metódu v konkrétnej triede je
uložená ako slovník nasledovne a podľa inštrukcie ktorá sa má vykonať sa vyberie správna metóda na vykonanie.

```
jumpManager = JumpManager(self)

self.method_for_opcode = {
    "JUMP": jumpManager.jump,
     "JUMPIFEQ": jumpManager.jumpifeq
     ...
 }
```

Správna metóda sa zavolá s jedným argumentom, inštrukciou.

### Pamäťový model

Interpret obsahuje atribút `self.memory`, ktorý je inicializovaný na objekt triedy `Memory`. Tento objekt drží všetky
premenné definované v rámci **globálneho**, **dočasného** a všetkých **lokálnych rámcov**. Ďalej obsahuje zásobník
volaní. Trieda `Memory` obsahuje metódy pre prácu s premennými a ich hodnotami.

### Ukladanie a práca s premennými

Premenná je ukladaná ako objekt `Variable`, ktorý obsahuje meno a samotnú hodnotu premennej ako objekt typu `Symbol`.
`Symbol` obsahuje atribúty typ a hodnotu. `Symbol` sa používa aj na ukladanie argumentov inštrukcií.

### Chybové stavy

Všetky chybové stavy vrátane sématických a iných chýb sa riešia pomocou špeciálne vytvorenej výnimky `InterpretError`,
ktorá ako prvý argument prijíma číslo chyby `InterpretErrorEnum`.

## Rozšírenie NVI

Objektovo orientovaný návrhový vzor továreň je využitý pri vytváraní inštrukcií v triede `XmlInstructionFactory`. Hlavný
zmysel využitia je v zjednodušení kódu a zapuzdrenia načítavania inštrukcií z XML súboru. Pokiaľ by v budúcnosti
aplikácia mala podporovať napr. načítavanie z JSON súboru, stačilo by vytvoriť `JSONInstructionsFactory` implementujúcu
metódu `load_instructions` a okrem inicializácie správneho továrenského objektu by sa nič iné nemenilo.

Vzhľadom na fakt, že Python priamo nepodporuje rozhranie (interface), samotná továreň nie je prinútená implementovať
metódu `load_instructions` žiadnym jazykovým mechanizmom. 

## Testovací skript

Slúži na spustenie a vyhodnotenie testov slúžiacich na kontrolu analyzátora a interpreta. Testy môžu byť uložené v
zložkách a podzložkách. Skript dovoľuje spúšťať separátne jednotlivé súčasti, rovnako aj spustiť ich zreťazene.

### Načítavanie testov zo zložiek

Pre načítanie všetkých testov sú hľadané všetky súbory v zložke s príponou `.src`. Následne sa skontroluje či existujú
súbory s príponou `.in` a `.rc` a prípadne sa dogenerujú.

### Spúštanie testov

V prípade, že sa má spustiť iba jedna časť - buď analyzátor, alebo interpret, načíta sa súbor so zdrojovým súborom s
príponou `.src` a jeho obsah sa pošle na vstup testovaného skriptu. Porovnajú sa návratové hodnoty (referenčný v
súbore `.rc`), pokiaľ sú oba nula, tak sa vykoná porovnanie obsahu.

Pokiaľ sa majú spustiť oba skripty za sebou, tak sa zdrojový súbor najprv použije ako vstup pre analyzátor a výstup sa
uloží s príponou `.parser.out` a pustí sa ako vstup pre interpret (spolu s prípadným súborom s príponou `.in`, ktorý
obsahuje vstupy pre interpret). Až na konci sa porovnajú návratové kódy (referenčný kód je v súbore `.rc`) a v prípade
oboch nulových kódov sa porovná obsah. Interpret sa púšťa iba pokiaľ výstup z analyzátora bol úspešný, teda vrátil
nulový návratový kód.

### Porovnanie obsahu

Obsah testových súborov sa vykonáva pomocou utilitky `diff` a v prípade porovnávania XML súborov pomocou programu
jexamxml. 

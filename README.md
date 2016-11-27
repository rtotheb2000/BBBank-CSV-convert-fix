# BBBank CSV convert/fix

Downloadable CSV (comma seperated values) [Wiki](https://en.wikipedia.org/wiki/Comma-separated_values) that are provided by the online banking system of the BBBank eG have the following basic structure

    "BBBank eG"
    
    "Umsatzanzeige"
    
    "BLZ:";"12345678";;"Datum:";"10.01.2017"
    "Konto:";"2656744";;"Uhrzeit:";"10:37:52"
    "Abfrage von:";"Max Mustermann";;"Kontoinhaber:";"Max Mustermann"
    
    "Zeitraum:";"Alle Umsätze";"von:";;"bis:";
    "Betrag in EUR:";;"von:";" ";"bis:";" "
    "Sortiert nach:";"Buchungstag";"absteigend"
    
    "Buchungstag";"Valuta";"Auftraggeber/Zahlungsempfänger";"Empfänger/Zahlungspflichtiger";"Konto-    Nr.";"IBAN";"BLZ";"BIC";"Vorgang/Verwendungszweck";"Kundenreferenz";"Währung";"Umsatz";" "
    "09.01.2017";"09.01.2017";"Max Mustermann";"Max Mustermann";;;;;"EURO-UEBERWEISUNG
    Übertrag TAN:123456 IBAN: D
    E12345678910111213141 BIC:
    ABCDEFGHIJK";;"EUR";"1.000,00";"S"
    "09.01.2017";"09.01.2017";"Mustermann Max";"Irgendeine Institution";;;;;"Verwendungszweck 1
    Verwendungszweck 2
    IBAN: DE123456789101112131
    41 BIC: ABCDEFGHIJK";;"EUR";"1.000,00";"H"
    
    "01.01.2017";;;;;;;;;"Anfangssaldo";"EUR";"0,00";"H"
    "09.01.2017";;;;;;;;;"Endsaldo";"EUR";"0,00";"H"

This form makes the original file unsuitable for import with e.g. `pandas` (but also with `excel` considering the unncessary linebreaks), which led me to write this little script.

## What it does...

This python script does essentially three things:
- it removes the header starting with `BBBank eG` and ending with `"Sortiert nach:";"Buchungstag";"absteigend"\n` by looking for the first relevant line containing `"Buchungstag";"Valuta";`
- it also removes the tail of the file containing `\n..."Anfangssaldo"...\n..."Endsaldo"\n`
- it finally removes linebreaks for lines that are not properly ended with either `"S"` or `"H"` and adds a blankspace instead

The result looks like this

    "Buchungstag";"Valuta";"Auftraggeber/Zahlungsempfänger";"Empfänger/Zahlungspflichtiger";"Konto-Nr.";"IBAN";"BLZ";"BIC";"Vorgang/Verwendungszweck";"Kundenreferenz";"Währung";"Umsatz";" "
    "09.01.2017";"09.01.2017";"Max Mustermann";"Max Mustermann";;;;;"EURO-UEBERWEISUNG Übertrag TAN:123456 IBAN: D E12345678910111213141 BIC: ABCDEFGHIJK";;"EUR";"1.000,00";"S" 
    "09.01.2017";"09.01.2017";"Mustermann Max";"Irgendeine Institution";;;;;"Verwendungszweck 1 Verwendungszweck 2 IBAN: DE123456789101112131 41 BIC: DEUTDEDB110";;"EUR";"1.000,00";"H" 

In addition to the above described conversion of the content of the file, the initial encoding of the file is evaluated (I found the original files to be encoded in `windows-1252` [Wiki](https://en.wikipedia.org/wiki/Windows-1252)) and the converted file will be formatted using `utf-8` [Wiki](https://en.wikipedia.org/wiki/UTF-8).

## How to use...

This script has been tested using `Ubuntu` and `python3`. For now I will not try to make it compatible with `python2.7`, but it probably takes little effort to do so.

Make sure you installed all the required python modules that are listed in `requirements.txt`.

- put script and downloaded csv files in the same folder
- open terminal at that folder and run `python3 BBBankCSV.py Umsaetze_DE12345678910111213141_2017.01.02.csv` to convert a single file
- you can also pass multiple files like this `python3 BBBankCSV.py Umsaetze_DE12345678910111213141_2017.01.02_1.csv Umsaetze_DE12345678910111213141_2017.01.02_1.csv`
- if you want to convert all csv files in this folder, you can run `python3 BBBankCSV.py Umsaetze_\*.csv` (make sure in this case to have no previously fixed files in the folder)

The input files will not be changed and new files will be created by the scheme `initialfilename_fixed.csv` in the same folder.

## Known issues
- several "Verwendungszwecke" that are seperated with a linebreak initially always will be seperated by a blankspace afterwards. This leads to IBAN numbers that are seperated initially by a linebreak to still be seperated in the converted file by a blankspace.

If you find additional issues with this script, please feel free to contribute.

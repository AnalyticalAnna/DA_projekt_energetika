import glob
import re

# Vyhledej všechny CSV soubory ve složce "data"
csv_files = glob.glob('data/*.csv')

# Spoj CSV soubory do jednoho souboru 'combined_load.csv'
combined_file = 'combined_load.csv'
with open(combined_file, 'w', encoding='utf-8') as outfile:
    header_written = False
    for file in csv_files:
        with open(file, 'r', encoding='utf-8') as infile:
            # Čtení prvního řádku (záhlaví)
            header = infile.readline()
            
            # Příklad header
            # "Time (UTC)","Day-ahead Total Load Forecast [MW] - Albania (AL)","Actual Total Load [MW] - Albania (AL)"
            # Získání kódu země z hlavičky pomocí regulárního výrazu
        
            match = re.search(r'Actual Total Load \[MW\] - .*?\((.*?)\)', header)
            if match:
                country_code = match.group(1)
            else:
                country_code = 'UNKNOWN'
            
            # Odstranění názvu státu z hlavičky
            header = re.sub(r' - [^)]*\)', '', header)

             # Zápis záhlaví pouze jednou (z prvního souboru)
            if not header_written:
                outfile.write(header.strip() + ',"country_code"\n')
                header_written = True
            
            # Čtení zbytku souboru a přidání kódu země do každého řádku
            for line in infile:
                outfile.write(line.strip() + f',"{country_code}"\n')
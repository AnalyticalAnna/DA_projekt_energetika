
import os
import requests
import urllib.parse
from bs4 import BeautifulSoup

# řešení problému s příliš headers
# HTTPException('got more than 100 headers')
import http.client
http.client._MAXHEADERS = 1000

# získání názvů zemí a jejich area codes ze zemí na ENTSOE
r = requests.get(
    "https://transparency.entsoe.eu/generation/r2/actualGenerationPerProductionType/show?name=&defaultValue=false&viewType=TABLE&areaType=CTY"
)
bs = BeautifulSoup(r.content, "html.parser")

countryCheckboxes = bs.select(
    "#dv-market-areas-content .dv-filter-hierarchic-wrapper > .dv-filter-checkbox"
)

# příklad názvu země a kódu: [("Czech Republic", "CTY|10YCZ-CEPS-----N")]
countryToAreaCode = []
for checkbox in countryCheckboxes:
    value = checkbox.find("input")["value"]
    areaCode = value.replace("|SINGLE", "")
    country = (checkbox.text.strip(), areaCode)
    countryToAreaCode.append(country)

# zde je možné natvrdo nastavit jednu zemi pro ladění kódu, aby to nezahlcovalo server
#countryToAreaCode = [("Czech Republic", "CTY|10YCZ-CEPS-----N")]

for year in range(2015, 2024):
    for countryName, areaCode in countryToAreaCode:
        print(f"Downloading data for {countryName} ({areaCode})")
        # Download link for
        # 'https://transparency.entsoe.eu/generation/r2/actualGenerationPerProductionType/export?name=&defaultValue=false&viewType=TABLE&areaType=CTY&atch=true&datepicker-day-offset-select-dv-date-from_input=D&dateTime.dateTime=06.10.2015+00%3A00%7CCET%7CDAYTIMERANGE&dateTime.endDateTime=06.10.2015+00%3A00%7CCET%7CDAYTIMERANGE&area.values=CTY%7C10Y1001A1001A83F!CTY%7C10Y1001A1001A83F&productionType.values=B01&productionType.values=B25&productionType.values=B02&productionType.values=B03&productionType.values=B04&productionType.values=B05&productionType.values=B06&productionType.values=B07&productionType.values=B08&productionType.values=B09&productionType.values=B10&productionType.values=B11&productionType.values=B12&productionType.values=B13&productionType.values=B14&productionType.values=B20&productionType.values=B15&productionType.values=B16&productionType.values=B17&productionType.values=B18&productionType.values=B19&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC%2B1)+%2F+CEST+(UTC%2B2)&dataItem=ALL&timeRange=YEAR&exportType=CSV',

        areaCodeUriEncoded = urllib.parse.quote(areaCode)

        # Doplň své hodnoty cookies po přihlášení (z developer tools)
        cookies = {
            "SESSION":"YTRiYWVhZjgtZjE1MS00YmM4LTk1YWUtMzk1ZGJlNGM0YTQ2", 
            "JSESSIONID": "9E3A472B03DB8DCAA35E56593BB799CB"
            }

        #Moje url
        url = f"https://transparency.entsoe.eu/load-domain/r2/totalLoadR2/export?name=&defaultValue=false&viewType=TABLE&areaType=CTY&atch=false&dateTime.dateTime=01.01.{year}+00%3A00%7CUTC%7CDAY&biddingZone.values={areaCodeUriEncoded}!{areaCodeUriEncoded}&dateTime.timezone=UTC&dateTime.timezone_input=UTC&dataItem=ALL&timeRange=YEAR&exportType=CSV" 

        # například
        # URL="https://transparency.entsoe.eu/load-domain/r2/totalLoadR2/export?name=&defaultValue=false&viewType=TABLE&areaType=CTY&atch=false&dateTime.dateTime=01.01.2014+00%3A00%7CUTC%7CDAY&biddingZone.values=CTY%7C10YCZ-CEPS-----N!CTY%7C10YCZ-CEPS-----N-----N&dateTime.timezone=UTC&dateTime.timezone_input=UTC&dataItem=ALL&timeRange=YEAR&exportType=CSV"

        # web FUNGUJE!
        # url = "https://transparency.entsoe.eu/load-domain/r2/totalLoadR2/export?name=&defaultValue=false&viewType=TABLE&areaType=CTY&atch=false&dateTime.dateTime=12.11.2024+00%3A00%7CUTC%7CDAY&biddingZone.values=CTY%7C10YCZ-CEPS-----N!CTY%7C10YCZ-CEPS-----N&dateTime.timezone=UTC&dateTime.timezone_input=UTC&dataItem=ALL&timeRange=YEAR&exportType=CSV"

        # url="https://transparency.entsoe.eu/load-domain/r2/totalLoadR2/export?name=&defaultValue=false&viewType=TABLE&areaType=CTY&atch=false&dateTime.dateTime=01.01.2014+00%3A00%7CUTC%7CDAY&biddingZone.values=CTY%7C10YCZ-CEPS-----N!CTY%7C10YCZ-CEPS-----N&dateTime.timezone=UTC&dateTime.timezone_input=UTC&dataItem=ALL&timeRange=YEAR&exportType=CSV"

        response = requests.get(url, cookies=cookies)

        print("Downloading data for", countryName)
        #kontrolní vypsání url každého státu - jestli se správně vyplňuje url adresa
        print(url)
        r = requests.get(url, cookies=cookies, allow_redirects=True)
        
        #uložení souboru do složky "data" jako název státu a rok
        filename = f"./data/{countryName} {year}.csv"
        os.makedirs(os.path.dirname(filename), exist_ok=True)        
        open(filename, "wb").write(r.content)
        print("Saved to", os.path.abspath(filename))


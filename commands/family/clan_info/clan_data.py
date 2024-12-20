import json

# Funktion zum Laden der Clan-Informationen aus der JSON-Datei
def load_clan_info(clan_tag):
    try:
        with open(f"datenbank/clan/{clan_tag}.json", "r", encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return None

# Clan-Auswahl für den initialen Parameter
clans = {
    "~DeathZone~": "2JLQVYQ8",
    "DZ⚜Academy": "2P82CQQJL",
    "DZ⚜Immortality": "2P28YJ9L2",
    "DZ⚜Utopia": "28VYRC2R8",
    "DZ⚜Afterlife": "22UYU90JL",
    "DZ⚜FighterZ": "2LRPVRCJ0",
    "-DeathZone-": "2LP29CJC9"
}
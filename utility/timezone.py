from datetime import datetime
import pytz

def convert_to_german_timezone(utc_time):
    """
    Konvertiert eine UTC-Zeit in die deutsche Zeitzone (MEZ/MESZ).
    
    :param utc_time: datetime - Die UTC-Zeit, die konvertiert werden soll
    :return: datetime - Die Zeit in der deutschen Zeitzone
    """
    german_timezone = pytz.timezone('Europe/Berlin')
    return utc_time.astimezone(german_timezone)

# Beispiel für die Verwendung der Funktion
if __name__ == "__main__":
    utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
    german_time = convert_to_german_timezone(utc_time)
    print(f"UTC Time: {utc_time}")
    print(f"German Time: {german_time}")
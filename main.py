from icalendar import Calendar, Event

def add_event(name: str) -> bool:
    txt = "BEGIN:VEVENT"

    txt += "\nEND:VEVENT"
    return True


def add_task(name: str) -> bool:
    txt = "BEGIN:VEVENT"

    txt += "\nEND:VEVENT"
    return True

def main():
    print(f"Hello World!")
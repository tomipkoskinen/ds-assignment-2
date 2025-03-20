import xmlrpc.client
import datetime

s = xmlrpc.client.ServerProxy('http://localhost:8000')
print(s.health())

# Print list of available methods
print(s.system.listMethods())
print()

def menu() -> int:
    print("1) Add note")
    print("2) Get topic")
    print("3) Append Wikipedia article to topic")
    print("0) Exit")
    user_input = input("Choose option: ")
    try:
        menu_selection = int(user_input)
    except ValueError:
        menu_selection = -1
    return menu_selection

def main():
    menu_selection = None

    while menu_selection != 0:
        menu_selection = menu()

        if menu_selection == 1:
            topic = input("Topic: ")
            name = input("Name: ")
            text = input("Text: ")
            timestamp_input = input("Timestamp (MM/DD/YY - HH:MM:SS) or empty for current time: ")
            if timestamp_input:
                try:
                    datetime.datetime.strptime(timestamp_input, "%m/%d/%y - %H:%M:%S")
                    timestamp = timestamp_input
                except ValueError:
                    print("Invalid timestamp")
                    continue
            else:
                timestamp = datetime.datetime.now().strftime("%m/%d/%y - %H:%M:%S")
            if s.add_note(topic, name, text, timestamp):
                print("note added")
            else:
                print("error adding note")
        elif menu_selection == 2:
            topic = input("Topic: ")
            notes = s.get_notes(topic)
            if notes:
                for note in notes:
                    print()
                    print(note["name"])
                    print(note["text"])
                    print(note["timestamp"])
            else:
                print("Topic is empty")
        elif menu_selection == 3:
            query = input("Search query: ")
            result = s.search_wikipedia(query)
            if result != None:
                print(result)
                topic = input("Topic to add to: ")
                name = "Wikipedia " + query
                text = result
                timestamp = datetime.datetime.now().strftime("%m/%d/%y - %H:%M:%S")
                if s.add_note(topic, name, text, timestamp):
                    print("note added")
                else:
                    print("error adding note")
            else:
                print("No article found")
        elif menu_selection == 0:
            break
        else:
            print("Invalid option")
        print()
    return None

main()

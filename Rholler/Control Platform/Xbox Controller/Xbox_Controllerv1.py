import inputs

def get_gamepad():
    try:
        while True:
            events = inputs.get_gamepad()
            for event in events:
                process_event(event)
    except KeyboardInterrupt:
        print("Program exited")

def process_event(event):
    if event.ev_type == "Key":
        print(f"{event.code}: {event.state}")
    elif event.ev_type == "Absolute":
        print(f"{event.code}: {event.state}")

if __name__ == "__main__":
    get_gamepad()

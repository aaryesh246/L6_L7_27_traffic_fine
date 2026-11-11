def parse_ticket_id(ticket_id):
    """Parse IDs in PREFIX-YEAR-SERIAL format.

    Returns (uppercase_prefix, year, serial), or None for invalid input.
    """
    if not isinstance(ticket_id, str):
        return None

    parts = ticket_id.strip().split("-")
    if len(parts) != 3:
        return None

    prefix, year_text, serial_text = (part.strip() for part in parts)

    if not prefix or not prefix.isalnum():
        return None
    if not year_text.isdigit() or len(year_text) != 4:
        return None
    if not serial_text.isdigit():
        return None

    return prefix.upper(), int(year_text), int(serial_text)


def total_fines(amounts_csv):
    """Return the sum of comma-separated non-negative fines, capped at 10000.

    Returns None for invalid input.
    """
    if not isinstance(amounts_csv, str):
        return None

    raw_amounts = amounts_csv.strip()
    if not raw_amounts:
        return None

    tokens = raw_amounts.split(",")
    amounts = []

    for token in tokens:
        token = token.strip()
        if not token or not token.isdigit():
            return None
        amounts.append(int(token))

    return min(sum(amounts), 10000)


def speed_excess(reading):
    """Calculate integer percentage above the speed limit.

    Input format: speed/limit. Returns None for invalid input or a
    non-positive speed limit.
    """
    if not isinstance(reading, str):
        return None

    parts = reading.strip().split("/")
    if len(parts) != 2:
        return None

    speed_text, limit_text = (part.strip() for part in parts)

    if not speed_text.isdigit() or not limit_text.isdigit():
        return None

    speed = int(speed_text)
    limit = int(limit_text)

    if limit <= 0:
        return None

    return (speed - limit) * 100 // limit


def main():
    print("==== Running parse_ticket_id ====")
    user_input = input("Enter a ticket ID (e.g. TF-2024-0456): ")
    result = parse_ticket_id(user_input)
    print("Ticket Prefix, Year and Serial:", result)

    print("\n==== Running total_fines ====")
    user_input = input("Enter fine amounts as CSV (e.g. 500,1200,300): ")
    result = total_fines(user_input)
    print("Total Fines:", result)

    print("\n==== Running speed_excess ====")
    user_input = input("Enter speed/limit (e.g. 72/60): ")
    result = speed_excess(user_input)
    print("Percent Over Limit:", result)


if __name__ == "__main__":
    main()

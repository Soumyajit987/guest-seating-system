def parse_file(file):

    guests = []

    data = file.read().decode()

    for line in data.splitlines():

        if line.startswith("#") or not line:
            continue

        row = line.split(",")

        guests.append({
            "name": row[0],
            "group": row[1],
            "vip": row[2] == "Yes",
            "friends": row[3].split("|") if row[3] else [],
            "avoid": row[4].split("|") if row[4] else []
        })

    return guests
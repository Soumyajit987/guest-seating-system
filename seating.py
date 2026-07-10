def generate_seating(guests, tables, capacity):
    seating = [[] for _ in range(tables)]
    remaining = [capacity] * tables
   
    guests.sort(key=lambda x: x["vip"], reverse=True)
    name_to_table = {}
   

    for guest in guests:

        placed = False

       

        for friend in guest["friends"]:
            if friend in name_to_table:
                table = name_to_table[friend]
                if remaining[table] > 0:
                    conflict = False
                    for person in seating[table]:
                        if person in guest["avoid"]:
                            conflict = True
                            break
                    if not conflict:
                        seating[table].append(guest["name"])
                        remaining[table] -= 1
                        name_to_table[guest["name"]] = table
                        placed = True
                        break

        if placed:
            continue

        best_table = -1
        best_score = -100000
        for table in range(tables):
            if remaining[table] == 0:
                continue

            score = 0

            if guest["vip"] and table == 0:
                score += 50

            for person in seating[table]:
                if person in guest["friends"]:
                    score += 10

            conflict = False

            for person in seating[table]:
                if person in guest["avoid"]:
                    conflict = True
                    score -= 100
            if conflict:
                continue
            
            score += remaining[table]
            if score > best_score:
                best_score = score
                best_table = table

        if best_table != -1:
            seating[best_table].append(guest["name"])
            remaining[best_table] -= 1
            name_to_table[guest["name"]] = best_table
    return seating
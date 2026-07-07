def generate_seating(guests, tables, capacity):

    seating = [[] for _ in range(tables)]

    index = 0

    for guest in guests:

        seating[index].append(guest["name"])

        if len(seating[index]) == capacity:
            index += 1

            if index >= tables:
                break

    return seating
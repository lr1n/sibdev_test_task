def process_csv(reader):
    """This function takes a csv reader and handle it with our needs

    Returns: a list with dicts
    """
    customers = set()
    data = dict()

    for el in reader:
        customers.add(el[0])

    for el in customers:
        data[el] = [0, set()]

    for el in reader:
        data[el[0]][0] += int(el[2])
        data[el[0]][1].add(el[1])

    sorted_data = {
        k: v for k, v in sorted(data.items(), key=lambda x: x[1], reverse=True)
    }

    gems = []
    data_5_items = []
    for k, v in sorted_data.items():
        data_5_items.append([k, v[0], v[1]])
        gems.extend(list(v[1]))
        if len(data_5_items) > 4:
            break

    for el in data_5_items:
        for gem in gems:
            if gem in el[2] and gems.count(gem) < 2:
                el[2].remove(gem)

    for el in data_5_items:
        el[2] = list(el[2])

    res_data = []
    for el in data_5_items:
        res_data.append({
            'username': el[0], 'spent_money': el[1], 'gems': el[2]
        })

    return res_data

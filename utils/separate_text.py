def separateText(text): 
    email = {}

    for line in text.strip().split("\n"): 
        key, value = line.split(":", 1)
        email[key.strip().lower()] = value.strip()

    return email
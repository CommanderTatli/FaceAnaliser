def categorise(categories, records, attr, field_name):
    new_records = []
    stats = {}
    for record in records:
        record[field_name] = "None"
        for c in categories:
            if record[attr] in c:
                record[field_name] = c[0]
                break
        new_records.append(record)
        if record[field_name] == "None":
            if record[attr] in stats.keys():
                stats[record[attr]] += 1
            else:
                stats[record[attr]] = 1

    print("--------------------------------")
    print("|Categories and their frequency|")
    print("--------------------------------")
    categorisation_stats = {}
    for c in categories+[["None"]]:
        categorisation_stats[c[0]] = 0
    for r in records:
        for c in categories+[["None"]]:
            if r[field_name] == c[0]:
                categorisation_stats[c[0]] += 1
                break
    for c in categories+[["None"]]:
        print(c[0], ":", categorisation_stats[c[0]])

    print("--------------------")
    print("|Classified as None|")
    print("--------------------")
    stats = {k: v for k, v in sorted(stats.items(), key=lambda item: item[1])}
    for key in stats.keys():
        print(key, ":", stats[key])
    return new_records

def write_records(records, file):
    with open(file, "w") as file:
        for record in records:
            line = ""
            for key in record.keys():
                line += key+":"+record[key]+";"
            line = line[:-1] + "\n"
            file.write(line)

def read_records(file):
    records = []
    with open(file, "r") as file:
        for line in file.readlines():
            record = {}
            for i in line.split(";")[:-2]:
                record[i.split(":")[0]] = i.split(":")[1]
            records.append(record)
    return records


categories = [
    ["Star", "TV", "Actor", "Actress", "Singer", "Film", "Comic", "Model", "Pornstar", "Naturalist", "Performance"],
    ["Music", "Musician", "Conductor", "Rapper", "Guitarist", "Country", "Drummer", "Jazz", "Bassist",
     "Pianist", "Violinist", "Cellist", "Violist", "DJ"],
    ["Arts", "Art", "Author", "Novelist", "Composer", "Poet", "Painter", "Playwright", "Philosopher",
     "Journalist", "Cartoonist", "Critic", "Songwriter", "Screenwriter", "Editor", "Sculptor", "Publisher",
     "Photographer", "Columnist", "Fashion", "Theater", "Cinematographer", "Artist", "Designer", "Choreographer",
     "Lexicographer", "Essayist", "Chef", "Magician", "Blogger", "Curator", "Theatre", "Musicologist", "Engraver"],
    ["Law", "Historian", "Attorney", "Judge", "Lawyer", "Legal"],
    ["Military"],
    ["Religion", "Pundit"],
    ["Business/politics", "Politician", "Royalty", "Diplomat", "Activist", "Socialite", "Businessman",
     "Business", "Head", "Aristocrat", "Government", "Political", "Anarchist", "Organist", "Lobbyist"],
    ["Sports", "Sportsman", "Sports", "Boxing",  "Dancer", "Wrestling", "Soccer", "Baseball", "Football",
     "Basketball", "Hockey", "Golf", "Tennis", "Swimmer", "Skier", "Fitness", "Cricket", "Skateboarder", "Bowling",
     "Jockey", "Diver", "Cyclist", "Racehorse", "Gymnastics", "Martial", "Track", "Auto", "Figure Skating"],
    ["Sciences", "Scientist", "Engineer", "Mathematician", "Doctor", "Chemist", "Architect", "Inventor", "Physicist",
     "Educator", "Astronomer", "Scholar", "Computer", "Biologist", "Electronic", "Psychologist", "Sociologist",
     "Economist", "Explorer", "Botanist", "Anthropologist", "Geologist", "Agriculturalist", "Linguist",
     "Psychiatrist", "Zoologist","Paleontologist", "Archaeologist"],
    ["Crime", "Criminal", "Terrorist", "Assassin", "Spy", "Daredevil", "Hacker"]
]
records = read_records("data.txt")
new_records = categorise(categories, records, "occupation", "occupation_category")
write_records(new_records, "processed.txt")
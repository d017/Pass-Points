from bs4 import BeautifulSoup
import requests as rq

bsu_link = "https://abit.bsu.by/formk1?id=32"
html_link = "src/site.html"

def get_facs(link):
    soup = BeautifulSoup(rq.get(link).text, "lxml")
    table = soup.find("table")
    rows = table.find_all("tr")
    facs = list(filter(lambda r: r.find("td", class_="fl"), rows))
    return list(map(lambda r: r.find("td").text, facs)), facs

def get_specs(link, fac):
    soup = BeautifulSoup(rq.get(link).text, "lxml")
    table = soup.find("table")
    rows = table.find_all("tr")
    fac_index = rows.index(fac)
    specs = list()
    for row in rows[fac_index+1:]:
        if row.find("td", class_="vl"):
            specs.append(row)
        else:
            if row.find("td", class_="fl"):
                break

    return list(map(lambda r: r.find("td", class_="vl").text, specs)), specs

def get(cell):
    if cell.text:
        return int(cell.text)
    else:
        return 0

def pass_points(spec):
    ranges = list()
    ranges.append("396+")
    points = 395
    while points > 120:
        ranges.append(f"{points-4}-{points}")
        points -= 5
    ranges.append("120-")

    cells = spec.find_all("td")
    spec_cell = spec.find("td", class_="vl")
    cells = cells[cells.index(spec_cell):]

    places_count = get(cells[1])

    without_comp = get(cells[5]) + get(cells[6]) + get(cells[7])
    without_comp = min(without_comp, int(0.8 * places_count))
    places_left = places_count - without_comp

    if get(cells[8]) < places_left:
        return "0"

    index = 9
    while places_left > 0:
        places_left -= get(cells[index])
        if places_left <= 0:
            return ranges[index-9]
        index += 1

    raise ValueError("-")

bio_specs = get_specs(bsu_link, get_facs(bsu_link)[1][0])
print(pass_points(bio_specs[1][0]))

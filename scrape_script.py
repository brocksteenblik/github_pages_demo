import pandas as pd
import requests
from bs4 import BeautifulSoup

r = requests.get("https://dustloop.com/w/GGST")

soup = BeautifulSoup(r.text)

raw_links = soup.find_all("a")

filtered_raw_links = raw_links[49:83]

links = [link["href"] for link in filtered_raw_links]

final_links = ["https://dustloop.com" + link for link in links]

r = requests.get(final_links[0])
soup = BeautifulSoup(r.text)

data_dict = {
    "name": [],
    "5P": [],
    "5K": [],
    "c.S": [],
    "f.S": [],
    "5H": [],
    "5D": [],
    "5[D]": [],
    "2P": [],
    "2K": [],
    "2S": [],
    "2H": [],
    "2D": [],
    "6P": []
}

def safe_scrape(soup, tag, class_name):
    try:
        return soup.find(tag, {"class": class_name}).text.strip()
    except:
        return None

def safe_scrape_moves(soup):
    try:
        if safe_scrape(soup, "div", "t-infobox-title") != "A.B.A":
            return soup.find_all("div", {"class": "frameDataGridRow colCount-7"})
        else:
            return soup.find_all("div", {"class": "frameDataGridRow colCount-8"}) #ADJUST A.B.A LATER
            # I need to adjust characters with colCount-8 information, likely on a character-by-character basis.
    except:
        return None

def extract_move_data(moves, index, name):
    """
    Generally, indexes -> move names are:
    0 = 5P   1 = 5K   2 = c.S   3 = f.S   4 = 5H   
    5 = 2P   6 = 2K   7 = 2S    8 = 2H    9 = 2D  10 = 6P
    """
    problem_strive_characters = ["Nagoriyuki", "A.B.A", "Happy Chaos","Faust", "Lucy", "Bridget", "Elphelt Valentine"]
    if name in problem_strive_characters:
        return address_Strive_problem_characters(moves, index, name)
    elif index == "5D":
        return extract_8col_data(0)
    elif index == "5[D]":
        return extract_8col_data(1)
    else:
        return extract_7col_data(moves, index)
        
def extract_7col_data(moves, index):
    move = moves[index].contents
    move = [attribute.text for attribute in move]
    relevant_info = move[1:6]
    return relevant_info

def address_Strive_problem_characters(moves, index, name):
    # There are some issues with A.B.A and Nagoriyuki (8 row columns), Happy Chaos (No H attacks), and Faust, Lucy and Bridget (unique followups)
        if name == "Nagoriyuki":
            return address_Nagoriyuki(moves, index)
        elif name == "A.B.A":
            return address_ABA(moves, index)
        elif name == "Happy Chaos":
            return address_Happy_Chaos(moves, index)
        elif name == "Faust":
            return address_Faust(moves, index)
        elif name == "Lucy":
            return address_Lucy(moves, index)
        elif name == "Bridget":
            return address_Bridget(moves, index)
        elif name == "Elphelt Valentine":
            return address_Elphelt(moves, index)
        else:
            return index

def address_Nagoriyuki(moves, index):
    if index == "5D":
        return extract_8col_data(16)
    elif index == "5[D]":
        return extract_8col_data(17)
    elif index == 0 or index == 1 or index == 2:
        return extract_7col_data(moves, index)
    elif index == 3:
        return extract_8col_data(0)
    elif index == 4:
        return extract_8col_data(12)
    elif index == 5 or index == 6:
        return extract_7col_data(moves, index - 2)
    elif index == 7:
        return extract_8col_data(18)
    elif index == 8:
        return extract_8col_data(22)
    elif index == 9 or index == 10:
        return extract_7col_data(moves, index - 4)

def address_ABA(moves, index):
    if index == "5D":
        return extract_8col_data(10)
    elif index == "5[D]":
        return extract_8col_data(11)
    elif index == 0:
        return extract_8col_data(0)
    elif index > 0 and index <= 4:
        return extract_8col_data(index * 2)
    elif index >= 5 and index <= 10:
        return extract_8col_data((index + 1) * 2)

def address_Happy_Chaos(moves, index):
    if index == "5D":
        return extract_8col_data(0)
    elif index == "5[D]":
        return extract_8col_data(1)
    elif index >= 0 and index <= 3:
        return extract_7col_data(moves, index)
    elif index == 4:
        return None
    elif index >= 5 and index <= 7:
        return extract_7col_data(moves, index - 1)
    elif index == 8:
        return None
    elif index == 9 or index == 10:
        return extract_7col_data(moves, index - 2)

def address_Faust(moves, index):
    if index == "5D":
        return extract_8col_data(2)
    elif index == "5[D]":
        return extract_8col_data(3)
    elif index >= 0 and index <= 3:
        return extract_7col_data(moves, index)
    elif index == 4:
        return extract_8col_data(0)
    elif index >= 5 and index <= 10:
        return extract_7col_data(moves, index - 1)

def address_Lucy(moves, index):
    if index == "5D":
        return extract_8col_data(0)
    elif index == "5[D]":
        return extract_8col_data(1)
    elif index >= 0 and index <= 3:
        return extract_7col_data(moves, index)
    elif index >= 4 and index <= 7:
        return extract_7col_data(moves, index + 1)
    elif index >= 8 and index <= 10:
        return extract_7col_data(moves, index + 2)

def address_Bridget(moves, index):
    if index == "5D":
        return extract_8col_data(0)
    elif index == "5[D]":
        return extract_8col_data(1)
    elif index >= 0 and index <= 3:
        return extract_7col_data(moves, index)
    elif index == 4:
        return extract_7col_data(moves, index + 1)
    elif index >= 5 and index <= 10:
        return extract_7col_data(moves, index + 2)
    
def address_Elphelt(moves, index):
    if index == "5D":
        return extract_8col_data(0)
    elif index == "5[D]":
        return extract_8col_data(1)
    elif index >= 0 and index <= 4:
        return extract_7col_data(moves, index)
    elif index >= 5 and index <= 10:
        return extract_7col_data(moves, index + 1)

def extract_8col_data(index):
    moves = soup.find_all("div", {"class": "frameDataGridRow colCount-8"})
    move = moves[index].contents
    move = [attribute.text for attribute in move]
    relevant_info = move[2:7]
    return relevant_info

for link in final_links:
    directory = requests.get(link)
    soup = BeautifulSoup(directory.text)
    moves = safe_scrape_moves(soup)

    name = safe_scrape(soup, "div", "t-infobox-title")
    fiveP = extract_move_data(moves, 0, name)
    fiveK = extract_move_data(moves, 1, name)
    cS = extract_move_data(moves, 2, name)
    fS = extract_move_data(moves, 3, name)
    fiveH = extract_move_data(moves, 4, name)
    fiveD = extract_move_data(moves, "5D", name)
    chargeD = extract_move_data(moves, "5[D]", name)
    twoP = extract_move_data(moves, 5, name)
    twoK = extract_move_data(moves, 6, name)
    twoS = extract_move_data(moves, 7, name)
    twoH = extract_move_data(moves, 8, name)
    twoD = extract_move_data(moves, 9, name)
    sixP = extract_move_data(moves, 10, name)
    
    data_dict['name'].append(name)
    data_dict['5P'].append(fiveP)
    data_dict['5K'].append(fiveK)
    data_dict['c.S'].append(cS)
    data_dict['f.S'].append(fS)
    data_dict['5H'].append(fiveH)
    data_dict['5D'].append(fiveD)
    data_dict['5[D]'].append(chargeD)
    data_dict['2P'].append(twoP)
    data_dict['2K'].append(twoK)
    data_dict['2S'].append(twoS)
    data_dict['2H'].append(twoH)
    data_dict['2D'].append(twoD)
    data_dict['6P'].append(sixP)

    StriveDF = pd.DataFrame(data_dict)

r = requests.get("https://dustloop.com/w/GGXRD-R2")

soup = BeautifulSoup(r.text)
raw_links = soup.find_all("a")
filtered_raw_links = raw_links[85:110]
links = [link["href"] for link in filtered_raw_links]
final_links = ["https://dustloop.com" + link for link in links]

def create_pos_dict(soup):
    data = soup.find_all("h3")
    pos_dict = {
    "5P": [],
    "5K": [],
    "c.S": [],
    "f.S": [],
    "5H": [],
    "5D": [],
    "2P": [],
    "2K": [],
    "2S": [],
    "2H": [],
    "2D": [],
    "6P": [],
    "6K": [],
    "6S": [],
    "6H": []
    }
    for i in range(5):
        if "colorful-text" not in str(data[0]):
            data.pop(0)
    for i in range(len(data)):
        for move in pos_dict:
            if f"id=\"{move}\"" in str(data[i]):
                pos_dict[move].append(i)
                break
    return pos_dict

data_dict = {
    "name": [],
    "5P": [],
    "5K": [],
    "c.S": [],
    "f.S": [],
    "5H": [],
    "5D": [],
    "2P": [],
    "2K": [],
    "2S": [],
    "2H": [],
    "2D": [],
    "6P": []
}

def safe_scrape(soup, tag, class_name):
    try:
        return soup.find(tag, {"class": class_name}).text.strip()
    except:
        return None

def xrd_safe_scrape_moves(soup):
    try:
        if safe_scrape(soup, "div", "t-infobox-title") != "A.B.A":
            return soup.find_all("div", {"class": "frameDataGridRow colCount-7"})
        else:
            return soup.find_all("div", {"class": "frameDataGridRow colCount-8"}) #ADJUST A.B.A LATER
            # I need to adjust characters with colCount-8 information, likely on a character-by-character basis.
    except:
        return None

def xrd_extract_move_data(moves, index, name):
    if index != []:
        index = index[0]
        problem_xrd_characters = ["Answer", "Bedman", "Dizzy", "Elphelt Valentine", "Faust", "Jack-O", "Leo Whitefang", "Sol Badguy"]
        if name in problem_xrd_characters:
            return address_xrd_problem_characters(moves, index, name)    
        else:
            return xrd_extract_7col_data(moves, index)
    else:
        if name == "Bedman":
            return extract_8col_data(2)
        elif name == "Jack-O":
            return extract_7col_data(moves, 14)
        else:
            return None
        
def xrd_extract_7col_data(moves, index):
    move = moves[index].contents
    move = [attribute.text for attribute in move]
    relevant_info = move[1:6]
    if relevant_info[4] == "±0": 
        relevant_info[4] = "0"
    return relevant_info

def xrd_extract_8col_data(index):
    moves = soup.find_all("div", {"class": "frameDataGridRow colCount-8"})
    move = moves[index].contents
    move = [attribute.text for attribute in move]
    relevant_info = move[2:7]
    if relevant_info[4] == "±0":
        relevant_info[4] = "0"
    return relevant_info

def address_xrd_problem_characters(moves, index, name):
    if name == "Answer":
        return address_Answer(moves, index)
    elif name == "Bedman":
        return address_Bedman(moves, index)
    elif name == "Dizzy":
        return address_Dizzy(moves, index) 
    elif name == "Elphelt Valentine":
        return address_Elphelt_xrd(moves, index)  
    elif name == "Faust":
        return address_Faust_xrd(moves, index)
    elif name == "Jack-O":
        return address_JackO(moves, index)
    elif name == "Leo Whitefang":
        return address_Leo(moves, index)
    elif name == "Sol Badguy":
        return address_Sol(moves, index)
    else:
        return "hi"

def address_Answer(moves, index):
    if index < 9:
        return xrd_extract_7col_data(moves, index)
    elif index >= 9:
        return xrd_extract_7col_data(moves, index - 1)

def address_Bedman(moves, index):
    if index < 8:
        return xrd_extract_7col_data(moves, index)
    elif index == 12:
        return xrd_extract_7col_data(moves, index - 2)
    elif index >= 8:
        return xrd_extract_7col_data(moves, index - 1)

def address_Dizzy(moves, index):
    if index < 9:
        return xrd_extract_7col_data(moves, index)
    elif index >= 9:
        return xrd_extract_7col_data(moves, index - 1)

def address_Elphelt_xrd(moves, index):
    if index <= 3:
        return xrd_extract_7col_data(moves, index)
    elif index == 4:
        return xrd_extract_8col_data(0)
    elif index > 4:
        return xrd_extract_7col_data(moves, index - 1)

def address_Faust_xrd(moves, index):
    if index <= 4:
        return xrd_extract_7col_data(moves, index)
    elif index == 5:
        return xrd_extract_8col_data(0)
    elif index > 5:
        return xrd_extract_7col_data(moves, index - 1)

def address_JackO(moves, index):
    if index < 12:
        return xrd_extract_7col_data(moves, index)
    elif index >= 12:
        return xrd_extract_7col_data(moves, index - 2)

def address_Leo(moves, index):
    if index <= 2:
        return xrd_extract_7col_data(moves, index)
    elif index == 3 or index == 4:
        return xrd_extract_8col_data(2*index - 6)
    elif index >= 5:
        return xrd_extract_7col_data(moves, index - 2)

def address_Sol(moves, index):
    if index == 5:
        return xrd_extract_7col_data(moves, 0)
    elif index < 5:
        return xrd_extract_8col_data(2 * index)
    elif index > 5:
        return xrd_extract_8col_data(2 * (index - 1))

for link in final_links:
    directory = requests.get(link)
    soup = BeautifulSoup(directory.text)
    pos_dict = create_pos_dict(soup)
    moves = safe_scrape_moves(soup)

    name = safe_scrape(soup, "div", "t-infobox-title")
    fiveP = xrd_extract_move_data(moves, pos_dict["5P"], name)
    fiveK = xrd_extract_move_data(moves, pos_dict["5K"], name)
    cS = xrd_extract_move_data(moves, pos_dict["c.S"], name)
    fS = xrd_extract_move_data(moves, pos_dict["f.S"], name)
    fiveH = xrd_extract_move_data(moves, pos_dict["5H"], name)
    fiveD = xrd_extract_move_data(moves, pos_dict["5D"], name)
    twoP = xrd_extract_move_data(moves, pos_dict["2P"], name)
    twoK = xrd_extract_move_data(moves, pos_dict["2K"], name)
    twoS = xrd_extract_move_data(moves, pos_dict["2S"], name)
    twoH = xrd_extract_move_data(moves, pos_dict["2H"], name)
    twoD = xrd_extract_move_data(moves, pos_dict["2D"], name)
    sixP = xrd_extract_move_data(moves, pos_dict["6P"], name)
    
    data_dict['name'].append(name)
    data_dict['5P'].append(fiveP)
    data_dict['5K'].append(fiveK)
    data_dict['c.S'].append(cS)
    data_dict['f.S'].append(fS)
    data_dict['5H'].append(fiveH)
    data_dict['5D'].append(fiveD)
    data_dict['2P'].append(twoP)
    data_dict['2K'].append(twoK)
    data_dict['2S'].append(twoS)
    data_dict['2H'].append(twoH)
    data_dict['2D'].append(twoD)
    data_dict['6P'].append(sixP)

    XrdDF = pd.DataFrame(data_dict)

StriveDF.to_csv("data/Strive_Data", index=False)
XrdDF.to_csv("data/Xrd_Data", index=False)
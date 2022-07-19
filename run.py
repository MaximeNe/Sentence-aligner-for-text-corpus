###############################################################################
#   Author: Maxime NEMO                                                       #
#   Date: 2022/07/19                                                          #
#   Licence: GNU LESSER GENERAL PUBLIC LICENSE                                #
###############################################################################

from warnings import catch_warnings
import xlrd
import xlwt
from os import system

FR_FILENAME = "fr.txt"
NB_FILENAME = "nb.txt"


def read_txt(filename):
    with open(filename) as f:
        return [e.strip()for e in f.readlines()]


try:
    data_fr = read_txt(FR_FILENAME)
    print("found FR source file")
except FileNotFoundError:
    print("File not found: {}".format(FR_FILENAME))
    exit(1)
try:
    data_nb = read_txt(NB_FILENAME)
    print("found NB target file")
except FileNotFoundError:
    print("File not found: {}".format(NB_FILENAME))
    exit(1)

words_fr = set()
for e in data_fr:
    for word in e.split():
        words_fr.add(word)

words_nb = set()
for e in data_nb:
    for word in e.split():
        words_nb.add(word)

words_fr_nb = words_fr.intersection(words_nb)

try:
    workbook = xlrd.open_workbook(filename="Appendix NB.xlsx")
except FileNotFoundError:
    print("File not found: Appendix NB.xlsx")
    exit(1)

worksheet = workbook.sheet_by_index(0)

nb_dict = {}
for i in range(worksheet.nrows):
    # Les mots qui sont dans la colonne 1 sont soit uniques, soit séparés par '/'. Ensuite, si ils peuvent être au pluriel, "(s)" est présent.
    if ((worksheet.cell_value(i, 0) == "") or (worksheet.cell_value(i, 1) == "") or (worksheet.cell_value(i, 2) == "")):
        continue
        ...
    else:
        fr_words = worksheet.cell_value(i, 0).split("/")
        if len(fr_words) == 1:
            # Pas de féminin
            nb_dict[fr_words[0].replace(
                "(s)", "s")] = worksheet.cell_value(i, 2)
            nb_dict[fr_words[0].replace(
                "(s)", "")] = worksheet.cell_value(i, 1)
        else:
            # Féminin existe
            nb_dict[fr_words[0].replace(
                "(s)", "") + "s"] = worksheet.cell_value(i, 2)
            nb_dict[fr_words[0].replace(
                "(s)", "")] = worksheet.cell_value(i, 1)
            nb_dict[fr_words[1].replace(
                "(s)", "s")] = worksheet.cell_value(i, 2)
            nb_dict[fr_words[1].replace(
                "(s)", "")] = worksheet.cell_value(i, 1)


with open("dict.stem.dic", "w") as f:
    for e in words_fr_nb:
        f.write(e + " @ " + e + "\n")
    for e in nb_dict:
        f.write(nb_dict[e] + " @ " + e + "\n")

print("dictionary built.")

system("hunalign/src/hunalign/hunalign dict.stem.dic fr.txt nb.txt -text -realign > alligned.txt")


f = open("alligned.txt")
data = f.readlines()


fr, nb = [], []
for line in data:
    fr_sent, nb_sent = line.split("\t")[:2]
    if fr_sent == '':
        for sent in nb_sent.split(" ~~~ "):
            nb.append(sent)
            fr.append("")
    elif nb_sent == '':
        for sent in fr_sent.split(" ~~~ "):
            fr.append(sent)
            nb.append("")
    else:

        fr.append(fr_sent)
        nb.append(nb_sent)


badBG = xlwt.Pattern()
badBG.pattern = badBG.SOLID_PATTERN
badBG.pattern_fore_colour = 3

badFontStyle = xlwt.XFStyle()
badFontStyle.pattern = badBG

workbook = xlwt.Workbook()
sheet = workbook.add_sheet('page 0')

i = 0
for j in range(len(fr)):
    if '~~~' not in fr[j] and '~~~' not in nb[j]:
        sheet.write(i, 0, fr[j])
        sheet.write(i, 1, nb[j])
        i += 1

    elif '~~~' not in fr[j] and '~~~' in nb[j]:
        # On doit split nb[i]
        sub_sent = nb[j].split(" ~~~ ")

        # On va dire que fr[i] correspond a la plus longue phrase de sub_sent
        longest_sent = max(sub_sent, key=len)

        for s in sub_sent:
            if s == longest_sent:
                sheet.write(i, 0, fr[j], badFontStyle)
                sheet.write(i, 1, s, badFontStyle)
                i += 1
            else:
                sheet.write(i, 0, "", badFontStyle)
                sheet.write(i, 1, s,  badFontStyle)
                i += 1

    elif '~~~' in fr[j] and '~~~' not in nb[j]:
        # On doit split fr[i]
        sub_sent = fr[j].split(" ~~~ ")

        # On va dire que nb[i] correspond a la plus longue phrase de sub_sent
        longest_sent = max(sub_sent, key=len)

        for s in sub_sent:
            if s == longest_sent:
                sheet.write(i, 0, s, badFontStyle)
                sheet.write(i, 1, nb[j], badFontStyle)
                i += 1
            else:
                sheet.write(i, 0, s, badFontStyle)
                sheet.write(i, 1, "", badFontStyle)
                i += 1

workbook.save('output.xls')

system("rm alligned.txt")
system("rm dict.stem.dic")
system("rm translate.txt")

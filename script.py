# read json file

# Python program to read

import json
# translator
import googletrans
from googletrans import Translator
from fpdf import FPDF
from warnings import filterwarnings
import argparse
# parser
parser = argparse.ArgumentParser('My program')
parser.add_argument('-j', '--json')
parser.add_argument('-o', '--output')
args = parser.parse_args()

# parser info
json_file = args.json
output = args.output

translator = Translator()
pdf = FPDF()

# list for supported languge by font
gargi_supports_language = ['hindi', 'tamil']
fireflysung_supports_language = ['chinese', 'japanese']
# all google translate language with code
google_languages = googletrans.LANGUAGES

pdf.add_page()
# add font to the pdf
pdf.add_font('DejaVu', '',
             'font/DejaVuSansCondensed.ttf', uni=True)
pdf.add_font('fireflysung', '',
             'font/fireflysung.ttf', uni=True)
pdf.add_font('gargi', '',
             'font/gargi.ttf', uni=True)
pdf.add_font('kalpurush', '',
             'font/Kalpurush.ttf', uni=True)

# set fonts for pdf


def set_font(lan):
    if(lan.lower() in gargi_supports_language):
        pdf.set_font('gargi', '', 14)
    if(lan.lower() in fireflysung_supports_language):
        pdf.set_font('fireflysung', '', 14)


def find_language_code_set_font(language):
    # takes input as dict of language code and language name pair and returns language code and set the font for pdf
    if(language.lower() == 'bangla'):
        pdf.set_font('kalpurush', '', 14)
        return 'bn'
    myLanlist = {}
    for lan in google_languages:
        if(google_languages[lan] == language.lower()):
            set_font(language)
            return lan
        if(len(google_languages[lan].split(' ')) > 1):
            myLanlist[lan] = google_languages[lan].split(' ')[0]
    for lan in myLanlist:
        if(myLanlist[lan] == language.lower()):
            set_font(language)
            pdf.set_font('fireflysung', '', 14)
            return str(lan)


# Add a page
# set style and size of font
# that you want in the pdf
pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
pdf.set_font('DejaVu', '', 14)

with open(json_file) as f:
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    content = data["text"]
    languages = data["languages"]
    # Iterating through the json
    # list
    for i in languages:
        language = find_language_code_set_font(i)
        result = translator.translate(content, dest=language)
        pdf.multi_cell(800, 10, txt=str(i),
                       align='L')
        pdf.multi_cell(800, 10, txt=str(result.text),
                       align='L')
filterwarnings('ignore')
pdf.output(output, 'F')
filterwarnings('default')

#!/usr/bin/env python3

#--start of config--#

# Don't use Unicode characters.
ASCII_ONLY = False
# Don't use terminal color escapes.
COLORLESS = False
# Escape Turkish letters with a preceding symbol. `None` for no escaping.
ESCAPE_TURKISH_LETTERS = '/'
# User agent string to query the service with.
LIES_AND_DECEIT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'

#--end of config--#

# Nedir - A command-line tool to query the TDK Güncel Türkçe Sözlük.
# Written in 2023 by Natalie <razorlovesbaba@tuta.io>
#
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any
# warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication
# along with this software.
# If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

from sys import argv, stdout
from os import get_terminal_size
from urllib.request import Request, urlopen
from urllib.parse import quote
from json import loads

if COLORLESS:
	RESET = ''
	FAINT = ''
	ACCENT = ''
	ERROR = ''
else:
	RESET = '\x1b[0m'
	FAINT = '\x1b[2m'
	ACCENT = '\x1b[1;91m'
	ERROR = '\x1b[1;31m'

SYMBOLS = {
	'c': 'ç',
	'g': 'ğ',
	'i': 'ı',
	'o': 'ö',
	's': 'ş',
	'u': 'ü',
}

if len(argv) == 1:
	word = input(f'{ACCENT}kelime:{RESET} ')
	print(f'{FAINT}{('-' if ASCII_ONLY else '—') * (len(word) + 8)}{RESET}')
else:
	word = ' '.join(argv[1:])

if ESCAPE_TURKISH_LETTERS:
	for symbol, new_symbol in SYMBOLS.items():
		word = word.replace(ESCAPE_TURKISH_LETTERS + symbol, new_symbol)

req = Request(f'https://sozluk.gov.tr/gts?ara={quote(word)}')
req.add_header('User-Agent', LIES_AND_DECEIT)
with urlopen(req) as response:
	body = response.read()
	data = loads(body.decode('utf-8'))

if type(data) == dict and (error := data.get('error')):
	print(f'{ERROR}{error}{RESET}')
	quit()

for index, entry in enumerate(data):
	if index != 0: print()
	print(ACCENT, end='')
	if len(data) > 1: print(f'{index + 1}. ', end='')
	print(f'{entry["madde"]}:{RESET}', end='')
	print()

	for meaning in entry['anlamlarListe']:
		print(f'{ACCENT}-{RESET} {meaning["anlam"]}')
		if examples := meaning.get('orneklerListe'):
			for example in examples:
				print(f'  {ACCENT}>{RESET} {example["ornek"]}')

				if not example.get('yazar'): continue
				writer = example['yazar'][0]['tam_adi']
				print(f'    {FAINT}- {",".join(writer["tam_adi"] for writer in example["yazar"])}', end='')
				print(RESET)

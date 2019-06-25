#!/usr/bin/python3

import sys
import random
import statistics
import requests
from bs4 import BeautifulSoup
import genanki


# parse wikitables from wikipedia and wiktionary
def parse_wikipedia(soup):
  wikitables = soup.find_all("table", "wikitable")
  # unlike quizlet wikipedia pages can have more than one table.
  parsetable = None
  if len(wikitables) == 0:
    print("Page contains no wikitables.")
    return -1

  if len(wikitables) > 1:
    # ask user to select table (giving top-left as hint)
    print("Page contains multiple wikitables: the top-left cells of "
          + "each are listed below.\n")
    for idx,w in enumerate(wikitables):
      print("{}: ".format(idx) + w.find_all("tbody")[0].find_all("td")[0].text)
    while parsetable is None:
      try:
        x = int(input("\nWhich table do you want to parse? "))
        parsetable = wikitables[x]
      except:
        print("Invalid input.")
        parsetable = None
  elif len(wikitables) == 1:
    parsetable = wikitables[0]

  # now with table to be parsed selected its
  # just a matter of constructing the array
  result = []
  rows = parsetable.find_all("tr")
  for row in rows:
    colvals = []
    cols = row.find_all("td")
    for col in cols:
      colvals.append(col.text)
    if len(colvals) > 0:
      result.append(colvals)

  return result


# add support for parsing quizlets
def parse_quizlet(soup):
  cards = soup.find_all("div", "SetPageTerm-content")
  result = []
  for card in cards:
    cardvals = []
    # apparently some cards can have more than two sides so I'm being
    # careful here to not assume there's only a front and a back
    cardsides = card.find_all("div", "SetPageTerm-sideContent")
    for cardside in cardsides:
      cardvals.append(cardside.text)
    if len(cardvals) > 0:
      result.append(cardvals)

  return result


# Maps hostname to parsing function
function_table = {
  "en.wikipedia.org"  : parse_wikipedia,
  "en.wiktionary.org" : parse_wikipedia,
  "quizlet.com"       : parse_quizlet,
  # extend if necessary
}


# strip protocol and everything after the first non-period
# or alphanumeric char
def get_url_hostname(url: str) -> str:
  return url.split("//")[-1].split("/")[0].split("?")[0]


# only execute code if it is the main module.
# feel free to import this file and extend it yourself otherwise
if __name__ == "__main__":

  # TODO make this thing less stupid to use
  if len(sys.argv) != 6:
    print("web2anki v1.0.1")
    print("usage: " + sys.argv[0] + " <web-url> <front-format> <back-format> "
          + "<deck-name> <output-name>")
    print("Where web-url is a valid link to the page with protocol included "
          + "and front-format and back-format are HTML strings describing "
          + "the layout of the card.")
    print("More information can be found at "
          + "https://github.com/brandon-gong/web2anki")
    sys.exit(1)

  print("Attempting to connect to server at " + sys.argv[1] + "...")
  try:
    site_html = requests.get(sys.argv[1]).text
  except requests.exceptions.MissingSchema:
    print("The supplied url is invalid: no schema was found.  Did you mean "
          + "http://" + sys.argv[1] + "?")
  except requests.exceptions.ConnectionError:
    print("Failed to connect to server.  Check internet connectivity and "
          + "ensure that the url you have provided does not include typos.")
  print("Connection successful. Parsing...")

  result = None
  try:
    soup = BeautifulSoup(site_html, "html.parser")
    result = function_table[get_url_hostname(sys.argv[1])](soup)
  except KeyError:
    print("The website you are trying to parse ("
          + get_url_hostname(sys.argv[1])
          + ") is not currrently supported by web2anki."
          + "  Please consider implementing this functionality and open a"
          + " pull request at https://github.com/brandon-gong/web2anki.")

  # sanity check to make sure a table actually exists
  if result == -1:
    print("No cards found.")
    sys.exit(1)

  # calculate number of columns in the table.
  # Some wiki tables may not be perfectly regular (i.e. same number of cols
  # per row) so we need to make sure it doesn't crash when those happen.
  rowlens = []
  for row in result:
    rowlens.append(len(row))
  numcols = 0
  try:
    # get most common number of columns per row
    numcols = statistics.mode(rowlens)
  except:
    numcols = len(result[0])

  print("Table has {} columns.  Generating deck...".format(numcols))
  fieldtemplate = []
  for i in range(numcols):
    fieldtemplate.append({'name' : "col{}".format(i)})

  # construct the model
  vocab_model = genanki.Model(
    random.randrange(1 << 30, 1 << 31),
    'Simple Model',
    fields=fieldtemplate,
    templates=[{
      'name': 'Card 1',
      'qfmt': sys.argv[2],
      'afmt': sys.argv[3],
    }])

  # generate deck from rows
  vocab_deck = genanki.Deck(random.randrange(1 << 30, 1 << 31), sys.argv[4])
  decksize = 0
  for row in result:
    if len(row) != numcols:
      print("warning: irregular row length ({}); skipping".format(len(row)))
      continue
    vocab_deck.add_note(genanki.Note(
      model=vocab_model,
      fields=row
    ))
    decksize += 1

  # Log some data
  print("Deck '{}' created with {} cards.".format(sys.argv[4], decksize))
  print("Writing to file {}...".format(sys.argv[5]))

  # write to disk
  # TODO: can this fail somehow
  genanki.Package(vocab_deck).write_to_file(sys.argv[5])
  print("Done.")


# Web2Anki
This tool transforms tables online from sites such as Wikipedia and Quizlet
into Anki decks.  Anki is a free and open-source flashcards program that
utilizes spaced-recognition to improve memory and retention
of learned materials.

## Development
Web2Anki has not been extensively tested yet, so I encourage you check
back over your deck in the end to ensure all data has been transferred
accurately and appropriately.  Furthermore Web2Anki lacks frontends for sites
besides Wikipedia, Wiktionary, and Quizlet.  If you would like other sites to
be supported, I'm open to pull requests. Because this was built more for myself
than for general use I haven't really put much thought into usability and
flexibility of the program.  However I have made a _few_ efforts to make the
code sort of readable so feel free to modify it for your own purposes, or
import web2anki.py into your own program and use the functions I have
already written.

## Setting up
Download this repository to your computer, either via
```
git clone https://github.com/brandon-gong/web2anki
```
or by downloading the zip and decompressing it on your computer.

This tool relies on a number of 3rd-party packages installed from pip;
therefore, before
you run this program you must first install those packages.
```
pip3 install -r requirements.txt
```
All set.

## Usage
```
./web2anki.py <web-url> <front-format> <back-format> <deck-name> <output-name>
```
Where:
- `web-url` is the copied link to the webpage containing the table you
  want to transcribe, including protocol (ex. `https://`)
- `front-format` and `back-format` are all HTML strings that _can_ and
  _should_ include one or more extra variables surrouded by double
  curly braces.  These variables, for an n-columned table, include
  `FrontSide, col0, col1, col2, ..., col(n-1)`.
- `deck-name` is the name of the deck as it will appear in Anki once imported.
- `output-name` is the output name of your file.  Please include the
  .apkg extension in this argument.

After running, open Anki and use File > Import to import the generated
apkg file into the program.

### Example usage
Suppose we have this table that we would like to transcribe to Anki:

| Atomic number  | Element name  | Symbol  | Origin of name  |
| :------------: | :-----------: | :-----: | :-----------------: |
| 1              | Hydrogen      | H       | Greek elements hydro- and -gen, meaning 'water-forming'|
| 2              | Helium        |  He     | Greek hḗlios, 'sun' |
| 3              | Lithium       |  Li     |  Greek líthos, 'stone'|
| 4              | Beryllium     |  Be     |  beryl, a mineral (ultimately from the name of Belur in southern India) |
| 5              | Boron         |  B      |  borax, a mineral (from Arabic bawraq) |
| _and 112 more rows..._  |

Clearly 118 rows of elements will be extraordinarily difficult and tedious to
manually transcribe, and also open up the likelihood of human error.  Luckily,
this is a case where Web2Anki will be very handy in assisting the
transcription.

On the front of the card we want the element name; on the back, the symbol.
Easy enough.  The command is:
```
./web2anki.py https://en.wikipedia.org/wiki/List_of_chemical_elements "{{col1}}" "{{FrontSide}}<br>{{col2}}" "Element Names and Symbols" output.apkg`
```
(`./web2anki.py` and `python3 web2anki.py` are interchangeable)

Notice the usage of `{{FrontSide}}`.  `{{FrontSide}}` is  special variable
that contains all of the HTML code for the front of the card; in this case, it
would be equivalent to the second argument, "`{{col1}}`".  It's sole purpose
is to help reduce the amount you have to repeat yourself.

Let's say we want to display the atomic number on the front of the card, in
big bold text, and on the back we want to add the atomic name and origin.
What's the command?  Simply modifying arguments 2 and 3 gives:
```
./web2anki.py https://en.wikipedia.org/wiki/List_of_chemical_elements "<h1>{{col0}}</h1>" "{{FrontSide}}<br>{{col1}}, originating from {{col3}}" "Element Names and Symbols" output.apkg`
```

Clearly you will need some basic understanding of how to use html tags to
achieve more complex formatting.  A quick crash course:
- Wrap text you want to format in a certain way in tags
- These tags include `<i>` for italic, `<b>` for bold, `<h1>`, `<h2>`, `<h3>`
  for progressively smaller headers and subheaders, and `<sup>`, `<sub>` for
  superscripts and subscripts respectively.
- For example: `<i>Hello</i> this <b>is an</b> <sup>example</sup>` will give
  _Hello_ this **is an** <sup>example</sup>.
- Furthermore, you can create newlines using the `<br>` tag.

For more help on HTML formatting, there's this thing called Google that
will be able to guide you.

## Issues, Feature requests
Unfortunately, as this was just a quick little tool I built to help myself,
I am not super interested in spending more time than needed implementing
support for more websites that I will never use myself.  If you want support
for those sites, you will have to implement that yourself.
However, I am open to fixing small bugs or cases that won't take too much
of my time.

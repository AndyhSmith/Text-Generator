# Text-Generator

Description: Used to generate non-sense text based on simple language patterns in Wikipedia articles. This does not use LLMs or any other advanced methods, it simply uses the frequency of
characters to generate text.

Additional Notes:

-   Anything generated with meaningful words is purely coincidental.
-   When training data is limited generated text may be similar to the training data.
-   Wikipedia articles are chosen at random, training content is not filtered.
-   I have not run this on all languages, the python program will let you do your own training.

## Files

**main.py:** Main file, used to generate text.

**WikipediaWPCodes.json:** Wikipedia article language codes, used to get random articles.

**Languages/\***\_data.json: Training data for each language.

_The files in the Languages folder contain weights and frequencies for each character in the language associated with the file. You can use those weights and frequencies to generate text._

## Usage

```bash
$ pip install requests
$ python3 .\main.py
```

## Data Model

```json
{
    // Various stats
    "stats": {
        "totalCharsAnalyzed": 4 // Total chars analyzed
    },
    "pages": {
        "Article ID": "Article Title"
    },
    // First Char
    "a": {
        // Frequency/count of chars after first char
        "frequency": {
            "b": 3,
            "c": 1
        },
        "frequencyTotal": 3, // Sum of all frequencies
        // Chance of chars after the first char being selected
        "weights": {
            "b": 0.75,
            "c": 0.25
        }
    },
    // Chance of initial char being selected
    "firstCharWeight": {
        "a": 1
    }
}
```

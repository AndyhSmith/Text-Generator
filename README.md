# Text-Generator

Attempts to generate text in different languages using a simple frequency table.

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

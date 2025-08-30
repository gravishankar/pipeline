# 📚 Vocabulary Database Exports

Export files generated from the RobertsGuide vocabulary database (365 words total).

## 📋 **File Index**

### **Complete Database Export**
- **`RobertsGuide_Complete_365_words.csv`** - All 365 words with full data (366 lines including header)

### **Alphabetical Splits** 
- **`RobertsGuide_A-H_alphabetical.csv`** - Words A through H (123 lines including header)
- **`RobertsGuide_I-P_alphabetical.csv`** - Words I through P (95 lines including header)  
- **`RobertsGuide_Q-Z_alphabetical.csv`** - Words Q through Z (126 lines including header)

### **By Parts of Speech**
- **`RobertsGuide_Adjectives_only.csv`** - All adjectives (195 lines including header)
- **`RobertsGuide_Nouns_only.csv`** - All nouns (81 lines including header)
- **`RobertsGuide_Verbs_only.csv`** - All verbs (86 lines including header)

### **Special Purpose**
- **`RobertsGuide_Random_100_flashcards.csv`** - Random 100 words for flashcard creation (100 lines)

## 📊 **Data Structure**

### **Complete Export Fields:**
```csv
word,part_of_speech,definition,example_sentence,mnemonic,difficulty,source,quality_score,date_added
```

### **Simplified Export Fields:**
```csv
word,part_of_speech,definition,example_sentence
```

### **Flashcard Export Fields:**
```csv
word,definition
```

## 🎯 **Usage Examples**

### **Import into Excel/Google Sheets**
1. Open Excel/Google Sheets
2. File → Import → Choose CSV file
3. Select comma as delimiter
4. Headers are included in row 1

### **Import into Anki (Flashcards)**
1. Use `RobertsGuide_Random_100_flashcards.csv`
2. Anki → File → Import
3. Field separator: Comma
4. Map: Field 1 → Front, Field 2 → Back

### **Use in Programming**
```python
import pandas as pd

# Load complete vocabulary
df = pd.read_csv('RobertsGuide_Complete_365_words.csv')

# Load only nouns
nouns = pd.read_csv('RobertsGuide_Nouns_only.csv')

# Sample usage
print(f"Total words: {len(df)}")
print(f"Nouns: {len(nouns)}")
```

## 📈 **Word Statistics**

- **Total Words**: 365
- **Quality Score**: 4.0/5 (High Quality)
- **Difficulty**: Advanced level
- **Source**: RobertsNerdyGuide
- **Added**: 2025-08-29

### **Part of Speech Distribution:**
- **Adjectives**: ~194 words (53%)
- **Nouns**: ~80 words (22%) 
- **Verbs**: ~85 words (23%)
- **Adverbs**: ~6 words (2%)

## 🔄 **Regenerating Exports**

To create new export files:

```bash
# Complete export
sqlite3 vocabulary.db -header -csv "SELECT * FROM vocabulary WHERE source = 'RobertsGuide' ORDER BY word;" > new_export.csv

# Custom filters
sqlite3 vocabulary.db -header -csv "SELECT word, definition FROM vocabulary WHERE part_of_speech = 'noun';" > nouns_only.csv
```

## 📝 **Notes**

- All exports are UTF-8 encoded
- Quotes in definitions are properly escaped
- Empty fields show as blank in CSV
- Headers included in all main export files
- Random flashcard file regenerates differently each time

---

**Generated**: August 30, 2025  
**Database Version**: RobertsGuide v1.0  
**Total Records**: 365 vocabulary words
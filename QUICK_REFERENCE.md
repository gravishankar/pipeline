# 📋 Quick Reference - Vocabulary Database Queries

## 🚀 **Instant Commands**

```bash
# 1. Show database overview
python3 show_vocabulary.py

# 2. Interactive explorer
python3 query_vocabulary.py

# 3. Direct database access
sqlite3 vocabulary.db -header -column
```

## 🔢 **Essential Counts**
```bash
# Total words
sqlite3 vocabulary.db "SELECT COUNT(*) FROM vocabulary;"

# Words by source
sqlite3 vocabulary.db "SELECT source, COUNT(*) FROM vocabulary GROUP BY source;"

# Words by part of speech
sqlite3 vocabulary.db "SELECT part_of_speech, COUNT(*) FROM vocabulary GROUP BY part_of_speech;"
```

## 🔤 **Word Lists**
```bash
# First 20 words
sqlite3 vocabulary.db "SELECT word, definition FROM vocabulary ORDER BY word LIMIT 20;"

# Random 10 words
sqlite3 vocabulary.db "SELECT word, definition FROM vocabulary ORDER BY RANDOM() LIMIT 10;"

# All RobertsGuide words
sqlite3 vocabulary.db "SELECT word, definition FROM vocabulary WHERE source = 'RobertsGuide';"
```

## 🔍 **Quick Searches**
```bash
# Search word names
sqlite3 vocabulary.db "SELECT word, definition FROM vocabulary WHERE word LIKE '%SEARCHTERM%';"

# Search definitions
sqlite3 vocabulary.db "SELECT word, definition FROM vocabulary WHERE definition LIKE '%SEARCHTERM%';"

# Find nouns/verbs/adjectives
sqlite3 vocabulary.db "SELECT word, definition FROM vocabulary WHERE part_of_speech = 'noun';"
```

## 📊 **Top Queries**
```bash
# High quality words (4+ score)
sqlite3 vocabulary.db "SELECT word, definition, quality_score FROM vocabulary WHERE quality_score >= 4;"

# Words with examples
sqlite3 vocabulary.db "SELECT word, definition, example_sentence FROM vocabulary WHERE example_sentence IS NOT NULL;"

# Recently added
sqlite3 vocabulary.db "SELECT word, source, date_added FROM vocabulary ORDER BY date_added DESC LIMIT 10;"
```

## 💾 **Save Results**
```bash
# Save to file
sqlite3 vocabulary.db "SELECT word, definition FROM vocabulary;" > wordlist.txt

# Save as CSV
sqlite3 vocabulary.db -csv "SELECT * FROM vocabulary;" > vocabulary.csv
```

---
**📖 For complete guide see: QUERY_USAGE_GUIDE.md**
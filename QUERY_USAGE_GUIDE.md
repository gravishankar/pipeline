# 🔍 Vocabulary Database Query Guide

Complete guide for exploring and querying your vocabulary database using the tools and scripts provided.

## 📋 **Table of Contents**

1. [Quick Start](#-quick-start)
2. [Database Overview](#-database-overview)
3. [Python Query Scripts](#-python-query-scripts)
4. [Direct SQLite Commands](#-direct-sqlite-commands)
5. [Common Query Patterns](#-common-query-patterns)
6. [Advanced Queries](#-advanced-queries)
7. [Troubleshooting](#-troubleshooting)

---

## 🚀 **Quick Start**

### **Method 1: Simple Display Script**
```bash
# Show database summary and samples
python3 show_vocabulary.py
```

### **Method 2: Interactive Explorer**
```bash
# Launch interactive menu system
python3 query_vocabulary.py
```

### **Method 3: Direct SQLite Commands**
```bash
# Access database directly
sqlite3 vocabulary.db
```

---

## 📊 **Database Overview**

### **Database Schema**
```sql
CREATE TABLE vocabulary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL,
    part_of_speech TEXT,
    definition TEXT NOT NULL,
    example_sentence TEXT,
    mnemonic TEXT,
    difficulty TEXT DEFAULT 'medium',
    source TEXT NOT NULL,
    date_added TEXT NOT NULL,
    quality_score INTEGER DEFAULT 3
);
```

### **Current Data Sources**
- **RobertsGuide**: 365 advanced vocabulary words (Quality: 4/5)

---

## 🐍 **Python Query Scripts**

### **1. show_vocabulary.py - Simple Display**

**What it does:**
- Shows database statistics
- Displays sample RobertsGuide words
- Lists top words alphabetically
- Shows recently added words

**How to use:**
```bash
cd /path/to/apps/directory
python3 show_vocabulary.py
```

**Sample Output:**
```
================================================================================
🎓 VOCABULARY DATABASE SUMMARY
================================================================================

📚 ROBERTSGUIDE:
   advanced: 365 words (avg quality: 4.0/5)
   Added: 2025-08-29

🎯 TOTAL VOCABULARY: 365 words

📖 ROBERTS NERDY GUIDE - SAMPLE WORDS
================================================================================

 1. ABUNDANCE (noun)
    Definition: A large quantity of something.
    Example: "The farmer was pleased with the abundance of crops this season."
```

### **2. query_vocabulary.py - Interactive Explorer**

**What it does:**
- Interactive menu system
- Search functionality
- Detailed statistics
- Customizable queries

**How to use:**
```bash
python3 query_vocabulary.py
```

**Menu Options:**
1. **📊 Database Statistics** - Complete overview of all data
2. **🔤 Top 100 Words** - Alphabetical word list
3. **📚 RobertsGuide Data** - Specific RobertsGuide content
4. **⏰ Recent Additions** - Recently added words
5. **🔍 Search Words** - Search by word or definition
6. **🎯 Top 50 Words** - Quick word preview

**Example Usage:**
```
Choose option: 5
Enter search term: ambig
```

**Search Results:**
```
🔍 SEARCH RESULTS for 'ambig'
==================================================
Found 2 matches

🔹 ambiguity (noun) - [RobertsGuide]
   Uncertainty or lack of clarity.
   Example: "The ambiguity of the statement caused confusion."

🔹 ambiguous (adj) - [RobertsGuide]
   Open to multiple interpretations.
   Example: "Her response was ambiguous and left room for doubt."
```

---

## 💾 **Direct SQLite Commands**

### **Opening the Database**
```bash
# Basic access
sqlite3 vocabulary.db

# With formatted output
sqlite3 vocabulary.db -header -column
```

### **Essential SQLite Commands**
```sql
-- Show all tables
.tables

-- Show table structure
.schema vocabulary

-- Exit SQLite
.quit

-- Enable headers and column mode
.header on
.mode column
```

---

## 🎯 **Common Query Patterns**

### **1. Word Counting and Statistics**

```sql
-- Total word count
SELECT COUNT(*) as total_words FROM vocabulary;

-- Count by source
SELECT source, COUNT(*) as word_count 
FROM vocabulary 
GROUP BY source;

-- Count by difficulty
SELECT difficulty, COUNT(*) as count 
FROM vocabulary 
GROUP BY difficulty;

-- Average quality score
SELECT source, AVG(quality_score) as avg_quality 
FROM vocabulary 
GROUP BY source;
```

### **2. Word Browsing**

```sql
-- First 20 words alphabetically
SELECT word, part_of_speech, definition 
FROM vocabulary 
ORDER BY word 
LIMIT 20;

-- Random 10 words
SELECT word, definition 
FROM vocabulary 
ORDER BY RANDOM() 
LIMIT 10;

-- Words with examples
SELECT word, definition, example_sentence 
FROM vocabulary 
WHERE example_sentence IS NOT NULL 
LIMIT 10;
```

### **3. Source-Specific Queries**

```sql
-- All RobertsGuide words
SELECT word, part_of_speech, definition 
FROM vocabulary 
WHERE source = 'RobertsGuide' 
ORDER BY word;

-- RobertsGuide statistics
SELECT 
    COUNT(*) as total_words,
    AVG(quality_score) as avg_quality,
    MIN(date_added) as first_added,
    MAX(date_added) as last_added
FROM vocabulary 
WHERE source = 'RobertsGuide';
```

### **4. Search and Filter**

```sql
-- Search word names
SELECT word, definition 
FROM vocabulary 
WHERE word LIKE '%ambig%';

-- Search definitions
SELECT word, definition 
FROM vocabulary 
WHERE definition LIKE '%large%';

-- Case-insensitive search
SELECT word, definition 
FROM vocabulary 
WHERE LOWER(word) LIKE '%abc%' 
   OR LOWER(definition) LIKE '%xyz%';

-- Words by part of speech
SELECT word, definition 
FROM vocabulary 
WHERE part_of_speech = 'noun';

-- High-quality words only
SELECT word, definition, quality_score 
FROM vocabulary 
WHERE quality_score >= 4;
```

---

## 🔬 **Advanced Queries**

### **1. Complex Analysis**

```sql
-- Longest definitions
SELECT word, LENGTH(definition) as def_length, definition 
FROM vocabulary 
ORDER BY LENGTH(definition) DESC 
LIMIT 10;

-- Words with longest names
SELECT word, LENGTH(word) as word_length 
FROM vocabulary 
ORDER BY LENGTH(word) DESC 
LIMIT 10;

-- Part of speech distribution
SELECT 
    part_of_speech,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM vocabulary), 2) as percentage
FROM vocabulary 
GROUP BY part_of_speech 
ORDER BY count DESC;
```

### **2. Date-Based Queries**

```sql
-- Words added today
SELECT word, source, date_added 
FROM vocabulary 
WHERE DATE(date_added) = DATE('now');

-- Words added in last 7 days
SELECT word, source, date_added 
FROM vocabulary 
WHERE date_added >= datetime('now', '-7 days') 
ORDER BY date_added DESC;

-- Words by month
SELECT 
    strftime('%Y-%m', date_added) as month,
    COUNT(*) as words_added 
FROM vocabulary 
GROUP BY strftime('%Y-%m', date_added);
```

### **3. Quality Analysis**

```sql
-- Quality score distribution
SELECT 
    quality_score,
    COUNT(*) as count 
FROM vocabulary 
GROUP BY quality_score 
ORDER BY quality_score DESC;

-- Best quality words
SELECT word, definition, quality_score 
FROM vocabulary 
WHERE quality_score = 5;

-- Words needing quality improvement
SELECT word, definition, quality_score 
FROM vocabulary 
WHERE quality_score <= 2;
```

---

## 📝 **Practical Examples**

### **Example 1: Creating Word Lists**

```sql
-- SAT prep word list (advanced words)
SELECT word, definition 
FROM vocabulary 
WHERE difficulty = 'advanced' 
ORDER BY word;

-- Words for flashcards
SELECT 
    word,
    part_of_speech,
    definition,
    example_sentence
FROM vocabulary 
WHERE quality_score >= 4 
ORDER BY RANDOM() 
LIMIT 50;
```

### **Example 2: Educational Content**

```sql
-- Words by topic (using definition keywords)
SELECT word, definition 
FROM vocabulary 
WHERE definition LIKE '%science%' 
   OR definition LIKE '%research%' 
   OR definition LIKE '%study%';

-- Academic vocabulary
SELECT word, definition 
FROM vocabulary 
WHERE definition LIKE '%research%' 
   OR definition LIKE '%analysis%' 
   OR definition LIKE '%study%' 
   OR definition LIKE '%theory%';
```

### **Example 3: Data Export**

```sql
-- Export to CSV format
.mode csv
.output vocabulary_export.csv
SELECT word, part_of_speech, definition, example_sentence 
FROM vocabulary 
ORDER BY word;
.output stdout
.mode column
```

---

## 🛠 **Using Query Results**

### **1. Save Results to File**

```bash
# Save query results
sqlite3 vocabulary.db "SELECT word, definition FROM vocabulary ORDER BY word;" > word_list.txt

# Save with headers
sqlite3 vocabulary.db -header -csv "SELECT * FROM vocabulary;" > vocabulary_complete.csv
```

### **2. Pipe to Other Tools**

```bash
# Count words starting with 'A'
sqlite3 vocabulary.db "SELECT word FROM vocabulary WHERE word LIKE 'a%';" | wc -l

# Search for specific patterns
sqlite3 vocabulary.db "SELECT word FROM vocabulary;" | grep "^con"
```

---

## 🔧 **Troubleshooting**

### **Common Issues**

**Problem**: `sqlite3: command not found`
**Solution**: Install SQLite3
```bash
# macOS
brew install sqlite3

# Ubuntu/Debian
sudo apt-get install sqlite3

# Windows
Download from https://sqlite.org/download.html
```

**Problem**: `no such table: vocabulary`
**Solution**: Check database file exists
```bash
ls -la vocabulary.db
sqlite3 vocabulary.db ".tables"
```

**Problem**: Python script not found
**Solution**: Ensure you're in the apps directory
```bash
cd /path/to/vocab_pipeline/apps/
ls -la *.py
```

### **Database Maintenance**

```sql
-- Check database integrity
PRAGMA integrity_check;

-- Optimize database
VACUUM;

-- Show database info
PRAGMA table_info(vocabulary);
```

---

## 📚 **Query Cookbook - Copy & Paste Ready**

### **Quick Lookups**
```bash
# Show word count
sqlite3 vocabulary.db "SELECT COUNT(*) FROM vocabulary;"

# Show sources
sqlite3 vocabulary.db "SELECT DISTINCT source FROM vocabulary;"

# Random word of the day
sqlite3 vocabulary.db "SELECT word, definition FROM vocabulary ORDER BY RANDOM() LIMIT 1;"
```

### **Word Lists**
```bash
# All nouns
sqlite3 vocabulary.db -header -column "SELECT word, definition FROM vocabulary WHERE part_of_speech = 'noun' ORDER BY word;"

# All verbs
sqlite3 vocabulary.db -header -column "SELECT word, definition FROM vocabulary WHERE part_of_speech = 'verb' ORDER BY word;"

# All adjectives
sqlite3 vocabulary.db -header -column "SELECT word, definition FROM vocabulary WHERE part_of_speech = 'adj' ORDER BY word;"
```

### **Search Queries**
```bash
# Find words containing 'tion'
sqlite3 vocabulary.db "SELECT word FROM vocabulary WHERE word LIKE '%tion';"

# Find words about emotions
sqlite3 vocabulary.db "SELECT word, definition FROM vocabulary WHERE definition LIKE '%feeling%' OR definition LIKE '%emotion%';"
```

---

## 🎓 **Tips for Best Results**

1. **Use `.header on` and `.mode column`** for readable output
2. **Add `LIMIT`** to large queries to avoid overwhelming output
3. **Use `ORDER BY word`** for alphabetical results
4. **Save complex queries** in `.sql` files for reuse
5. **Use `%pattern%`** for partial matches in LIKE queries
6. **Combine multiple conditions** with AND/OR for precise searches

---

## 📞 **Need Help?**

- Check the database exists: `ls -la vocabulary.db`
- Verify Python scripts: `ls -la *.py`
- Test SQLite: `sqlite3 --version`
- View table structure: `sqlite3 vocabulary.db ".schema vocabulary"`

---

**Happy Querying! 🔍📚**

*Your vocabulary database contains 365 high-quality words ready for exploration!*
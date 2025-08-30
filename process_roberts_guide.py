#!/usr/bin/env python3
"""
Process RobertsNerdyGuide.csv and add it to the vocabulary database.
"""

import sqlite3
import csv
import re
from pathlib import Path
from datetime import datetime

def create_database_schema(db_path):
    """Create the vocabulary database schema."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create vocabulary table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vocabulary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        part_of_speech TEXT,
        definition TEXT NOT NULL,
        example_sentence TEXT,
        mnemonic TEXT,
        difficulty TEXT DEFAULT 'medium',
        source TEXT NOT NULL,
        date_added TEXT NOT NULL,
        quality_score INTEGER DEFAULT 3,
        UNIQUE(word, source)
    )
    ''')
    
    # Create index for faster searches
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_word ON vocabulary(word)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_source ON vocabulary(source)')
    
    conn.commit()
    conn.close()
    print("Database schema created successfully.")

def parse_csv_line(line):
    """Parse a single line from the RobertsNerdyGuide.csv file."""
    # Split on comma, but handle quoted text
    parts = []
    current_part = ""
    in_quotes = False
    
    for char in line.strip():
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            parts.append(current_part)
            current_part = ""
        else:
            current_part += char
    
    # Add the last part
    if current_part:
        parts.append(current_part)
    
    if len(parts) < 2:
        return None
        
    word = parts[0].strip()
    definition_and_example = parts[1].strip()
    
    # Extract part of speech from definition
    pos_match = re.match(r'^([^\.]+)\.\s*(.+)', definition_and_example)
    if pos_match:
        pos = pos_match.group(1).strip()
        rest = pos_match.group(2).strip()
    else:
        pos = "unknown"
        rest = definition_and_example
    
    # Extract example sentence (text in parentheses)
    example_match = re.search(r'\("([^"]+)"\)$', rest)
    if example_match:
        example_sentence = example_match.group(1)
        definition = rest[:example_match.start()].strip()
    else:
        # Try without quotes
        example_match = re.search(r'\(([^)]+)\)$', rest)
        if example_match:
            example_sentence = example_match.group(1)
            definition = rest[:example_match.start()].strip()
        else:
            example_sentence = ""
            definition = rest
    
    return {
        'word': word,
        'part_of_speech': pos,
        'definition': definition,
        'example_sentence': example_sentence,
        'mnemonic': '',  # RobertsGuide doesn't include mnemonics
        'difficulty': 'advanced',  # Most words seem advanced
        'source': 'RobertsGuide',
        'date_added': datetime.now().isoformat(),
        'quality_score': 4  # High quality definitions and examples
    }

def process_roberts_guide(csv_path, db_path):
    """Process the RobertsNerdyGuide.csv file and add to database."""
    print(f"Processing {csv_path}...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    words_added = 0
    words_skipped = 0
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            try:
                word_data = parse_csv_line(line)
                if not word_data:
                    continue
                
                # Insert into database
                cursor.execute('''
                INSERT OR IGNORE INTO vocabulary 
                (word, part_of_speech, definition, example_sentence, mnemonic, 
                 difficulty, source, date_added, quality_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    word_data['word'],
                    word_data['part_of_speech'],
                    word_data['definition'],
                    word_data['example_sentence'],
                    word_data['mnemonic'],
                    word_data['difficulty'],
                    word_data['source'],
                    word_data['date_added'],
                    word_data['quality_score']
                ))
                
                if cursor.rowcount > 0:
                    words_added += 1
                    print(f"Added: {word_data['word']}")
                else:
                    words_skipped += 1
                    print(f"Skipped (duplicate): {word_data['word']}")
                    
            except Exception as e:
                print(f"Error processing line {line_num}: {e}")
                print(f"Line content: {line[:100]}...")
                continue
    
    conn.commit()
    conn.close()
    
    print(f"\nProcessing complete!")
    print(f"Words added: {words_added}")
    print(f"Words skipped: {words_skipped}")
    print(f"Total processed: {words_added + words_skipped}")

def main():
    """Main function to process RobertsNerdyGuide.csv."""
    # Set up paths
    base_path = Path(__file__).parent
    csv_path = base_path / "Data" / "csv" / "RobertsNerdyGuide.csv"
    db_path = base_path / "Data" / "vocabulary.db"
    
    if not csv_path.exists():
        print(f"Error: CSV file not found at {csv_path}")
        return
    
    # Create database schema
    create_database_schema(db_path)
    
    # Process the CSV file
    process_roberts_guide(csv_path, db_path)
    
    # Verify the data was added
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM vocabulary WHERE source = 'RobertsGuide'")
    roberts_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM vocabulary")
    total_count = cursor.fetchone()[0]
    
    print(f"\nDatabase verification:")
    print(f"RobertsGuide words: {roberts_count}")
    print(f"Total words in database: {total_count}")
    
    # Show some sample entries
    print(f"\nSample RobertsGuide entries:")
    cursor.execute("""
    SELECT word, part_of_speech, definition, example_sentence 
    FROM vocabulary 
    WHERE source = 'RobertsGuide' 
    ORDER BY word 
    LIMIT 5
    """)
    
    for word, pos, definition, example in cursor.fetchall():
        print(f"- {word} ({pos}): {definition}")
        if example:
            print(f"  Example: {example}")
    
    conn.close()

if __name__ == "__main__":
    main()
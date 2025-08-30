#!/usr/bin/env python3
"""
Simple script to display vocabulary database content.
"""

import sqlite3
import sys
from pathlib import Path

def main():
    db_path = Path(__file__).parent / "vocabulary.db"
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=" * 80)
    print("🎓 VOCABULARY DATABASE SUMMARY")
    print("=" * 80)
    
    # Database Statistics
    cursor.execute("""
        SELECT 
            source,
            COUNT(*) as word_count,
            AVG(quality_score) as avg_quality,
            difficulty,
            MIN(date_added) as first_added
        FROM vocabulary 
        GROUP BY source, difficulty
        ORDER BY source, difficulty
    """)
    
    current_source = None
    for source, count, avg_quality, difficulty, first_added in cursor.fetchall():
        if source != current_source:
            print(f"\n📚 {source.upper()}:")
            current_source = source
        print(f"   {difficulty}: {count} words (avg quality: {avg_quality:.1f}/5)")
        print(f"   Added: {first_added[:10]}")
    
    # Total count
    cursor.execute("SELECT COUNT(*) FROM vocabulary")
    total = cursor.fetchone()[0]
    print(f"\n🎯 TOTAL VOCABULARY: {total} words")
    
    print("\n" + "=" * 80)
    print("📖 ROBERTS NERDY GUIDE - SAMPLE WORDS")
    print("=" * 80)
    
    # Show RobertsGuide samples
    cursor.execute("""
        SELECT word, part_of_speech, definition, example_sentence 
        FROM vocabulary 
        WHERE source = 'RobertsGuide' 
        ORDER BY word 
        LIMIT 15
    """)
    
    for i, (word, pos, definition, example) in enumerate(cursor.fetchall(), 1):
        print(f"\n{i:2d}. {word.upper()} ({pos})")
        print(f"    Definition: {definition}")
        if example:
            print(f"    Example: {example}")
    
    print("\n" + "=" * 80)
    print("🔤 TOP 25 WORDS (Alphabetically)")
    print("=" * 80)
    
    cursor.execute("""
        SELECT word, part_of_speech, LEFT(definition, 50) as short_def
        FROM vocabulary 
        ORDER BY word 
        LIMIT 25
    """)
    
    for i, (word, pos, short_def) in enumerate(cursor.fetchall(), 1):
        # Handle SQLite not having LEFT function
        if len(short_def) > 47:
            short_def = short_def[:47] + "..."
        print(f"{i:2d}. {word:20s} ({pos:4s}) {short_def}")
    
    print("\n" + "=" * 80)
    print("⏰ RECENTLY ADDED WORDS")
    print("=" * 80)
    
    cursor.execute("""
        SELECT word, source, date_added, LEFT(definition, 40) as short_def
        FROM vocabulary 
        ORDER BY date_added DESC 
        LIMIT 10
    """)
    
    for word, source, date_added, short_def in cursor.fetchall():
        date_str = date_added[:10] + " " + date_added[11:19]
        if len(short_def) > 37:
            short_def = short_def[:37] + "..."
        print(f"{word:20s} [{source:12s}] {date_str} - {short_def}")
    
    conn.close()

if __name__ == "__main__":
    main()
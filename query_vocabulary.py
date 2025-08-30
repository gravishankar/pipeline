#!/usr/bin/env python3
"""
Query script for exploring vocabulary database.
"""

import sqlite3
from pathlib import Path

def connect_db():
    """Connect to the vocabulary database."""
    db_path = Path(__file__).parent / "vocabulary.db"
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        return None
    return sqlite3.connect(db_path)

def show_top_words(limit=100):
    """Show top N words alphabetically."""
    conn = connect_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT word, part_of_speech, definition 
        FROM vocabulary 
        ORDER BY word 
        LIMIT ?
    """, (limit,))
    
    print(f"\n🔤 TOP {limit} WORDS (Alphabetically)")
    print("=" * 60)
    
    for i, (word, pos, definition) in enumerate(cursor.fetchall(), 1):
        print(f"{i:3d}. {word} ({pos})")
        print(f"     {definition}")
        print()
    
    conn.close()

def show_roberts_guide_data():
    """Show RobertsGuide vocabulary data."""
    conn = connect_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    # Get count and date info
    cursor.execute("""
        SELECT 
            COUNT(*) as total_words,
            MIN(date_added) as first_added,
            MAX(date_added) as last_added
        FROM vocabulary 
        WHERE source = 'RobertsGuide'
    """)
    
    count, first_added, last_added = cursor.fetchone()
    
    print(f"\n📚 ROBERTS NERDY GUIDE DATA")
    print("=" * 50)
    print(f"Total Words: {count}")
    print(f"Added: {first_added[:10]} {first_added[11:19]}")
    print(f"Quality Score: 4/5 (High Quality)")
    print(f"Difficulty: Advanced")
    print()
    
    # Show sample words
    cursor.execute("""
        SELECT word, part_of_speech, definition, example_sentence 
        FROM vocabulary 
        WHERE source = 'RobertsGuide' 
        ORDER BY word 
        LIMIT 20
    """)
    
    print("📖 SAMPLE WORDS:")
    print("-" * 50)
    
    for word, pos, definition, example in cursor.fetchall():
        print(f"🔹 {word} ({pos})")
        print(f"   Definition: {definition}")
        if example:
            print(f"   Example: {example}")
        print()
    
    conn.close()

def search_words(search_term):
    """Search for words containing the search term."""
    conn = connect_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT word, part_of_speech, definition, example_sentence, source 
        FROM vocabulary 
        WHERE word LIKE ? OR definition LIKE ?
        ORDER BY word
    """, (f"%{search_term}%", f"%{search_term}%"))
    
    results = cursor.fetchall()
    
    print(f"\n🔍 SEARCH RESULTS for '{search_term}'")
    print("=" * 50)
    print(f"Found {len(results)} matches")
    print()
    
    for word, pos, definition, example, source in results:
        print(f"🔹 {word} ({pos}) - [{source}]")
        print(f"   {definition}")
        if example:
            print(f"   Example: {example}")
        print()
    
    conn.close()

def show_database_stats():
    """Show overall database statistics."""
    conn = connect_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    # Total count by source
    cursor.execute("""
        SELECT 
            source,
            COUNT(*) as word_count,
            AVG(quality_score) as avg_quality,
            MIN(date_added) as first_added
        FROM vocabulary 
        GROUP BY source 
        ORDER BY word_count DESC
    """)
    
    print(f"\n📊 DATABASE STATISTICS")
    print("=" * 60)
    
    total_words = 0
    for source, count, avg_quality, first_added in cursor.fetchall():
        print(f"📚 {source}:")
        print(f"   Words: {count}")
        print(f"   Avg Quality: {avg_quality:.1f}/5")
        print(f"   Added: {first_added[:10]}")
        print()
        total_words += count
    
    print(f"🎯 TOTAL VOCABULARY: {total_words} words")
    
    # Show difficulty distribution
    cursor.execute("""
        SELECT difficulty, COUNT(*) as count 
        FROM vocabulary 
        GROUP BY difficulty 
        ORDER BY count DESC
    """)
    
    print(f"\n📈 DIFFICULTY LEVELS:")
    for difficulty, count in cursor.fetchall():
        print(f"   {difficulty}: {count} words")
    
    conn.close()

def show_recent_additions(days=7):
    """Show recently added words."""
    conn = connect_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT word, source, date_added, definition 
        FROM vocabulary 
        WHERE date_added >= datetime('now', '-{} days')
        ORDER BY date_added DESC 
        LIMIT 50
    """.format(days))
    
    results = cursor.fetchall()
    
    print(f"\n⏰ RECENT ADDITIONS (Last {days} days)")
    print("=" * 50)
    print(f"Found {len(results)} recent additions")
    print()
    
    for word, source, date_added, definition in results:
        print(f"🆕 {word} [{source}]")
        print(f"   Added: {date_added[:10]} {date_added[11:19]}")
        print(f"   {definition}")
        print()
    
    conn.close()

def main():
    """Main interactive menu."""
    while True:
        print("\n" + "="*60)
        print("🎓 VOCABULARY DATABASE EXPLORER")
        print("="*60)
        print("1. 📊 Database Statistics")
        print("2. 🔤 Top 100 Words (Alphabetical)")
        print("3. 📚 RobertsGuide Data")
        print("4. ⏰ Recent Additions")
        print("5. 🔍 Search Words")
        print("6. 🎯 Top 50 Words")
        print("0. ❌ Exit")
        print()
        
        choice = input("Choose an option (0-6): ").strip()
        
        if choice == "1":
            show_database_stats()
        elif choice == "2":
            show_top_words(100)
        elif choice == "3":
            show_roberts_guide_data()
        elif choice == "4":
            show_recent_additions()
        elif choice == "5":
            term = input("Enter search term: ").strip()
            if term:
                search_words(term)
        elif choice == "6":
            show_top_words(50)
        elif choice == "0":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
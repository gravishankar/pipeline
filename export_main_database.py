#!/usr/bin/env python3
"""
Export script for the main vocabulary database (11,107+ words).
Creates logical splits of 500 words each and organized exports by criteria.
"""

import sqlite3
import os
from pathlib import Path

def create_export_directory():
    """Create main vocabulary exports directory."""
    export_dir = Path(__file__).parent / "main_vocabulary_exports"
    export_dir.mkdir(exist_ok=True)
    return export_dir

def connect_main_db():
    """Connect to the main vocabulary database."""
    db_path = Path(__file__).parent.parent / "vocab.db"
    if not db_path.exists():
        print(f"Main database not found at {db_path}")
        return None
    return sqlite3.connect(db_path)

def export_by_batches(conn, export_dir, batch_size=500):
    """Export vocabulary in batches of specified size."""
    cursor = conn.cursor()
    
    # Get total count
    cursor.execute("SELECT COUNT(*) FROM words")
    total_words = cursor.fetchone()[0]
    
    print(f"Exporting {total_words} words in batches of {batch_size}...")
    
    num_batches = (total_words + batch_size - 1) // batch_size
    
    for i in range(num_batches):
        start = i * batch_size
        batch_num = i + 1
        start_word_num = start + 1
        end_word_num = min(start + batch_size, total_words)
        
        # Export this batch
        cursor.execute("""
            SELECT 
                w.lemma as word,
                w.display as display_form,
                w.pos as part_of_speech,
                w.difficulty_band as difficulty,
                w.frequency_rank,
                s.source_name as source,
                w.created_at
            FROM words w 
            LEFT JOIN sources s ON w.first_seen_source_id = s.id
            ORDER BY w.lemma
            LIMIT ? OFFSET ?
        """, (batch_size, start))
        
        filename = f"Main_Database_Words_{start_word_num:04d}-{end_word_num:04d}_Batch{batch_num:02d}.csv"
        filepath = export_dir / filename
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            # Write CSV header
            f.write("word,display_form,part_of_speech,difficulty,frequency_rank,source,created_at\n")
            
            # Write data rows
            for row in cursor.fetchall():
                # Escape quotes and handle None values
                escaped_row = []
                for item in row:
                    if item is None:
                        escaped_row.append('')
                    elif '"' in str(item):
                        escaped_row.append(f'"{str(item).replace('"', '""')}"')
                    else:
                        escaped_row.append(str(item))
                f.write(','.join(escaped_row) + '\n')
        
        print(f"Created {filename}: words {start_word_num}-{end_word_num}")

def export_by_difficulty(conn, export_dir):
    """Export vocabulary organized by difficulty bands."""
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT difficulty_band FROM words WHERE difficulty_band IS NOT NULL ORDER BY difficulty_band")
    difficulties = cursor.fetchall()
    
    print(f"Exporting by difficulty levels...")
    
    for (difficulty,) in difficulties:
        cursor.execute("""
            SELECT 
                w.lemma as word,
                w.display as display_form,
                w.pos as part_of_speech,
                w.frequency_rank,
                s.source_name as source
            FROM words w 
            LEFT JOIN sources s ON w.first_seen_source_id = s.id
            WHERE w.difficulty_band = ?
            ORDER BY w.lemma
        """, (difficulty,))
        
        results = cursor.fetchall()
        filename = f"Main_Database_Difficulty_{difficulty.replace(' ', '_')}_Words.csv"
        filepath = export_dir / filename
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            f.write("word,display_form,part_of_speech,frequency_rank,source\n")
            
            for row in results:
                escaped_row = []
                for item in row:
                    if item is None:
                        escaped_row.append('')
                    elif '"' in str(item):
                        escaped_row.append(f'"{str(item).replace('"', '""')}"')
                    else:
                        escaped_row.append(str(item))
                f.write(','.join(escaped_row) + '\n')
        
        print(f"Created {filename}: {len(results)} words")

def export_by_source(conn, export_dir):
    """Export vocabulary organized by source."""
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT s.source_name, COUNT(w.id) as word_count 
        FROM words w 
        LEFT JOIN sources s ON w.first_seen_source_id = s.id
        GROUP BY s.source_name 
        ORDER BY word_count DESC
    """)
    
    sources = cursor.fetchall()
    print(f"Exporting by sources...")
    
    for source_name, word_count in sources:
        if source_name is None:
            source_name = "Unknown_Source"
            safe_name = "Unknown_Source"
        else:
            safe_name = source_name.replace('.', '_').replace(' ', '_').replace('(', '').replace(')', '')
        
        cursor.execute("""
            SELECT 
                w.lemma as word,
                w.display as display_form,
                w.pos as part_of_speech,
                w.difficulty_band as difficulty,
                w.frequency_rank
            FROM words w 
            LEFT JOIN sources s ON w.first_seen_source_id = s.id
            WHERE s.source_name = ? OR (s.source_name IS NULL AND ? = 'Unknown_Source')
            ORDER BY w.lemma
        """, (source_name if source_name != "Unknown_Source" else None, source_name))
        
        results = cursor.fetchall()
        filename = f"Main_Database_Source_{safe_name}_{len(results)}_words.csv"
        filepath = export_dir / filename
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            f.write("word,display_form,part_of_speech,difficulty,frequency_rank\n")
            
            for row in results:
                escaped_row = []
                for item in row:
                    if item is None:
                        escaped_row.append('')
                    elif '"' in str(item):
                        escaped_row.append(f'"{str(item).replace('"', '""')}"')
                    else:
                        escaped_row.append(str(item))
                f.write(','.join(escaped_row) + '\n')
        
        print(f"Created {filename}: {len(results)} words from {source_name}")

def export_complete_database(conn, export_dir):
    """Export the complete database in one file."""
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            w.lemma as word,
            w.display as display_form,
            w.pos as part_of_speech,
            w.difficulty_band as difficulty,
            w.frequency_rank,
            s.source_name as source,
            w.created_at,
            w.updated_at
        FROM words w 
        LEFT JOIN sources s ON w.first_seen_source_id = s.id
        ORDER BY w.lemma
    """)
    
    filepath = export_dir / "Main_Database_Complete_All_Words.csv"
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        f.write("word,display_form,part_of_speech,difficulty,frequency_rank,source,created_at,updated_at\n")
        
        count = 0
        for row in cursor.fetchall():
            escaped_row = []
            for item in row:
                if item is None:
                    escaped_row.append('')
                elif '"' in str(item):
                    escaped_row.append(f'"{str(item).replace('"', '""')}"')
                else:
                    escaped_row.append(str(item))
            f.write(','.join(escaped_row) + '\n')
            count += 1
    
    print(f"Created Main_Database_Complete_All_Words.csv: {count} words")

def create_summary_report(conn, export_dir):
    """Create a summary report of the database contents."""
    cursor = conn.cursor()
    
    # Get total count
    cursor.execute("SELECT COUNT(*) FROM words")
    total_words = cursor.fetchone()[0]
    
    # Get difficulty distribution
    cursor.execute("SELECT difficulty_band, COUNT(*) FROM words GROUP BY difficulty_band ORDER BY COUNT(*) DESC")
    difficulty_dist = cursor.fetchall()
    
    # Get source distribution
    cursor.execute("""
        SELECT COALESCE(s.source_name, 'Unknown') as source, COUNT(*) 
        FROM words w 
        LEFT JOIN sources s ON w.first_seen_source_id = s.id
        GROUP BY s.source_name 
        ORDER BY COUNT(*) DESC
    """)
    source_dist = cursor.fetchall()
    
    # Get POS distribution
    cursor.execute("SELECT pos, COUNT(*) FROM words WHERE pos IS NOT NULL GROUP BY pos ORDER BY COUNT(*) DESC")
    pos_dist = cursor.fetchall()
    
    # Create summary report
    report_path = export_dir / "MAIN_DATABASE_SUMMARY.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 📊 Main Vocabulary Database Export Summary\n\n")
        f.write(f"**Total Words**: {total_words:,}\n")
        f.write(f"**Export Date**: {Path(__file__).stat().st_mtime}\n\n")
        
        f.write("## 📈 Distribution by Difficulty\n\n")
        for difficulty, count in difficulty_dist:
            difficulty_name = difficulty if difficulty else "Unspecified"
            f.write(f"- **{difficulty_name}**: {count:,} words ({count/total_words*100:.1f}%)\n")
        
        f.write("\n## 📚 Distribution by Source\n\n")
        for source, count in source_dist:
            f.write(f"- **{source}**: {count:,} words ({count/total_words*100:.1f}%)\n")
        
        f.write("\n## 🔤 Distribution by Part of Speech\n\n")
        for pos, count in pos_dist:
            f.write(f"- **{pos}**: {count:,} words ({count/total_words*100:.1f}%)\n")
        
        f.write(f"\n## 📁 Export Files Created\n\n")
        f.write("### Complete Database\n")
        f.write("- `Main_Database_Complete_All_Words.csv` - All words with complete data\n\n")
        
        f.write("### 500-Word Batches\n")
        num_batches = (total_words + 499) // 500
        for i in range(num_batches):
            start = i * 500 + 1
            end = min((i + 1) * 500, total_words)
            f.write(f"- `Main_Database_Words_{start:04d}-{end:04d}_Batch{i+1:02d}.csv`\n")
        
        f.write("\n### By Difficulty Level\n")
        for difficulty, count in difficulty_dist:
            difficulty_name = difficulty.replace(' ', '_') if difficulty else "Unspecified"
            f.write(f"- `Main_Database_Difficulty_{difficulty_name}_Words.csv` - {count:,} words\n")
        
        f.write("\n### By Source\n")
        for source, count in source_dist:
            safe_name = source.replace('.', '_').replace(' ', '_').replace('(', '').replace(')', '') if source else "Unknown_Source"
            f.write(f"- `Main_Database_Source_{safe_name}_{count}_words.csv` - {count:,} words\n")
    
    print(f"Created MAIN_DATABASE_SUMMARY.md")

def main():
    """Main export function."""
    print("=" * 60)
    print("🎓 MAIN VOCABULARY DATABASE EXPORTER")
    print("=" * 60)
    
    # Create export directory
    export_dir = create_export_directory()
    print(f"Export directory: {export_dir}")
    
    # Connect to database
    conn = connect_main_db()
    if not conn:
        return
    
    try:
        # Export complete database
        print("\n1. Exporting complete database...")
        export_complete_database(conn, export_dir)
        
        # Export in 500-word batches
        print("\n2. Exporting in 500-word batches...")
        export_by_batches(conn, export_dir, 500)
        
        # Export by difficulty
        print("\n3. Exporting by difficulty levels...")
        export_by_difficulty(conn, export_dir)
        
        # Export by source
        print("\n4. Exporting by source...")
        export_by_source(conn, export_dir)
        
        # Create summary report
        print("\n5. Creating summary report...")
        create_summary_report(conn, export_dir)
        
        print(f"\n✅ Export complete! Files saved to: {export_dir}")
        print(f"📊 Check MAIN_DATABASE_SUMMARY.md for details")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()
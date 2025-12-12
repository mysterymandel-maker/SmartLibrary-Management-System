import psycopg2
from database.db_connection import get_connection, release_connection
import hashlib
from datetime import datetime, timedelta

def seed_data():
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        print("Seeding database with sample data...")
        
        # 1. Add sample books
        books = [
            ("To Kill a Mockingbird", "Harper Lee", "978-0061120084", 3),
            ("1984", "George Orwell", "978-0451524935", 5),
            ("Pride and Prejudice", "Jane Austen", "978-0141439518", 2),
            ("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565", 4),
            ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "978-0590353427", 6),
            ("The Hobbit", "J.R.R. Tolkien", "978-0547928227", 3),
            ("The Catcher in the Rye", "J.D. Salinger", "978-0316769488", 2),
            ("The Lord of the Rings", "J.R.R. Tolkien", "978-0544003415", 4),
            ("Animal Farm", "George Orwell", "978-0451526342", 3),
            ("Brave New World", "Aldous Huxley", "978-0060850524", 2),
            ("The Chronicles of Narnia", "C.S. Lewis", "978-0066238500", 3),
            ("Fahrenheit 451", "Ray Bradbury", "978-1451673319", 2),
            ("The Hunger Games", "Suzanne Collins", "978-0439023528", 5),
            ("Divergent", "Veronica Roth", "978-0062024039", 4),
            ("The Fault in Our Stars", "John Green", "978-0142424179", 3),
            ("Ark", "Francis Sillah","978-0726957431", 7),
        ]
        
        for title, author, isbn, copies in books:
            cur.execute(
                "INSERT INTO books (title, author, isbn, available_copies, total_copies) VALUES (%s, %s, %s, %s, %s)",
                (title, author, isbn, copies, copies)
            )
        print(f"Added {len(books)} books")
        
        # 2. Add sample members
        members = [
            ("alice", "member"),
            ("bob", "member"),
            ("charlie", "member"),
            ("diana", "member"),
            ("eve", "member"),
            ("frank", "librarian"),
        ]
        
        for username, role in members:
            pw_hash = hashlib.sha256(username.encode()).hexdigest()
            cur.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                (username, pw_hash, role)
            )
        print(f"Added {len(members)} users")
        
        # Get user IDs for later use
        cur.execute("SELECT id, username FROM users WHERE username IN ('alice', 'bob', 'charlie', 'diana', 'eve', 'admin')")
        users = {row[1]: row[0] for row in cur.fetchall()}
        
        # Get book IDs
        cur.execute("SELECT id, title FROM books")
        book_ids = [row[0] for row in cur.fetchall()]
        
        # 3. Add sample book clubs
        clubs = [
            ("Classic Literature Club", "Discussing timeless classics", users.get('admin', 1)),
            ("Sci-Fi Enthusiasts", "Exploring science fiction worlds", users.get('alice', 2)),
            ("Young Adult Readers", "Modern YA fiction discussion", users.get('bob', 3)),
            ("Fantasy Realm", "Epic fantasy adventures", users.get('charlie', 4)),
        ]
        
        club_ids = []
        for name, desc, owner_id in clubs:
            cur.execute(
                "INSERT INTO book_clubs (name, description, created_by) VALUES (%s, %s, %s) RETURNING id",
                (name, desc, owner_id)
            )
            club_id = cur.fetchone()[0]
            club_ids.append(club_id)
            
            # Add creator as member
            cur.execute(
                "INSERT INTO club_members (club_id, user_id) VALUES (%s, %s)",
                (club_id, owner_id)
            )
        
        # Add more members to clubs
        if 'alice' in users and len(club_ids) > 0:
            cur.execute("INSERT INTO club_members (club_id, user_id) VALUES (%s, %s)", (club_ids[0], users['alice']))
        if 'bob' in users and len(club_ids) > 1:
            cur.execute("INSERT INTO club_members (club_id, user_id) VALUES (%s, %s)", (club_ids[1], users['bob']))
        if 'charlie' in users and len(club_ids) > 2:
            cur.execute("INSERT INTO club_members (club_id, user_id) VALUES (%s, %s)", (club_ids[2], users['charlie']))
        if 'diana' in users and len(club_ids) > 0:
            cur.execute("INSERT INTO club_members (club_id, user_id) VALUES (%s, %s)", (club_ids[0], users['diana']))
            
        print(f"Added {len(clubs)} book clubs with members")
        
        # 4. Add sample loan history (some active, some returned)
        loans = [
            # Active loans
            (users.get('alice', 2), book_ids[0], datetime.now().date(), (datetime.now() + timedelta(days=7)).date(), None, 'borrowed'),
            (users.get('alice', 2), book_ids[1], datetime.now().date(), (datetime.now() + timedelta(days=7)).date(), None, 'borrowed'),
            (users.get('bob', 3), book_ids[4], datetime.now().date(), (datetime.now() + timedelta(days=7)).date(), None, 'borrowed'),
            (users.get('charlie', 4), book_ids[5], datetime.now().date(), (datetime.now() + timedelta(days=7)).date(), None, 'borrowed'),
            
            # Returned loans (for statistics)
            (users.get('alice', 2), book_ids[2], (datetime.now() - timedelta(days=20)).date(), (datetime.now() - timedelta(days=13)).date(), (datetime.now() - timedelta(days=15)).date(), 'returned'),
            (users.get('bob', 3), book_ids[1], (datetime.now() - timedelta(days=15)).date(), (datetime.now() - timedelta(days=8)).date(), (datetime.now() - timedelta(days=10)).date(), 'returned'),
            (users.get('charlie', 4), book_ids[1], (datetime.now() - timedelta(days=10)).date(), (datetime.now() - timedelta(days=3)).date(), (datetime.now() - timedelta(days=5)).date(), 'returned'),
            (users.get('diana', 5), book_ids[4], (datetime.now() - timedelta(days=25)).date(), (datetime.now() - timedelta(days=18)).date(), (datetime.now() - timedelta(days=20)).date(), 'returned'),
            (users.get('eve', 6), book_ids[4], (datetime.now() - timedelta(days=30)).date(), (datetime.now() - timedelta(days=23)).date(), (datetime.now() - timedelta(days=25)).date(), 'returned'),
        ]
        
        for user_id, book_id, borrow_date, due_date, return_date, status in loans:
            cur.execute(
                "INSERT INTO loans (user_id, book_id, borrow_date, due_date, return_date, status) VALUES (%s, %s, %s, %s, %s, %s)",
                (user_id, book_id, borrow_date, due_date, return_date, status)
            )
            
            # Update book availability for active loans
            if status == 'borrowed':
                cur.execute("UPDATE books SET available_copies = available_copies - 1 WHERE id = %s", (book_id,))
        
        print(f"Added {len(loans)} loan records")
        
        conn.commit()
        cur.close()
        
        print("\nDatabase seeded successfully!")
        print("\nSample user credentials (password = username):")
        print("  - alice / alice (member)")
        print("  - bob / bob (member)")
        print("  - charlie / charlie (member)")
        print("  - diana / diana (member)")
        print("  - eve / eve (member)")
        print("  - frank / frank (librarian)")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error seeding database: {error}")
    finally:
        if conn:
            release_connection(conn)

if __name__ == "__main__":
    seed_data()

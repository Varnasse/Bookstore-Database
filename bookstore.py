import sqlite3

connect = sqlite3.connect('ebookstore.db')
c = connect.cursor()

# Create the books table
c.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER,
    Title TEXT,
    Author TEXT,
    Qty INTEGER
)
""")
connect.commit()

# Insert sample data into the books table
c.execute("""
INSERT INTO books (id, Title, Author, Qty)
VALUES
    (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
    (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
    (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
    (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
    (3005, 'Alice In Wonderland', 'Lewis Carroll', 12)
""")

# Commit the changes
connect.commit()

# Main menu for the user
def main_menu():
    print("Ebookstore Database" + "\n")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("0. Exit")
    choice = int(input("Enter your choice: "))
    return choice

# Function to enter a book
def enter_book(c, connect):
    id = int(input("Enter the ID: "))
    
    # Check to ensure the ID is not already in use
    c.execute("SELECT id FROM books WHERE id=?", (id,))
    if c.fetchone() is not None:
        print("The ID you entered already exists in the database." + "\n")
        return
    
    # Ask the user to enter book details
    title = input("Enter the title: ")
    author = input("Enter the author: ")
    qty = int(input("Enter the quantity: "))

    # Add it to the table
    c.execute("""
    INSERT INTO books (id, Title, Author, Qty)
    VALUES (?,?,?,?)
    """, (id, title, author, qty))
    connect.commit()
    print("Book has been entered successfully." + "\n")

# Function to update a book
def update_book(c, connect):
    id = int(input("Enter the ID of the book to update: "))
    
    # Check to ensure the ID exists in the table
    c.execute("SELECT id FROM books WHERE id=?", (id,))
    if c.fetchone() is None:
        print("The ID you entered doesn't exist in the database.")
        return

    # Allow the user to update the quantity of books available
    qty = int(input("Enter the new quantity: "))
    c.execute("""
    UPDATE books
    SET Qty = ?
    WHERE id = ?
    """, (qty, id))
    connect.commit()
    print("Book has been updated successfully."+"\n")

# Function to delete a book
def delete_book(c, connect):
    id = int(input("Enter the ID of the book to delete: "))

    # Check to ensure the ID exists in the table
    c.execute("SELECT id FROM books WHERE id=?", (id,))
    if c.fetchone() is None:
        print("The ID you entered doesn't exist in the database." + "\n")
        return

    # Delete the specified ID from the table
    c.execute("""
    DELETE FROM books
    WHERE id = ?
    """, (id,))
    connect.commit()
    print("Book has been deleted successfully." + "\n")

# Function to search for a book
def search_books(c):
    search_term = input("Enter the search term: ")

    # Using the DISTINCT keyword to ensure it returns only unique rows:
    c.execute("""
    SELECT DISTINCT * FROM books
    WHERE Title LIKE ? OR Author LIKE ?
    """, ('%' + search_term + '%', '%' + search_term + '%'))

    # Print the results to the user
    results = c.fetchall()
    for result in results:
        print("ID: " + str(result[0]) + "\n" "Title: " + result[1] + "\n" + "Author: " + result[2] + "\n" + "Qty: " + str(result[3]))

# Connect to the database (creates the file if it doesn't exist)
connect = sqlite3.connect("ebookstore.db")

# Create a cursor object
c = connect.cursor()

# Show the main menu and handle the user's choice
choice = None
while choice != 0:
    choice = main_menu()
    if choice == 1:
        enter_book(c, connect)
    elif choice == 2:
        update_book(c, connect)
    elif choice == 3:
        delete_book(c, connect)
    elif choice == 4:
        search_books(c)

# Close the connection
connect.close()
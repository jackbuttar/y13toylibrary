from flask import Flask, render_template, redirect, flash, url_for, request, g
import sqlite3   #for the database stuff

app = Flask(__name__)

#the path and filename for the database
DATABASE = "C:\\Users\\Jack\\Documents\\91903 - Website and Database Assessment\\toylibrary\\toyLibraryDatabase.db"

#cool function to automatcally connect and query
def get_db():
    db = sqlite3.connect(DATABASE)
    return db

#routes go here

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/toys_public')
def toys_public():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Items")
    results = cursor.fetchall()
    return render_template('toys_public.html',results=results)

@app.route('/toys_admin')
def toys_admin():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Items")
    results = cursor.fetchall()
    return render_template('toys_admin.html',results=results)

@app.route('/admin_login', methods=('GET', 'POST'))
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        code = request.form['code']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = ? AND Code = ? AND Password = ?',
                       (username, code, password))
        admin = cursor.fetchone()

        if admin:
            # Successful login
            # You might want to set up a session here
            return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard or home page
        else:
            flash('Invalid credentials. Please try again.')

    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')  # Create an admin_dashboard.html template

@app.route('/members')
def members():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Members")
    results = cursor.fetchall()
    return render_template('members.html',results=results)

@app.route('/rentals')
def rentals():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Rentals")
    results = cursor.fetchall()
    return render_template('rentals.html',results=results)

@app.route('/member_search', methods=('GET', 'POST'))
def member_search():
    if request.method == 'POST':
        member = request.form['member']
        search_term = '%'+member+'%'
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Members WHERE Name LIKE ?',[search_term])
        results = cursor.fetchall()
        return render_template('members.html', results=results, member=member)
    return render_template('search.html')

@app.route('/on_rent')
def on_rent():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT Items.item_id, items.Item, items.Type, items.[Purchase Price] FROM Items JOIN rentals ON rentals.Item_ID = items.Item_ID WHERE rentals.[Returned Date] IS NULL")
    results = cursor.fetchall()
    return render_template('on_rent.html',results=results)

@app.route('/oneyear_members')
def oneyear_members():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT Members.Name, Members.[Membership Period] FROM Members WHERE Members.[Membership Period] = '1Y'")
    results = cursor.fetchall()
    return render_template('oneyear_members.html',results=results)

@app.route('/sixmonth_members')
def sixmonth_members():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT Members.Name, Members.[Membership Period] FROM Members WHERE Members.[Membership Period] = '6M'")
    results = cursor.fetchall()
    return render_template('sixmonth_members.html',results=results)

@app.route('/new_item', methods=('GET', 'POST'))
def new_item():
    if request.method == 'POST':
        item = request.form["item"]
        type = request.form['type']
        purchase_price = request.form['purchasePrice']  # changed variable name for consistency

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                'INSERT INTO items (item, type, [Purchase Price]) VALUES (?, ?, ?);',
                (item, type, purchase_price)
            )
            db.commit()  # commit the transaction
        except Exception as e:
            db.rollback()  # rollback if there's an error
            # You might want to log the error or flash a message here
            print(f"Error inserting item: {e}")

        return redirect('http://127.0.0.1:8080/toys_admin')  # Redirect to a view after insertion

    return render_template('new_item.html')

@app.route('/new_member', methods=('GET', 'POST'))
def new_member():
    if request.method == 'POST':
        name = request.form["name"]
        address = request.form["address"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        date_joined = request.form["date_joined"]
        membership_period = request.form["membership_period"]
        amount_owed = request.form["amount_owed"]  # New field

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                '''
                INSERT INTO members (name, address, email, [phone number], [date joined], [membership period], [amount owed]) 
                VALUES (?, ?, ?, ?, ?, ?, ?);
                ''',
                (name, address, email, phone_number, date_joined, membership_period, amount_owed)
            )
            db.commit()  # commit the transaction
        except Exception as e:
            db.rollback()  # rollback if there's an error
            print(f"Error inserting member: {e}")

        return redirect('http://127.0.0.1:8080/members')  # Redirect to a view after insertion

    return render_template('new_member.html')

@app.route('/new_rental', methods=('GET', 'POST'))
def new_rental():
    if request.method == 'POST':
        item_id = request.form["item_id"]
        member_id = request.form["member_id"]
        rental_date = request.form["rental_date"]
        returned_date = request.form["returned_date"]
        rental_cost = request.form["rental_cost"]
        late_fee = request.form["late_fee"]

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                '''
                INSERT INTO rentals (Item_ID, Member_ID, [Rental Date], [Returned Date], [Rental Cost], [Late Fee]) 
                VALUES (?, ?, ?, ?, ?, ?);
                ''',
                (item_id, member_id, rental_date, returned_date, rental_cost, late_fee)
            )
            db.commit()  # commit the transaction
        except Exception as e:
            db.rollback()  # rollback if there's an error
            print(f"Error inserting rental: {e}")

        return redirect('http://127.0.0.1:8080/rentals')  # Redirect to a view after insertion

    return render_template('new_rental.html')

@app.route('/search_rental', methods=('GET', 'POST'))
def search_rental():
    if request.method == 'POST':
        rental_id = request.form["rental_id"]
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM rentals WHERE Rental_ID = ?', (rental_id,))
        rental = cursor.fetchone()

        if rental is None:
            return "Rental not found", 404

        return redirect(url_for('edit_rental', rental_id=rental_id))  # Redirect to edit route with rental_id

    return render_template('search_rental.html')

@app.route('/edit_rental/<int:rental_id>', methods=('GET', 'POST'))
def edit_rental(rental_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Get updated data from the form
        item_id = request.form["item_id"]
        member_id = request.form["member_id"]
        rental_date = request.form["rental_date"]
        returned_date = request.form["returned_date"]
        rental_cost = request.form["rental_cost"]
        late_fee = request.form["late_fee"]

        try:
            # Update the rental entry in the database
            cursor.execute(
                '''
                UPDATE rentals 
                SET Item_ID = ?, Member_ID = ?, [Rental Date] = ?, [Returned Date] = ?, [Rental Cost] = ?, [Late Fee] = ? 
                WHERE Rental_ID = ?;
                ''',
                (item_id, member_id, rental_date, returned_date, rental_cost, late_fee, rental_id)
            )
            db.commit()  # commit the transaction
            return redirect('http://127.0.0.1:8080/rentals')  # Redirect to a view after update
        except Exception as e:
            db.rollback()  # rollback if there's an error
            print(f"Error updating rental: {e}")

    # If GET request, fetch the current rental data
    cursor.execute('SELECT * FROM rentals WHERE Rental_ID = ?', (rental_id,))
    rental = cursor.fetchone()

    # Check if rental exists
    if rental is None:
        return "Rental not found", 404

    # Pass rental data to the template for pre-filling the form
    return render_template('edit_rental.html', rental=rental)

@app.route('/delete_item', methods=('GET', 'POST'))
def delete_item():
    if request.method == 'POST':
        item_id = request.form["item_id"]
        
        db = get_db()
        cursor = db.cursor()
        
        # Check if the item exists before attempting to delete
        cursor.execute('SELECT * FROM items WHERE Item_ID = ?', (item_id,))
        item = cursor.fetchone()

        if item is None:
            return "Item not found", 404

        try:
            # Delete the item from the database
            cursor.execute('DELETE FROM items WHERE Item_ID = ?', (item_id,))
            db.commit()  # Commit the transaction
            return redirect('http://127.0.0.1:8080/toys_public')  # Redirect to a view after deletion
        except Exception as e:
            db.rollback()  # Rollback if there's an error
            print(f"Error deleting item: {e}")

    return render_template('delete_item.html')  # Render delete_item.html for GET requests

@app.route('/search_member', methods=('GET', 'POST'))
def search_member():
    if request.method == 'POST':
        member_id = request.form["member_id"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM members WHERE Member_ID = ?', (member_id,))
        member = cursor.fetchone()

        if member is None:
            return "Member not found", 404

        return redirect(url_for('edit_member', member_id=member_id))  # Redirect to edit route with member_id

    return render_template('search_member.html')

@app.route('/edit_member/<int:member_id>', methods=('GET', 'POST'))
def edit_member(member_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Get the updated Amount Owed from the form
        amount_owed = request.form["amount_owed"]

        try:
            # Update the [Amount Owed] in the members table
            cursor.execute(
                '''
                UPDATE members 
                SET [Amount Owed] = ? 
                WHERE Member_ID = ?;
                ''',
                (amount_owed, member_id)
            )
            db.commit()  # Commit the transaction
            return redirect('http://127.0.0.1:8080/members')  # Redirect to a view after update
        except Exception as e:
            db.rollback()  # Rollback if there's an error
            print(f"Error updating member: {e}")

    # If GET request, fetch the current member data
    cursor.execute('SELECT * FROM members WHERE Member_ID = ?', (member_id,))
    member = cursor.fetchone()

    # Check if member exists
    if member is None:
        return "Member not found", 404

    # Pass member data to the template for pre-filling the form
    return render_template('edit_member.html', member=member)

#this bit of code runs the app that we just made with debug on
if __name__ == "__main__":
    app.run(port=8080, debug=True)
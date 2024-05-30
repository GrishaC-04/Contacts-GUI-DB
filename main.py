from sqlite3 import *
from tkinter import *
from tkinter import messagebox

def dbSetup():
    conn = connect('contactsDB.db')
    crsr =  conn.cursor()
    crsr.execute('''
             CREATE TABLE IF NOT EXISTS contacts (
             contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
             first_name TEXT NOT NULL,
             last_name TEXT,
             email TEXT,
             phone_number TEXT NOT NULL,
             address TEXT   
             )
            ''')
    conn.commit()
    conn.close()

def clear():
    first_name_entry.delete(0,END)
    last_name_entry.delete(0,END)
    email_entry.delete(0,END)
    phone_number_entry.delete(0,END)
    address_entry.delete(0,END)

def insertContacts():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()
    phone_number = phone_number_entry.get()
    address = address_entry.get()

    if first_name and phone_number:
        conn = connect('contactsDB.db')
        crsr = conn.cursor()
        crsr.execute('''
                    INSERT INTO contacts (first_name, last_name, email, phone_number, address)
                    VALUES (?,?,?,?,?)
        ''', (first_name, last_name, email, phone_number, address))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Contact Added Successfully")
        clear()
    else:
        messagebox.showwarning("Error", "First Name and the Phone Number are Required Fields")

def showAllContacts():
    top = Toplevel(root)
    listbox = Listbox(top, width=50)
    listbox.pack()
    conn = connect('contactsDB.db')
    crsr =  conn.cursor()
    crsr.execute('SELECT * FROM contacts')
    rows = crsr.fetchall()
    conn.close()
    listbox.delete(0,END)
    for row in rows:
        listbox.insert(END, row)

    def deleteSelected(rows):
        selected_index = listbox.curselection()

        if selected_index:
            selected_contact_id = rows[selected_index[0]][0]

            confirmation = messagebox.askquestion("Confim Delete", "Are you sure?")

            if confirmation == 'yes':
                conn = connect('contactsDB.db')
                crsr =  conn.cursor()
                crsr.execute('DELETE FROM contacts WHERE contact_id=?', (selected_contact_id,))
                conn.commit()
                conn.close()

                listbox.delete(selected_index[0])
                rows = crsr.execute('SELECT * FROM contacts')
                listbox.delete(0,END)
                for row in rows:
                    listbox.insert(END, row)
                messagebox.showinfo("Success", "Contact Deleted Successfully")
        else:
            messagebox.showwarning("Error", "Please Select a contact to delete")
    
    def updateSelected(rows):
        selected_index = listbox.curselection()

        if selected_index:
            pass 

    btn_delete = Button(top, text="Delete Selected", command=lambda: deleteSelected(rows))
    btn_delete.pack(pady=10)

    btn_update = Button(top, text="Update Selected", command=lambda: updateSelected(rows))
    btn_update.pack(pady=10)

    top.pack()



def searchContact():
    top = Toplevel(root)
    top.pack()
    
root = Tk()
root.title('Contacts Manager')

dbSetup()

Label(root, text="First Name").grid(row=0, column=0, padx=10, pady=5)
first_name_entry = Entry(root)
first_name_entry.grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Last Name").grid(row=1, column=0, padx=10, pady=5)
last_name_entry = Entry(root)
last_name_entry.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Email").grid(row=2, column=0, padx=10, pady=5)
email_entry = Entry(root)
email_entry.grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Phone Number").grid(row=3, column=0, padx=10, pady=5)
phone_number_entry = Entry(root)
phone_number_entry.grid(row=3, column=1, padx=10, pady=5)

Label(root, text="Address").grid(row=4, column=0, padx=10, pady=5)
address_entry = Entry(root)
address_entry.grid(row=4, column=1, padx=10, pady=5)

btn_add= Button(root, text="Add Contact", command = insertContacts)
btn_add.grid(row=5, column=0, columnspan=2, pady=10)

btn_show= Button(root, text="Show All Contacts", command = showAllContacts)
btn_show.grid(row=6, column=0, padx=10, pady=10)

btn_search= Button(root, text="Search Contact", command = searchContact)
btn_search.grid(row=6, column=1, padx=10, pady=10)


root.mainloop()
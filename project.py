import difflib
from tkinter import *
import sqlite3
import webbrowser
import folium
from tkinter.messagebox import *

class Mosque:
    def __init__(self):
        self.conn = sqlite3.connect('mosques_database.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS mosques (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            address TEXT,
            coordinates TEXT,
            imam_name TEXT)''')
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def Display(self):
        self.cur.execute('SELECT * FROM mosques')
        return self.cur.fetchall()

    def Search(self, name):
        self.cur.execute('SELECT * FROM mosques WHERE name=?', (name,))
        return self.cur.fetchall()

    def Insert(self, ID, name, type, address, coordinates, imam_name):
        self.cur.execute('INSERT INTO mosques VALUES (?, ?, ?, ?, ?, ?)',
                         (ID, name, type, address, coordinates, imam_name))
        self.conn.commit()

    def Delete(self, ID):
        self.cur.execute('DELETE FROM mosques WHERE id=?', (ID,))
        self.conn.commit()


class App:
    def __init__(self, master):
        self.master = master
        self.mosque = Mosque()

        # Create frames
        self.left_frame = Frame(master)
        self.left_frame.pack(side=LEFT, expand=False, fill=BOTH)

        self.right_frame = Frame(master)
        self.right_frame.pack(side=RIGHT, expand=True, fill=BOTH)

        self.upper_left_frame = Frame(self.left_frame)
        self.upper_left_frame.pack(side=TOP, expand=True, fill=BOTH)

        self.bottom_left_frame = Frame(self.left_frame)
        self.bottom_left_frame.pack(side=BOTTOM, expand=True, fill=BOTH)

        # Create the option menu
        self.Type_label = Label(self.upper_left_frame, text='Type').grid(row=1,column=0, padx=5, pady=5)
        self.Types = ['مسجد', 'جامع', 'أخرى']
        self.selected_type = StringVar()
        self.selected_type.set(self.Types[0])

        self.Type_OptionMenu = OptionMenu(self.upper_left_frame, self.selected_type, *self.Types)
        self.Type_OptionMenu.grid(row=1, column=1, padx=5, pady=5)
        
        # Create variables, labels and entries
        self.ID_label = Label(self.upper_left_frame, text='ID')
        self.ID_label.grid(row=0,column=0, padx=5, pady=5)
        self.ID_entry = Entry(self.upper_left_frame)
        self.ID_entry.grid(row=0, column=1, padx=5, pady=5)

        self.Coordinates_label = Label(self.upper_left_frame, text='Coordinates')
        self.Coordinates_label.grid(row=2,column=0, padx=5, pady=5)
        self.Coordinates_entry = Entry(self.upper_left_frame)
        self.Coordinates_entry.grid(row=2, column=1, padx=5, pady=5)

        self.Name_label = Label(self.upper_left_frame, text='Name')
        self.Name_label.grid(row=0,column=2, padx=5, pady=5)
        self.Name_entry = Entry(self.upper_left_frame)
        self.Name_entry.grid(row=0,column=3, padx=5, pady=5)

        self.Address_label = Label(self.upper_left_frame, text='Address')
        self.Address_label.grid(row=1,column=2, padx=5, pady=5)
        self.Address_entry = Entry(self.upper_left_frame)
        self.Address_entry.grid(row=1,column=3, padx=5, pady=5)

        self.Imam_name_label = Label(self.upper_left_frame, text='Imam_name')
        self.Imam_name_label.grid(row=2,column=2, padx=5, pady=5)
        self.Imam_name_entry = Entry(self.upper_left_frame)
        self.Imam_name_entry.grid(row=2,column=3, padx=5, pady=5)

        # Create buttons
        self.button_frame = Frame(self.bottom_left_frame)
        self.button_frame.pack(expand=True)

        self.Clear_button = Button(self.button_frame, text='Clear', command=self.clear_entries).grid(row=0,column=3, padx=5, pady=5)
        self.DisplayAll = Button(self.button_frame, text='Display All', command=self.display_all).grid(row=0,column=0, padx=5, pady=5)
        self.SearchByName = Button(self.button_frame, text='Search By Name', command=self.searchh).grid(row=0, column=1, padx=5, pady=5)
        self.UpdateEntry = Button(self.button_frame, text='Update Entry', command=self.update_entry).grid(row=0,column=2, padx=5, pady=5)
        self.AddEntry = Button(self.button_frame, text='Add Entry', command=self.add_entry).grid(row=1, column=0, padx=5, pady=5)
        self.DeleteEntry = Button(self.button_frame, text='Delete Entry', command=self.delete_entry).grid(row=1, column=1, padx=5, pady=5)
        self.DisplayOnMap = Button(self.button_frame, text='Display on Map', command=self.display_on_map).grid(row=1,column=2, padx=5, pady=5)
        self.Exit_button = Button(self.button_frame, text='Exit', command=self.master.destroy).grid(row=1,column=3, padx=5, pady=5)

        # Create listbox
        self.Listbox1 = Listbox(self.right_frame)
        self.Listbox1.pack(side=LEFT, expand=True, fill=BOTH)

        # Create scrollbar
        self.scrollbar = Scrollbar(self.right_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.Listbox1.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.Listbox1.yview)

        def update_entries(event):
            selected_record = self.Listbox1.get(ANCHOR)
            self.ID_entry.delete(0, END)
            self.ID_entry.insert(0, selected_record[0])
            self.Name_entry.delete(0, END)
            self.Name_entry.insert(0, selected_record[1])
            self.selected_type.set(selected_record[2])
            self.Address_entry.delete(0, END)
            self.Address_entry.insert(0, selected_record[3])
            self.Coordinates_entry.delete(0, END)
            self.Coordinates_entry.insert(0, selected_record[4])
            self.Imam_name_entry.delete(0, END)
            self.Imam_name_entry.insert(0, selected_record[5])

        self.Listbox1.bind('<<ListboxSelect>>',update_entries)

    def display_all(self):
        self.Listbox1.delete(0, END)
        records = self.mosque.Display()
        if records:
            for record in records:
                self.Listbox1.insert(END, record)
        elif not records:
            showerror(title='No records found', message='No records found in the database.')
    
    def searchh(self):
        self.Listbox1.delete(0, END)
        name = self.Name_entry.get()
        records = self.mosque.Search(name)
        if records:
            for record in records:
                self.Listbox1.insert(END, record)
        else:
            # Use difflib to find close matching names in the database.
            all_names = [record[1] for record in self.mosque.Display()]
            close_matches = difflib.get_close_matches(name, all_names, n=5, cutoff=0.6)
            if close_matches:
                for match in close_matches:
                    self.mosque.cur.execute('SELECT * FROM mosques where name=?', (match,))
                    self.Listbox1.insert(END, self.mosque.cur.fetchone())
            else:
                self.Listbox1.insert(END, f"No record found for '{name}'.")

    def add_entry(self):
        entries = [self.ID_entry.get(), self.Name_entry.get(), self.selected_type.get(), self.Address_entry.get(), self.Coordinates_entry.get(), self.Imam_name_entry.get()]
        
        # check if any entry is empty
        if any(entry == '' for entry in entries):
            showerror('Error', 'Please fill all fields.')
            return
        
        # check if id is a valid integer
        if not self.ID_entry.get().isdigit():
            showerror('Invalid ID', 'ID must be an integer.')
            return

        # check if ID is available
        self.mosque.cur.execute("SELECT id FROM mosques")
        IDs = [x[0] for x in self.mosque.cur.fetchall()]
        if int(self.ID_entry.get()) in IDs:
            showerror('ID exists', 'ID already exists. Please choose another one.')
            return        
        
        self.mosque.Insert(*entries)
        showinfo('Success', 'Record added successfully.')

    def delete_entry(self):
        # check if id entry is empty
        if self.ID_entry.get() == '':
            showerror('Error', 'Please enter an ID.')
            return
        ID = int(self.ID_entry.get())
        # check if ID exists in the database
        if ID not in [x[0] for x in self.mosque.Display()]:
            showerror('ID not found', 'ID not found in the database.')
            return
        self.mosque.Delete(ID)
        showinfo('Success', 'Record deleted successfully.')

    def update_entry(self):
        # check if id entry is empty
        if self.ID_entry.get() == '':
            showerror('Error', 'Please enter an ID to update the record.')
            return
        # check if ID exists
        if int(self.ID_entry.get()) not in [x[0] for x in self.mosque.Display()]:
            showerror('ID not found', 'ID not found in the database.')
            return
        entries = [self.ID_entry.get(), self.Name_entry.get(), self.selected_type.get(), self.Address_entry.get(), self.Coordinates_entry.get(), self.Imam_name_entry.get()]
        self.mosque.cur.execute("UPDATE mosques SET name=?, type=?, address=?, coordinates=?, imam_name=? WHERE id=?", (*entries[1:], entries[0]))
        self.mosque.conn.commit()
        showinfo('Success', 'Record updated successfully.')

    def display_on_map(self):
        # check if coordinates entry is empty
        if self.Coordinates_entry.get() == '':
            showerror('Error', 'Please enter coordinates.')
            return
        coordinates = self.Coordinates_entry.get()
        lat, long = map(float, coordinates.split(','))
        m = folium.Map(location=[lat, long], zoom_start=16)
        folium.Marker(location=[lat, long], popup=self.Name_entry.get()).add_to(m)
        m.save('map.html')
        webbrowser.open('map.html')

    def clear_entries(self):
        self.ID_entry.delete(0, END)
        self.Name_entry.delete(0, END)
        self.selected_type.set(self.Types[0])
        self.Address_entry.delete(0, END)
        self.Coordinates_entry.delete(0, END)
        self.Imam_name_entry.delete(0, END)

if __name__ == '__main__':
    root = Tk()
    root.title(100*' '+ 'Mosques Management System')
    root.geometry('800x200')
    app = App(root)
    root.mainloop()
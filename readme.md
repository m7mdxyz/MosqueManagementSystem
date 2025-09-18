# 🕌 Mosques Management System

A desktop application developed in Python for managing a database of mosques. This project was completed as an assignment for the **CS492** course at the College of Computer, Qassim University, during the 2023 academic year.

**Course Project PDF:** [CS492 Project.pdf](CS492_Project.pdf)

## Project Overview

The system is built with a **Graphical User Interface (GUI)** using **Tkinter** and is connected to a **SQLite** database to store mosque data. The interface is structured into three main parts: input fields (Part 1), a display ListBox (Part 2), and operation buttons (Part 3).

My implementation goes beyond the core requirements by incorporating all the extra features for additional marks, as detailed in the project instructions.

### Core Features (Base Requirements) ✨

  * **Database Integration**: Connects to a `mosques_database.db` file to store and retrieve records from a `mosques` table.
  * **Object-Oriented Design**: Uses a `Mosque` class to handle all database operations, including connecting, displaying all records, searching by name, adding a new entry, and deleting a record.
  * **Standard Operations**:
      * **Display All**: Fetches and shows all mosque records in the ListBox.
      * **Search**: Retrieves a specific record from the database based on the mosque name.
      * **Add Entry**: Inserts a new mosque record into the database.
      * **Delete Entry**: Removes a record from the database using its ID.

### Advanced Features (Extra Marks) 🚀

My project includes the following enhancements, as suggested in the assignment's extra features section:

  * **Update Operation**: Implemented a function to allow users to update an existing mosque record, including its `Imam_name`.
  * **Display on Map**: Integrated **Folium** and **Webbrowser** libraries to visualize a mosque's location on an interactive map using its coordinates.
  * **Enhanced Search**: Improved the search functionality using the **difflib** library to provide a list of close matches if a user enters a misspelled name, enhancing the user experience.

## Technical Details 💻

  * **GUI Framework**: Tkinter 
  * **Database**: SQLite3 
  * **Mapping**: Folium, Webbrowser 
  * **Fuzzy String Matching**: difflib 

## How to Run 🏃‍♂️

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/m7mdxyz/MosqueManagementSystem.git
    cd ./MosqueManagementSystem
    ```
2.  **Install the required libraries:**
    ```bash
    pip install folium
    ```
3.  **Run the application:**
    ```bash
    python project.py
    ```

## File Structure 📂

```
.
├── CS492 Project.pdf     # The original project instructions
├── project.py            # The main application script
├── mosques_database.db   # The SQLite database file (created automatically)
├── map.html              # The generated map file (created when the "Display on Map" button is clicked)
└── README.md             # Project documentation
```
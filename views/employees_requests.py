import sqlite3
import json
from models import Employee
from models.location import Location



EMPLOYEES = [
    {
      "id": 1,
      "animalId": 1,
      "userId": 5
    },
    {
      "id": 2,
      "animalId": 5,
      "userId": 9
    },
    {
      "id": 3,
      "animalId": 3,
      "userId": 2
    },
    {
      "id": 4,
      "animalId": 4,
      "userId": 14
    },
    {
      "id": 5,
      "animalId": 5,
      "userId": 12
    },
    {
      "id": 6,
      "animalId": 6,
      "userId": 7
    },
    {
      "id": 7,
      "animalId": 7,
      "userId": 5
    },
    {
      "id": 8,
      "animalId": 8,
      "userId": 1
    },
    {
      "id": 9,
      "animalId": 9,
      "userId": 11
    },
    {
      "id": 10,
      "animalId": 10,
      "userId": 4
    },
    {
      "id": 11,
      "animalId": 11,
      "userId": 3
    },
    {
      "id": 12,
      "animalId": 3,
      "userId": 14
    }
  ]

def get_all_employees():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id,
            l.name location_name,
            l.address location_address
        FROM employee e
        JOIN location l 
          ON l.id = e.location_id
        """)

        # Initialize an empty list to hold all animal representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            employee = Employee(row['id'], row['name'], row['address'],
                            row['location_id'])
            location = Location(row['id'], row['location_name'], row['location_address'])

            employees.append(employee.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(employees)


def get_single_employee(id):
  
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        employee = Employee(data['id'], data['name'], data['address'],
                           data['location_id'])
                          

        return json.dumps(employee.__dict__)


def save_employee(new_employee):
    
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
                INSERT INTO Employee
            ( name, address, location_id )
             VALUES
            ( ?, ?, ? );
        """,(new_employee['name'], new_employee['address'],
              new_employee['location_id'],
             ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
         # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_employee['id'] = id


        return json.dumps(new_employee)

def delete_employee(id):
    # Initial -1 value for animal index, in case one isn't found
    employee_index = -1

    # Iterate the ANIMALS list, but use enumerate() so that you
    # can access the index value of each item
    for index, animal in enumerate(EMPLOYEES):
        if animal["id"] == id:
            # Found the animal. Store the current index.
            employee_index = index

    # If the animal was found, use pop(int) to remove it from list
    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)
        
def update_employee(id, new_employee):
    # Iterate the employeeS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the employee. Update the value.
            EMPLOYEES[index] = new_employee
            break

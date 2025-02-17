import csv
import os
import random
from datetime import datetime

# Define the set of seats (1A - 34A) and show available seats
# Generates seat labels from 1A to 34C (max 100 seats) and adds them to available seats
seats = [f"{num}{letter}" for num in range (1,35) for letter in 'ABC'][:100]
available_seats = set(seats)

# Load existing bookings from file
def load_bookings():
    if os.path.exists('booking_records.csv'):
        with open('booking_records.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                seat = row[2]
                if seat in available_seats:
                    available_seats.remove(seat)

# Call load_bookings function to update available_seats   
load_bookings()

# Function to save all bookings back to the CSV file
def save_bookings():
    bookings = []
    if os.path.exists('booking_records.csv'):
        with open('booking_records.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)
            bookings = [row for row in reader]

    # Append new bookings
    with open('booking_records.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Customer ID', 'Extension', 'Seat', 'Booking Time'])
        writer.writerows(bookings)

# Main menu loop
while True:
    menu_options = {
        '1': 'Book ticket',
        '2': 'Cancel ticket',
        '3': 'View available seats',
        '4': 'Update a booking',
        '5': 'Print window seats',
        '6': 'Quit'
    }

    # Display the menu and get the user's input
    intro = input("Welcome! Please select an option from the menu:\n"
                  "1. Book ticket\n"
                  "2. Cancel ticket\n"
                  "3. View available seats\n"
                  "4. Update a booking\n"
                  "5. Print window seats\n"
                  "6. Quit\n"
                  "Enter your choice (1-6): ")
        
    # Validate the user input and execute for corresponding option
    if intro in menu_options:
        print(f"You selected: {menu_options[intro]}")

        # Book ticket option 
        if intro == '1':
            header = ['Customer ID', 'Extension', 'Seat', 'Booking Time']
            
            # Generate a random customer ID
            def customer_id():
                return random.randint(100,999)
    
            # Generate a unique ticket extension
            def ticket_extension():
                while True:
                    ticket_num = random.randint(10000, 99999)
                    if not booking_exists(ticket_num):
                        return ticket_num
            
            # Chexk if a booking with a specific ticket number already exists
            def booking_exists(ticket_num):
                if os.path.exists('booking_records.csv'):
                    with open('booking_records.csv', mode = 'r') as file:
                        reader = csv.reader(file)
                        next(reader)
                        for row in reader:
                            if row[1] == str(ticket_num):
                                return True
                return False

            # Book a ticket   
            def book_ticket():
                if not available_seats:
                    print("No seats available for booking.\n")
                    return
                    
                ticket_num = ticket_extension()
                cust_id = customer_id()
                seat_num = random.choice(list(available_seats))
                booking_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                print(f'Your ticket number is: {cust_id}-{ticket_num}')
                print(f'Your seat is: {seat_num}\n')
                print(f'Booking time: {booking_time}\n')

                # Write booking to the file 
                with open('booking_records.csv', mode = 'a', newline = '') as file:
                        write = csv.writer(file)
                        write.writerow([cust_id, ticket_num, seat_num, booking_time])

                available_seats.remove(seat_num)

            # Create file with header if it doesn't exist   
            try:
                with open('booking_records.csv', mode='x', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(header)
            except FileExistsError:
                pass 
                
            book_ticket()
            print(f"Seats available: {len(available_seats)}\n")
            continue
        
        # Cancel ticket option
        elif intro == '2':
            #Code for ticket cancellation
            def delete_booking(customer_id, extension):
                bookings = []
                file_name = 'booking_records.csv'
                booking_found = False

                if os.path.exists(file_name):
                    with open(file_name, mode = 'r', newline = '') as file:
                        reader = csv.reader(file)
                        header = next(reader)
                        bookings = [row for row in reader]

                    # Find booking to delete
                    bookings_to_keep = []
                    for row in bookings:
                        if row[0] == customer_id and row[1] == extension:
                            booking_found = True
                            available_seats.add(row[2]) # Make seat available again
                            cancellation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            print(f"Ticket {customer_id}-{extension} cancelled at {cancellation_time}.")
                        else:
                            bookings_to_keep.append(row)

                    # Write remaining bookings back into file
                    with open(file_name, mode = 'w', newline = '') as file:
                        writer = csv.writer(file)
                        writer.writerow(header)
                        writer.writerows(bookings_to_keep)

                return booking_found
            
            # Prompt user for ticket ID, repeat if invalid
            while True:
                ticket_id = input("Enter your ticket ID (First 3 digits): \n")
                if len(ticket_id) == 3 and ticket_id.isdigit():
                    break
                print("Invalid input. Please enter a 3-digit number.")

            # Prompt user for ticket extension, repeat if invalid
            while True:
                ticket_extension = input("Enter your ticket extension (Last 5 digits): \n")
                if len(ticket_extension) == 5 and ticket_extension.isdigit():
                    break
                print("Invalid input. Please enter a 5-digit number.")

            # Proceed with cancellation
            if delete_booking(ticket_id, ticket_extension):
                print("Ticket successfully cancelled.\n")
            else:
                print("Ticket not found.\n")

            print(f"Seats available: {len(available_seats)}\n") #Shows seats left after cancellation
            continue
            
        # Shows available seats
        elif intro == '3':
            print(f"Total seats: {len(seats)}")
            print(f"Seats available: {len(available_seats)}")
            continue

        # Update a booking option
        elif intro == '4':
            def update_booking(customer_id, extension):
                bookings = []
                file_name = 'booking_records.csv'
                booking_found = False

                if os.path.exists(file_name):
                    with open(file_name, mode='r', newline='') as file:
                        reader = csv.reader(file)
                        header = next(reader)
                        bookings = [row for row in reader]

                    # Search for the booking
                    for row in bookings:
                        if row[0] == customer_id and row[1] == extension:
                            booking_found = True
                            print(f"Ticket found for Customer ID: {row[0]}")
                            print(f"Ticket Number: {row[0]}-{row[1]}")
                            print(f"Seat Number: {row[2]}")
                            print(f"Booking Time: {row[3]}")
                            break

                return booking_found

            # Prompt user for ticket ID , repeat if invalid
            while True:
                ticket_id = input("Enter your ticket ID (First 3 digits): \n")
                if len(ticket_id) == 3 and ticket_id.isdigit():
                    break
                print("Invalid input. Please enter a 3-digit number.")

            # Prompt user for ticket extension, repeat if invalid
            while True:
                ticket_extension = input("Enter your ticket extension (Last 5 digits): \n")
                if len(ticket_extension) == 5 and ticket_extension.isdigit():
                    break
                print("Invalid input. Please enter a 5-digit number")

            # Call the update_booking function and display result
            if update_booking(ticket_id, ticket_extension):
                print("Booking details displayed above.\n")
            else:
                print("Ticket not found.\n")
            continue
                                     
        # Shows window seats (seats ending in 'A') 
        elif intro == '5':
            booked_window_seats = [seat for seat in seats if seat.endswith('A') and seat not in available_seats]
            if booked_window_seats:
                print("Booked window seats: ")
                for seat in booked_window_seats:
                    print(seat)
            else:
                print("No window seats have been booked")
            continue
        
        # Quit program option
        elif intro == '6':
            save_bookings()
            print("Goodbye!")
        break
    else:
        print("Invalid option, please enter a number between 1 and 6.")

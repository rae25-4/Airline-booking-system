import csv
import os
import random
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog

#Define the set of seats (1A - 34A) and show available seats
seats = [f"{num}{letter}" for num in range (1,35) for letter in 'ABC'][:100]
available_seats = set(seats)# Load existing bookings from file

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
                
load_bookings()

# Creates CSV file if it does not exist
if not os.path.exists('booking_records.csv'):
    with open('booking_records.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Customer ID', 'Ticket Extension', 'Seat', 'Booking Time'])

# Update displayed available seats
def update_available_seats_display():
    available_seats_label.config(text=f"Available Seats: {len(available_seats)}")

# Book ticket function
def book_ticket():
    if not available_seats:
        messagebox.showinfo("Booking", "No seats available for booking.")
        return
    
    cust_id = random.randint(100, 999)
    ticket_num = random.randint(10000, 99999)
    seat_num = random.choice(list(available_seats))
    booking_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open('booking_records.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([cust_id, ticket_num, seat_num, booking_time])

    available_seats.remove(seat_num)
    messagebox.showinfo("Booking Successful", f"Ticket ID: {cust_id}-{ticket_num}\nSeat: {seat_num}\nBooking Time: {booking_time}")
    update_available_seats_display()

# Cancel ticket function
def cancel_ticket():
    # get and validate customer ID (3 digits)
    while True:
        cust_id = simpledialog.askstring("Cancel Ticket", "Enter the 3-digit Customer ID:")
        if cust_id is None:
            return
        if len(cust_id) == 3 and cust_id.isdigit():
            break
        messagebox.showerror("Invalid Input", "Please enter a valid 3-digit Customer ID.")
    
    # Get and validate ticket extension (5 digits)
    while True:
        ticket_num = simpledialog.askstring("Cancel Ticket", "Enter the 5-digit Ticket Extension:")
        if ticket_num is None:
            return
        if len(ticket_num) == 5 and ticket_num.isdigit():
            break
        messagebox.showerror("Invalid Input", "Please enter a valid 5-digit Ticket Extension.")

    # Read bookings and delete the matching booking
    bookings = []
    booking_found = False
    with open('booking_records.csv', mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if row[0] == cust_id and row[1] == ticket_num:
                booking_found = True
                available_seats.add(row[2])
            else:
                bookings.append(row)

    # Rewrite CSV file without cancelled booking
    if booking_found:
        with open('booking_records.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(bookings)
        messagebox.showinfo("Cancel Ticket", "Ticket cancelled successfully.")
    else:
        messagebox.showinfo("Cancel Ticket", "Ticket not found")

    update_available_seats_display()

# Update booking function
def update_booking():
    # Get and validate customer ID (3 digits)
    while True:
        cust_id = simpledialog.askstring("Update Booking", "Enter the 3-digit Customer ID")
        if cust_id is None:
            return
        if len(cust_id) == 3 and cust_id.isdigit():
            break
        messagebox.showerror("Invalid Input", "Please enter a valid 3-digit Customer ID.")

    # Get and validate ticket extension (5 digits)
    while True:
        ticket_num = simpledialog.askstring("Update Booking", "Enter the 5-digit Ticket Extension:")
        if ticket_num is None:
            return
        if len(ticket_num) == 5 and ticket_num.isdigit():
            break
        messagebox.showerror("Invalid Input", "Please enter a valid 5-digit Ticket Extension.")

    # Search for booking
    booking_found = False
    with open('booking_records.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[0] == cust_id and row[1] == ticket_num:
                booking_found = True
                messagebox.showinfo("Booking Details",
                                    f"Customer ID: {row[0]}\n"
                                    f"Ticket Number: {row[0]}-{row[1]}\n"
                                    f"Seat Number: {row[2]}\n"
                                    f"Booking Time:{row[3]}")
                break
        
    if not booking_found:
        messagebox.showinfo("Update Booking", "Ticket not found.")


# View available seats function
def view_available_seats():
    if available_seats:
        available_seats_text = "\n".join(sorted(available_seats))
        messagebox.showinfo("Available Seats", f"Available Seats:\n{available_seats_text}")
    else:
        messagebox.showinfo("Available Seats", "No seats available.")

# View window seats function
def view_window_seats():
    booked_window_seats = []

    with open('booking_records.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            seat_num = row[2]
            if seat_num.endswith('A'):
                booked_window_seats.append(seat_num)

    if booked_window_seats:
        window_seats_text = "\n".join(sorted(booked_window_seats))
        messagebox.showinfo("Booked Window Seats", f"Booked Window Seats:\n{window_seats_text}")
    else:
        messagebox.showinfo("Booked Window Seats", "No window seats have been booked.")

# Quit function
def quit_booking():
    root.quit()

# Step 1: Create the main application window
root = tk.Tk()
root.title("Airline Ticket Reservation")  # Set window title
root.geometry("400x600")  # Set window size

# Step 2: Buttons and labels
book_button = tk.Button(root, text="Book ticket", command=book_ticket)  # Create button
book_button.pack(pady=10)

cancel_button = tk.Button(root, text="Cancel ticket", command=cancel_ticket)  # Create button
cancel_button.pack(pady=10)

available_seat_button = tk.Button(root, text="View available seats", command=view_available_seats)  # Create button
available_seat_button.pack(pady=10)

update_booking_button = tk.Button(root, text="Update a booking", command=update_booking)  # Create button
update_booking_button.pack(pady=10)

window_seat_button = tk.Button(root, text="View window seats", command=view_window_seats)  # Create button
window_seat_button.pack(pady=10)

quit_button = tk.Button(root, text="Quit", command=quit_booking)  # Create button
quit_button.pack(pady=10)

available_seats_label = tk.Label(root, text="")
available_seats_label.pack(pady=20)
update_available_seats_display()

root.mainloop()
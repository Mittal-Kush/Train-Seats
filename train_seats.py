import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize the seat availability database
def init_seats():
    conn = sqlite3.connect('seats.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS seats (id INTEGER PRIMARY KEY, row INTEGER, seat INTEGER, available INTEGER)')
    for i in range(1, 12):
        for j in range(1, 8):
            if i == 11 and j > 3:
                break
            c.execute('INSERT INTO seats (row, seat, available) VALUES (?, ?, 1)', (i, j))
    conn.commit()
    conn.close()

# Book the specified number of seats
def book_seats(num_seats):
    conn = sqlite3.connect('seats.db')
    c = conn.cursor()
    booked_seats = []
    for i in range(1, 12):
        for j in range(1, 8):
            if i == 11 and j > 3:
                break
            c.execute('SELECT available FROM seats WHERE row=? AND seat=?', (i, j))
            if c.fetchone()[0] == 1:
                booked_seats.append((i, j))
                c.execute('UPDATE seats SET available=0 WHERE row=? AND seat=?', (i, j))
                if len(booked_seats) == num_seats:
                    break
        if len(booked_seats) == num_seats:
            break
    conn.commit()
    conn.close()
    return booked_seats

# Get the current seat availability status
def get_seat_availability():
    conn = sqlite3.connect('seats.db')
    c = conn.cursor()
    availability = []
    for i in range(1, 12):
        row_availability = []
        for j in range(1, 8):
            if i == 11 and j > 3:
                break
            c.execute('SELECT available FROM seats WHERE row=? AND seat=?', (i, j))
            row_availability.append(c.fetchone()[0])
        availability.append(row_availability)
    conn.close()
    return availability

def main():
    init_seats()
    app.run(debug=True)

if __name__ == '__main__':
    main()

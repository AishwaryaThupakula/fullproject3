from flask import Flask, render_template, request, redirect
import pymysql as sql

app = Flask(__name__)
my_connection = sql.connect(
    host="",
    root="",
    password="",
    database="project3"
)

my_cursor = my_connection.cursor()

book_table_query = """ 
         create table if not exists bookings(booking_id int primary key auto_increment,booking_date date,seats_req int,contact_email varchar(50)
         ) ;
"""
my_cursor.execute(book_table_query)


@app.route("/",methods=["GET"])
def homepage():
    return render_template("index.html")


@app.route("/book_event", methods =["GET","POST"])
def book_event():
    if request.method == "POST":
       event_id = int(request.form["event_id"])
       booking_date = request.form["booking_date"]
       seats_req = int(request.form["seats"])
       contact_email = request.form["contact_email"]

       get_event_query ="""
                   select max_seats from events where event_id  = %s;
                    """
       values = [event_id]
       my_cursor.execute(get_event_query,values)
       fetched = my_cursor.fetchall()
       
       if not fetched:
          return f"Invalid EventId{event_id}"
       else:
             max_seats = fetched[0][0]
             if seats_req > max_seats:
                    return f"cannot book more than{max_seats}"
             else:
                   
                   insert_query = """ 
                         insert into bookings(event_id,booking_date,seats,contact_email)
                         values (%s,%s,%s,%s);
                   """
                   values = [event_id,booking_date,seats_req,contact_email]
                   my_cursor.execute(insert_query,values)
                   my_connection.commit()
                   return "Booking Successfull"

    return render_template("book_event.html")


app.run(debug=True)
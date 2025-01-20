import time
import smtplib
from email.message import EmailMessage  # Import EmailMessage for creating emails

from datetime import datetime, timedelta
from flask import request
from flask import make_response
from flask_cors import cross_origin
from application.controller.api import *
from io import StringIO
import csv
from flask import render_template
from application.jobs.workers import celery
from datetime import datetime
from flask import current_app as app
from flask_sse import sse
from celery.schedules import crontab
print("crontab ", crontab)
from application.data.models import *


def get_users_with_no_bookings():
    all_users = db.session.query(User).all()
    booked_users = db.session.query(Booking.user_id).distinct()
    users_with_no_bookings = [user for user in all_users if user.id not in [booking.user_id for booking in booked_users]]
    return users_with_no_bookings

@celery.task
def send_email_to_users_with_no_bookings():
    users_with_no_bookings = get_users_with_no_bookings()

    for user in users_with_no_bookings:
        # Generate an email address using the username
        email = f"{user.username}@example.com"  # Replace 'username' with the actual attribute

        subject = 'Reminder: Explore our app!'
        body = 'We noticed that you haven\'t made any bookings yet. Don\'t miss out!'

        # Create an email message
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = 'lalitmach22@example.com'  # Replace with your email address
        msg['To'] = email

        try:
            # Connect to MailHog SMTP server (assuming it runs on localhost and port 1025)
            with smtplib.SMTP('localhost', 1025) as server:
                # Send the email
                server.send_message(msg)
        except Exception as e:
            print(f"Failed to send email to {email}: {str(e)}")

@celery.task
def send_booking_notifications():
    bookings = db.session.query(Booking).all()

    for booking in bookings:
        user = db.session.query(User).get(booking.user_id)
        show = db.session.query(Show).get(booking.show_id)
        venue = db.session.query(Venue).get(booking.venue_id)
        
        if user and show and venue:
            email = f"{user.username}@example.com"
            subject = 'Booking Notification'
            body = f'Your booking for the show "{show.name}" at "{venue.name}" has been confirmed.'

            # Create an email message
            msg = EmailMessage()
            msg.set_content(body)
            msg['Subject'] = subject
            msg['From'] = 'lalitmach22@example.com'  # Replace with your email address
            msg['To'] = email

            try:
                # Connect to MailHog SMTP server (assuming it runs on localhost and port 1025)
                with smtplib.SMTP('localhost', 1025) as server:
                    # Send the email
                    server.send_message(msg)
            except Exception as e:
                print(f"Failed to send email to {user.email}: {str(e)}")

def in_last_month(timestamp):
    current_time = datetime.now()
    last_month_start = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    last_month_end = last_month_start.replace(day=1)
    
    dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')  # Adjust format to match your database
    return last_month_start <= dt <= last_month_end

@celery.task
def generate_booking_report_last_month():
    # Calculate the timestamp range for the last month
    current_time = datetime.now()
    last_month_start = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    last_month_end = last_month_start.replace(day=1)
    
    # Query booking data for the last month
    #bookings = db.session.query(Booking).filter(Booking.timestamp >= last_month_start, Booking.timestamp <= last_month_end).all()
    bookings = db.session.query(Booking).all()
    # Generate the report
    report = []
    for booking in bookings:
        user = db.session.query(User).get(booking.user_id)
        show = db.session.query(Show).get(booking.show_id)
        venue = db.session.query(Venue).get(booking.venue_id)
        ticket_quantity = booking.quantity

        report_entry = {
            "user_name": user.name if user else "Unknown User",  # Replace with actual user field
            "booked_show": show.name if show else "Unknown Show",  # Replace with actual show field
            "booked_venue": venue.name if venue else "Unknown Venue",  # Replace with actual venue field
            "ticket_quantity": ticket_quantity,
        }
        report.append(report_entry)
    return report

@celery.task
def generate_admin_analytical_report():
    # Query booking data
    bookings = db.session.query(
        Booking.show_id,
        Booking.venue_id,
        db.func.sum(Booking.quantity).label("total_quantity")
    ).group_by(Booking.show_id, Booking.venue_id).all()

    # Prepare a report for shows
    show_report = []
    for booking in bookings:
        show = db.session.query(Show).get(booking.show_id)
        show_name = show.name if show else "Unknown Show"
        total_quantity = booking.total_quantity

        show_report_entry = {
            "name": show_name,
            "total_quantity": total_quantity,
        }
        show_report.append(show_report_entry)

    # Prepare a report for venues
    venue_report = []
    for booking in bookings:
        venue = db.session.query(Venue).get(booking.venue_id)
        venue_name = venue.name if venue else "Unknown Venue"
        total_quantity = booking.total_quantity

        venue_report_entry = {
            "name": venue_name,
            "total_quantity": total_quantity,
        }
        venue_report.append(venue_report_entry)

    # Sort reports by total_quantity in decreasing order
    show_report = sorted(show_report, key=lambda x: x["total_quantity"], reverse=True)
    venue_report = sorted(venue_report, key=lambda x: x["total_quantity"], reverse=True)

    return show_report, venue_report

@celery.task
def generate_daily_analytical_report():
    bookings = db.session.query(Booking).all()

    # Generate the daily analytical report
    report = []
    for booking in bookings:
        user = db.session.query(User).get(booking.user_id)
        show = db.session.query(Show).get(booking.show_id)
        venue = db.session.query(Venue).get(booking.venue_id)
        ticket_quantity = booking.quantity

        report_entry = {
            "user_name": user.username if user else "Unknown User",
            "booked_show": show.name if show else "Unknown Show",
            "booked_venue": venue.name if venue else "Unknown Venue",
            "ticket_quantity": ticket_quantity,
        }
        report.append(report_entry)

    # Create a CSV file for the report
    report_csv = "daily_analytical_report.csv"
    with open(report_csv, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["User Name", "Booked Show", "Booked Venue", "Ticket Quantity"])
        for entry in report:
            writer.writerow([entry["user_name"], entry["booked_show"], entry["booked_venue"], entry["ticket_quantity"]])

    # Send the daily report as an email attachment
    subject = 'Daily Analytical Report'
    body = 'Attached is your daily analytical report.'
    recipients = ['admin@example.com']  # Add your recipient's email address

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = 'lalitmach22@example.com'  # Replace with your email address
    msg['To'] = recipients

    with open(report_csv, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename="daily_analytical_report.csv")

    try:
        with smtplib.SMTP('localhost', 1025) as server:
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send daily analytical report: {str(e)}")
    return "HELLO LALIT , CHECKING DAILY EMAIL ANALYTICAL REPORT"

@celery.task
def generate_weekly_analytical_report():
    bookings = db.session.query(Booking).all()

    # Generate the weekly analytical report
    report = []
    for booking in bookings:
        user = db.session.query(User).get(booking.user_id)
        show = db.session.query(Show).get(booking.show_id)
        venue = db.session.query(Venue).get(booking.venue_id)
        ticket_quantity = booking.quantity

        report_entry = {
            "user_name": user.username if user else "Unknown User",
            "booked_show": show.name if show else "Unknown Show",
            "booked_venue": venue.name if venue else "Unknown Venue",
            "ticket_quantity": ticket_quantity,
        }
        report.append(report_entry)

    # Create a CSV file for the report
    report_csv = "weekly_analytical_report.csv"
    with open(report_csv, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["User Name", "Booked Show", "Booked Venue", "Ticket Quantity"])
        for entry in report:
            writer.writerow([entry["user_name"], entry["booked_show"], entry["booked_venue"], entry["ticket_quantity"]])

    # Send the weekly report as an email attachment
    subject = 'Weekly Analytical Report'
    body = 'Attached is your weekly analytical report.'
    recipients = ['admin@example.com']  # Add your recipient's email address

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = 'lalitmach22@example.com'  # Replace with your email address
    msg['To'] = recipients

    with open(report_csv, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename="weekly_analytical_report.csv")

    try:
        with smtplib.SMTP('localhost', 1025) as server:
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send weekly analytical report: {str(e)}")

@celery.task
def just_say_hello():
    print("INSIDE TASK")
    print("Hello Lalit ")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("In tasks, time is " ,dt_string)
    return "HELLO LALIT , WELCOME, TESTING CELERY WORKERS"

# Configure Celery Periodic Tasks
@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Schedule tasks to run periodically
    sender.add_periodic_task(
        crontab(minute=5, hour=11),  # Daily task
        send_email_to_users_with_no_bookings.s(),name = 'Normal Mail'
    )
    sender.add_periodic_task(
        crontab(minute=58, hour=10),  # Daily task
        send_booking_notifications.s(),name = "Booking Notification Mail"
    )
    sender.add_periodic_task(
        crontab(day_of_month=19, hour=11, minute=20),  # Monthly task
        generate_booking_report_last_month.s(),name = "Lalit Mail"
    )
    sender.add_periodic_task(
        crontab(day_of_month=19, hour=11, minute=10),  # Monthly task
        generate_admin_analytical_report.s(),name = 'Seema Mail'
    )
    # sender.add_periodic_task(60.0, just_say_hello.s(), name = " At every 10 seconds Just Hello"
    # )
    # sender.add_periodic_task(60.0, send_email_to_users_with_no_bookings.s(),
    #                          name = " Email At every 30 seconds"
    # )
    # sender.add_periodic_task(60.0, send_booking_notifications.s(),
    #                          name = " Booking Notification At every 60 seconds"
    # )
    # sender.add_periodic_task(30.0,generate_daily_analytical_report.s(),
    #                          name = " Daily Analytical Report At every 60 seconds"
    # )
    sender.add_periodic_task(
        crontab(hour=2, minute=0),  # Daily task at 2:00 AM
        generate_daily_analytical_report.s(),
    )

    # Weekly Analytical Report: Run weekly on a specific day and time (e.g., every Monday at 3 AM)
    sender.add_periodic_task(
        crontab(day_of_week=1, hour=3, minute=0),  # Weekly task on Mondays at 3:00 AM
        generate_weekly_analytical_report.s(),
    )


    

@celery.task
def your_immediate_task():
    # Your task logic here
    print("INSIDE SECOND TASK")
    print("This task is executed immediately.")

@celery.task()
def long_running_task():
    print("STARTED LONG task")
    now = datetime.now()
    print("Time before starting task -" , now)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    sse.publish({"message": "STARTED ="+dt_string }, type='greeting')
    for lp in range(10):
        now1 = datetime.now()
        dt_string = now1.strftime("%d/%m/%Y %H:%M:%S")
        sse.publish({"message": "RUNNING ="+dt_string }, type='greeting')
        print("date and time =", dt_string) 
        time.sleep(1)

    now2 = datetime.now()
    dt_string = now2.strftime("%d/%m/%Y %H:%M:%S")        
    sse.publish({"message": "COMPLETE ="+dt_string }, type='greeting')
    print("COMPLETED LONG RUN")
    



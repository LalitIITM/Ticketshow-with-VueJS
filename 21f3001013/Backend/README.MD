# My SPA App Backend

Welcome to the backend codebase of My SPA 'TICKETSHOW' App. This application is built using Flask, a lightweight web framework, and SQLite for the database. It provides APIs for user registration, login, CRUD operations for shows, venues, and bookings, along with admin-specific functionalities.

## Project Structure

The backend is organized into several modules and folders:

- `application/`: Contains various modules and files related to the application logic.
  - `api.py`: Defines all the APIs using Flask-RESTful.
  - `config.py`: Contains application configurations.
  - `database.py`: Handles database setup and configurations.
  - `login.py`: Manages user login functionality.
  - `controllers.py`: Implements CRUD operations and other functionalities.
  - `models.py`: Defines data models using SQLAlchemy ORM.
  - `workers.py`: Configures Celery for asynchronous tasks.
  - `emailcontrollers.py`: Schedules and handles email-related tasks.
- `db_directory/`: Contains the SQLite database file (`test.sqlite3`).
- `static/`: Holds static assets like uploaded images.
- `templates/`: Contains HTML templates for rendering pages.
- `api.yaml`: Specifications for the APIs in YAML format.
- `main.py`: Entry point of the backend application.
- `requirements.txt`: Lists all the required Python dependencies.

## Getting Started (In Linux)

1. Clone this repository to your local machine.
2. open a new terminal and run 'redis-server'. Redis server will run lon localhost :port 6379. We can check it using RESP.
3. open a new terminal and change directory to the Backend folder and run mail.sh to start mailhog. It will run on localhost:port  8025

4. Set up a virtual environment and activate it.
   
   Open a terminal and Run local_setup.sh- it will make virtual environmment and install all dependecies for the backend flask project.

   Run local_run.sh in the same terminal, app will run on localhost:8080

   Run local_workers.sh and local_beat.sh in separate terminals

## API Documentation

API endpoints and specifications are documented in the `api.yaml` file. You can use tools like Swagger UI or Postman to interact with the APIs.

## Contributing

Contributions are welcome! If you find issues or want to add new features, feel free to submit a pull request.

## License

This project is licensed under the ******************

## Useful commands
 find . -type f -exec dos2unix {} \;  Running the dos2unix command  is used to correct line-ending issues without changing the functionality of the code.(Useful when code has been written/edited using VS Code)

 ## prettify

npm run format-prettier for frontend




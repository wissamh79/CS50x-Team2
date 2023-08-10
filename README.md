# Medicina Project for for patients and doctors

##### The aim of this project is to create an electronic system for reservations with doctors, as well as to follow up the patient's previous condition by adding his review history.

To run this project, most importantly, python needs to be installed on the host machine. To check if python is installed, run
`python --version`
OR
`py --version`. If it returns a version number, then you're good to go. If it throws an error like '_Command is not recognized or Found_' then you should install python first.

Also, you need to have sqlite3 installed to. To check that, run: `sqlite3 --version`. If it is not installed, go ahead and install it.

Now that we have python installed, follow the steps:

- Open a terminal and `cd` into the folder of the project.
- Run `python -m venv venv` and wait a few seconds until it finishes.
- Depending on your OS:

  - Windows: Run `./venv/Scripts/activate`
  - Mac or Linux: Run `./venv/bin/activate`

- Run `pip install -r requirements.txt` and wait until it finishes installing the packages required.
- Now in the terminal, run: `python app.py` and it will start the server, now you can visit these routes:

| Route                            | Html to Render                            |
| -------------------------------- | ----------------------------------------- |
| `/`                              | `templates/index.html`                    |
| `/signup`                        | `templates/registration.html`             |
| `/login`                         | `templates/login.html`                    |
| `/logout`                        | `templates/logout.html`                   |
| `/patient personal page`         | `templates/patient_profile.html`          |
| `/doctor's personal page`        | `templates/doctor_profile.html`           |
| `/doctor's purview page`         | `templates/doctors_purview.html`          |
| `/patient history page`          | `templates/patient_history.html`          |
| `/reservations`                  | `templates/reservations.html`             |
| `/confirm reservations`          | `templates/confirm.html`                  |

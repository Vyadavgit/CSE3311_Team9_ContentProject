# CSE3311_Team9_ContentProject

The University of Texas at Arlington - Fall 2020 CSE3311-Team9 project.

**Team members**:<br />
Vivek Kumar Yadav <br />
Sergio Gonzalez <br />
Hersh Yogesh Mistry <br />
Koshish Khadka <br />


**Steps to compile our project:** <br />
Django <br />
    ● Download pip by using the command in the command-line interface: curl
    https://bootstrap.pypa.io/get-pip.py -o get-pip.py <br />
    ● Download Django using the command the command-line interface: pip install
    Django==3.*.* (please make sure the system has pip downloaded for this command to
    work, and here *,* is the latest version number) <br />
    ● Run this command to get the latest version of Django in the command-line interface: git
    clone https://github.com/django/django.git <br />
   
Python <br />
    ● Download Python3 for your respective operating system from
    https://www.python.org/downloads/ <br />

Github Repository (Download) <br />
    ● Download a zip file from the GitHub repository: 
    https://github.com/Vyadavgit/CSE3311_Team9_ContentProject <br />

Github Repository (Clone) <br />
    ● Create or choose a folder in the directory you wish to store the source code in. <br />
    ● Navigate to the folder in the directory using the command-line interface, and type “git
    init”. <br />
    ● Type “git pull https://github.com/Vyadavgit/CSE3311_Team9_ContentProject.git” <br />
    ● Navigate to DigitalContentsWebApp <br />
    
Stripe CLI <br />
    ● Install Stripe CLI or just perform step 1 from the following site:
    https://stripe.com/docs/stripe-cli <br />
    If installation did not work from the terminal then use the manual method provided by the
    website. <br />
    
**Local database setup instructions**: <br />
PostgreSQL Database Download <br />
    ● Download and install PostgreSQL setup file that supports your OS from the link below:
    https://www.enterprisedb.com/downloads/postgres-postgresql-downloads <br />
    
pgAdmin 4 <br />
    ● Download and install pgAdmin setup file that supports you OS from the link below:
    https://www.pgadmin.org/download/ <br />
 
After pgAdmin is installed your default browser will pop up with this link
http://127.0.0.1:56140/browser/ . Enter the master password for the pgAdmin and remember it
for following steps. <br />

Next steps: <br />
    Create a server group go to its properties and fill the information for following fields: <br />
    General: ‘Name’ <br />
    Connection: ‘Host name/address’ <br />
    
Use the master password you created while installing the pgAdmin for the password field. Also,
leave the defaults as it is. <br />

Create a database in the server and provide a name to it. <br />

Navigate to DigitalContentsWebApp file and run the commands “python manage.py <br />
makemigrations” followed by “python manage.py migrate” after that. <br />

Go to the “auth_group” in the “Tables” of the database you just created and add two groups as
following in the data rows for “auth_group”. <br />
    Id: 1 name: Viewer <br />
    Id: 2 name: Subscriber <br />
 
Save your changes. <br />

In settings.py file provide inputs for the following requirements based on the data you provided
above while setting your database: <br />


        # POSTGRES DATABASE LOCAL
        DATABASES = {
        Page 4
         'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': '*******',
         'USER': '**********',
         'PASSWORD': ‘*******’,
         'HOST': 'localhost',
         'PORT': '****'
         }
        }

Save your changes and the local database is ready for the project to run. <br />

Run <br />
    ● Navigate to DigitalContentsWebApp using the terminal. <br />
    ● Install requirements for this project from requirements.txt using the command: pip install
    requirements.txt <br />
    ● Type “python manage.py runserver” <br />
    ● Open a new terminal/prompt and then type “stripe listen --forward-to
    localhost:8000/webhook/” and let the server run in the background. <br />
    ● Use command “stripe login” in the terminal <br />
    ● Open a web browser and navigate to “http://127.0.0.1:8000/” (or use the IP address
    provided by Django server in the command-line interface) <br />


**Info for contributers**: <br />
Always use this command before creating a branch/writing your code:  
	 **git pull** :- command to pull the updated source code from the repository.<br />

Always create and work on a new branch if you are working on a new feature:<br />
	 **git branch BRANCHNAME** :- command to create a new branch<br />
	 **git checkout BRANCHNAME** :- command to switch to a different branch<br />

After you are ready to push a new feature/ready to update code follow commands below:<br />
	 **git add .** :- command to add your modifications<br />
	 **git commit -m "WRITE A SHORT DESCRIPTION ABOUT MODIFICATIONS/FEATURES YOU ADDED"** :- command to add short description<br />
	 **git push** :- command to push your code to repo [Please push it to your branch]<br />
	
Yay, You did it!<br />

Other commands:<br />
	 **git checkout master** :- command to switch to master branch<br />
	 **git status** :- command to check your current status <br />
	 **git branch** :- command to list available branches<br />
	 **git branch BRANCHNAME -D** :- command to delete branch<br />




# Web-Based-Cognitive-Assessment
<h3>Project Description</h3>
  <ol>
    <li>Web-based application to digitize the Philadelphia Pointing Span Test (PPST) to assess cognitive functions for early detection of neurological disorders. The test is delivered digitally in a user friendly way that allows for efficient calculations and secure tracking of patient metrics. Doctors are able to manage tests created for patients and easily compare patient data in table + graph formats.</li>
    <li>I was responsible for generating fake data in fixture.py, designing/creating the models and their respective functions, building the bash script, aggregating data, and making the aggregate data sheets in ss.py </li>
  </ol>

<h3>Set up for PPST</h3>


**Installation instructions**
  
  <ol>
  <li>Clone this repository: <b>git clone https://github.com/jacobschmitt23/Web-Based-Cognitive-Assessment.git</b> </li>
  <li>In the folder SP-team, create a virtual environment: <b>python3 -m venv venv</b> </li>
  <li>Activate the virtual environment:  <b>source venv/bin/activate</b></li>
  <li>Install dependencies:  <b>pip install django, numpy, scipy, pandas, mpld3, matplotlib, openpyxl</b></li>
  <li>Perform migrations:  <b>python manage.py makemigrations model</b></li> 
  <li>Migrate:  <b>python manage.py migrate</b></li>
  <li>Another Method of Performing Migrations: <b>bash clean-migrations.sh</b></li>
  <li>Install the fixture:  <b>python manage.py shell < fixture.py</b></li>
  <li>Run the project (either from the command line using  <b>python manage.py runserver</b>) or from your IDE</li>
  <li>Create a super user for admin <b>python manage.py createsuperuser</b></bi>
  </ol>

  **Additional Notes**
  
  <ol>
  <li>For download functionality to work, a folder named "temp" should be in the source directory if not generated during runtime.</li>
  <li>For there to be aggregate data the fixture must be run. If not the view data page and spreadsheet will not work properly.</li>
  </ol>

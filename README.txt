pip install -r requirements.txt

download and install Graphviz from https://gitlab.com/graphviz/graphviz/-/releases

Run the test.py with a help of python 3.9.

1. This project generates in the Docker a mcr.microsoft.com/mssql/server (it is about 1.57GB) and runs it.

2. It connects to the SQL Server, extracts data, performs data transformations, and generates an ERD (.png file).

3. It also initializes a Docker container and runs unit tests.

4. It creates an .env file with access credentials to a database containing target data.

5. It also copyies DataBase FilmData to our created Docker container.

6. Afterward it provides a report (Test_Report_db.txt) about quality and unit test results of Database FilmData.

7. It also creates a Docker ini file based on our created mcr.microsoft.com/mssql/server with a copied Database in it. so, you can build and run another Docker image.
import pyodbc
import pydot
import os
import docker
import unittest
from dotenv import load_dotenv
load_dotenv()

def connect_to_database(server, database, username, password):
    conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
    return pyodbc.connect(conn_str)

def get_table_names(cursor, database):
    table_names_query = """
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE' 
        AND TABLE_CATALOG = ? 
        AND TABLE_SCHEMA = 'dbo'
        AND TABLE_NAME NOT LIKE 'sys%'
    """
    return [table_name[0] for table_name in cursor.execute(table_names_query, database)]

def get_column_names(cursor, table_name, database):
    column_names_query = """
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = ? 
        AND TABLE_CATALOG = ? 
        AND TABLE_SCHEMA = 'dbo'
    """
    return [column[0] for column in cursor.execute(column_names_query, (table_name, database))]

def check_primary_key(cursor, table_name):
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE TABLE_NAME = ? AND CONSTRAINT_TYPE = 'PRIMARY KEY'", (table_name,))
    primary_key_count = cursor.fetchone()[0]
    return primary_key_count > 0

def check_data_characteristics(cursor, table_name):
    characteristics_checks = []
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]
    characteristics_checks.append(f"- Row Count: {row_count}")

    cursor.execute(f"SELECT COUNT(DISTINCT *) FROM {table_name}")
    distinct_row_count = cursor.fetchone()[0]
    characteristics_checks.append(f"- Distinct Row Count: {distinct_row_count}")

    return characteristics_checks

def check_data_uniqueness(cursor, table_name, database):
    uniqueness_checks = []
    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
    columns = cursor.fetchall()
    column_names = [col[0] for col in columns]

    for column_name in column_names:
        cursor.execute(f"SELECT COUNT(*), COUNT(DISTINCT {column_name}) FROM {table_name}")
        counts = cursor.fetchone()
        total_count, distinct_count = counts[0], counts[1]
        if total_count != distinct_count:
            uniqueness_checks.append(f"- Uniqueness violated for column '{column_name}': Total Count - {total_count}, Distinct Count - {distinct_count}")

    return uniqueness_checks

def check_data_integrity(cursor, table_name, database):
    integrity_checks = []
    if table_name == 'film_actor':
        # Check if actor_id and film_id combinations exist in the actor and film tables respectively
        cursor.execute(f"""
            SELECT COUNT(*) 
            FROM {table_name} fa
            LEFT JOIN actor a ON fa.actor_id = a.actor_id
            LEFT JOIN film f ON fa.film_id = f.film_id
            WHERE a.actor_id IS NULL OR f.film_id IS NULL
        """)
        invalid_combinations_count = cursor.fetchone()[0]
        if invalid_combinations_count > 0:
            integrity_checks.append(f"- Invalid actor_id or film_id combinations found in {table_name}: {invalid_combinations_count}")
        else:
            integrity_checks.append("OK")  # Add "OK" when no issues are found
    return integrity_checks

def check_data_consistency(cursor, table_name, database):
    consistency_checks = []
    if table_name == 'film_actor':
        # Check if the same actor appears in the same film multiple times
        cursor.execute(f"""
            SELECT actor_id, film_id, COUNT(*) as appearances
            FROM {table_name}
            GROUP BY actor_id, film_id
            HAVING COUNT(*) > 1
        """)
        duplicate_actor_film_combinations = cursor.fetchall()
        if duplicate_actor_film_combinations:
            for actor_id, film_id, appearances in duplicate_actor_film_combinations:
                consistency_checks.append(f"- Duplicate appearances of actor {actor_id} in film {film_id}: {appearances} times")
        else:
            consistency_checks.append("OK")  # Add "OK" when no issues are found
    return consistency_checks


def check_non_nullable_columns(cursor, table_name, database):
    cursor.execute(f"""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = ? 
        AND TABLE_CATALOG = ? 
        AND TABLE_SCHEMA = 'dbo' 
        AND IS_NULLABLE = 'NO'
    """, (table_name, database))
    non_nullable_columns = cursor.fetchall()
    null_checks = []
    for column in non_nullable_columns:
        column_name = column[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} IS NULL")
        null_count = cursor.fetchone()[0]
        null_checks.append((column_name, null_count))
    return null_checks

def generate_quality_check_report(cursor, table_names, database):
    quality_check_report = ""
    for table_name in table_names:
        quality_check_report += f"Table: {table_name}\n"
        quality_check_report += "- Primary Key: " + ("Found\n" if check_primary_key(cursor, table_name) else "Missing\n")
        null_checks = check_non_nullable_columns(cursor, table_name, database)
        for column_name, null_count in null_checks:
            quality_check_report += f"- Non-nullable column '{column_name}': {null_count} missing values\n"
        quality_check_report += "\n"

      # Check uniqueness
        quality_check_report += "- Uniqueness:\n"
        uniqueness_checks = check_data_uniqueness(cursor, table_name, database)
        for check in uniqueness_checks:
            quality_check_report += f"  {check}\n"
        
        # Check integrity
        integrity_checks = check_data_integrity(cursor, table_name, database)
        if integrity_checks:
            quality_check_report += "- Integrity:\n"
            for check in integrity_checks:
                quality_check_report += f"  {check}\n"
        else:
            quality_check_report += "- Integrity: OK\n"
        
        # Check consistency
        consistency_checks = check_data_consistency(cursor, table_name, database)
        if consistency_checks:
            quality_check_report += "- Consistency:\n"
            for check in consistency_checks:
                quality_check_report += f"  {check}\n"
        else:
            quality_check_report += "- Consistency: OK\n"
        
        quality_check_report += "\n"
    return quality_check_report


def build_data_pipeline(server, database, username, password):
    conn = connect_to_database(server, database, username, password)
    cursor = conn.cursor()

    table_names = get_table_names(cursor, database)
    table_info = {table_name: {'columns': get_column_names(cursor, table_name, database)} for table_name in table_names}

    quality_check_report = generate_quality_check_report(cursor, table_names, database)

    cursor.close()
    conn.close()

    return table_info, quality_check_report

def generate_erd(table_info):
    os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'  # Adjust the path as per your Graphviz installation
    graph = pydot.Dot(graph_type='digraph')
    relationships = [('actor', 'film_actor'), ('category', 'film'), ('film', 'film_actor'),
                     ('film', 'inventory'), ('film', 'language')]
    for table_name, info in table_info.items():
        node_label = f"{table_name}\nColumns: {', '.join(info['columns'])}"
        node = pydot.Node(table_name, label=node_label, shape='box')
        graph.add_node(node)
    for relationship in relationships:
        edge = pydot.Edge(relationship[0], relationship[1])
        graph.add_edge(edge)
    graph.write_png('erd.png')


def create_env_file(server, database, username, password):
    env_content = f"SQL_SERVER={server}\nSQL_DATABASE={database}\nSQL_USERNAME={username}\nSQL_PASSWORD={password}"
    with open('.env', 'w') as env_file:
        env_file.write(env_content)

def initialize_docker_container():
    # Initialize Docker client
    client = docker.from_env()

    try:
        # Check if the container already exists
        existing_container = client.containers.get('sql_server_container')
        container_id = existing_container.id
        container_ip = existing_container.attrs['NetworkSettings']['IPAddress']
        print(f'Container already exists. ID: {container_id}, IP: {container_ip}')
    except docker.errors.NotFound:
        # Pull the SQL Server Docker image
        client.images.pull('mcr.microsoft.com/mssql/server:latest')

        # Define environment variables for SQL Server container
        env_vars = {'ACCEPT_EULA': 'Y', 'SA_PASSWORD': password}

        # Define port bindings for SQL Server container
        port_bindings = {'1433/tcp': ('localhost', 1433)}

        # Run a Docker container with SQL Server
        container = client.containers.run('mcr.microsoft.com/mssql/server:latest', name='sql_server_container',
                                          detach=True, environment=env_vars, ports=port_bindings)

        # Get IP address of the container
        container_info = client.containers.get(container.id)
        container_ip = container_info.attrs['NetworkSettings']['Networks']['bridge']['IPAddress']

        # Create .env file with container IP address and database credentials
        create_env_file(container_ip, database, username, password)

        print(f'Container ID: {container.id}, IP address: {container_ip}')

def generate_dockerfile_from_env(env_file, output_file="Dockerfile"):
    """
    Generate a Dockerfile based on environment variables specified in the given .env file.

    Args:
        env_file (str): Path to the .env file containing environment variables.
        output_file (str): Path to the output Dockerfile.

    Returns:
        None
    """
    # Read the environment variables from the .env file
    with open(env_file, 'r') as f:
        env_vars = {}
        for line in f:
            key, value = line.strip().split('=')
            env_vars[key] = value
    
    # Create the Dockerfile with the environment variables
    with open(output_file, 'w') as dockerfile:
        dockerfile.write(f"""
# Use the SQL Server 2019 Linux container image as the base image
FROM mcr.microsoft.com/mssql/server:latest

# Set environment variables for SQL Server
ENV ACCEPT_EULA=${env_vars.get("ACCEPT_EULA")}
ENV SA_PASSWORD=${env_vars.get("SA_PASSWORD")}
ENV MSSQL_PID=Express
ENV MSSQL_TCP_PORT=1433
ENV SQL_USERNAME=${env_vars.get("SQL_USERNAME")}
ENV SQL_PASSWORD=${env_vars.get("SQL_PASSWORD")}

EXPOSE 1433
""")
        
def run_tests():
    # Define test cases
    class DataQualityTest(unittest.TestCase):
        def setUp(self):
            self.conn = connect_to_database(server, database, username, password)

        def tearDown(self):
            self.conn.close()

        def test_primary_key_constraints(self):
            cursor = self.conn.cursor()
            cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
            tables = cursor.fetchall()
            for table in tables:
                table_name = table[0]
                cursor.execute(f'SELECT COUNT(*) FROM (SELECT DISTINCT * FROM {table_name}) AS distinct_rows')
                distinct_row_count = cursor.fetchone()[0]
                cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
                row_count = cursor.fetchone()[0]
                self.assertEqual(row_count, distinct_row_count, f"Primary key constraint violated in '{table_name}' table")

        def test_data_integrity(self):
            cursor = self.conn.cursor()
            cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
            tables = cursor.fetchall()
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
                columns = cursor.fetchall()
                column_names = [col[0] for col in columns]
                if 'first_name' in column_names:
                    cursor.execute(f'SELECT COUNT(*) FROM {table_name} WHERE first_name = \'\'')
                    empty_first_names_count = cursor.fetchone()[0]
                    self.assertEqual(empty_first_names_count, 0, f"Data integrity violated: {table_name} first names cannot be empty")

    # Run tests
    suite = unittest.TestLoader().loadTestsFromTestCase(DataQualityTest)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    print(f"\nTest Report:\n{result}")

if __name__ == '__main__':

    database = os.getenv('POSTGRES_DATABASE')
    username = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    server = os.getenv('POSTGRES_URL')
    server += ',5432'

    table_info, quality_check_report = build_data_pipeline(server, database, username, password)

    print("\nQuality Check Report:")
    print("--------------------")
    print(quality_check_report)
        # Write test report to file
    with open('Test_Report_db_'+database+'.txt', 'w') as report_file:
        report_file.write(str(quality_check_report))
    generate_erd(table_info)

    initialize_docker_container()

    run_tests()
    
    env_file = '.env'
    output_file = 'Dockerfile'
    generate_dockerfile_from_env(env_file, output_file)
    

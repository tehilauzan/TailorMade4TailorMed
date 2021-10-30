from bs4 import BeautifulSoup
import requests
import sqlite3
import uuid

def create_db(conn):
    conn.execute('''CREATE TABLE Funds(Uuid TEXT, AssistanceProgramName TEXT, Status TEXT, GrantAmount TEXT)''')
    conn.execute('''CREATE TABLE EligibleTreatments (Uuid TEXT, Treatments TEXT)''')
    conn.execute('''CREATE TABLE TreatmentsCovered (Uuid TEXT, UuidFunds TEXT, UuidEligibleTreatments TEXT)''')

def init_to_db(conn, assistance_program):
    # Initialize the db for the first time
    found_uuid = str(uuid.uuid4())
    conn.execute('''INSERT INTO Funds VALUES(?,?,?,?)''', (found_uuid, assistance_program["name"], assistance_program["status"], assistance_program["grant amount"]))
    for tretment in assistance_program["treatments"]:
        Check_if_tretment_exsits = ('''SELECT * FROM EligibleTreatments WHERE Treatments = ? ''')
        conn.execute(Check_if_tretment_exsits, (tretment,))
        if (conn.fetchall() == []):
            eligible_treatments_uuid = str(uuid.uuid4())
            conn.execute('''INSERT INTO EligibleTreatments VALUES(?,?)''', (eligible_treatments_uuid,tretment))
            conn.execute('''INSERT INTO TreatmentsCovered VALUES(?,?,?)''', (str(uuid.uuid4()), found_uuid, eligible_treatments_uuid))
        else:
            query_uuid_treatment = ('''SELECT Uuid FROM EligibleTreatments WHERE Treatments = ? ''')
            conn.execute(query_uuid_treatment, (tretment,))
            uuid_treatment = conn.fetchone()[0]
            conn.execute('''INSERT INTO TreatmentsCovered VALUES(?,?,?)''', (str(uuid.uuid4()), found_uuid, uuid_treatment))


def update_db(conn, assistance_program):
    query_found_uuid = ('''SELECT Uuid FROM Funds WHERE AssistanceProgramName = ? ''')
    conn.execute(query_found_uuid, (assistance_program["name"],))
    found_uuid = conn.fetchone()[0]
    update_query_funds = '''UPDATE Funds SET Status = ?,  GrantAmount= ? where AssistanceProgramName = ? '''
    update_variables = assistance_program["status"], assistance_program["grant amount"], assistance_program["name"]
    conn.execute(update_query_funds, update_variables)
    for tretment in assistance_program["treatments"]:
        Check_if_tretment_exsits = ('''SELECT * FROM EligibleTreatments WHERE Treatments = ? ''')
        conn.execute(Check_if_tretment_exsits, (tretment,))
    if (conn.fetchall() == []):
        eligible_treatments_uuid = str(uuid.uuid4())
        conn.execute('''INSERT INTO EligibleTreatments VALUES(?,?)''', (eligible_treatments_uuid, tretment))
        conn.execute('''INSERT INTO TreatmentsCovered VALUES(?,?,?)''',
                     (str(uuid.uuid4()), found_uuid, eligible_treatments_uuid))
    else:
        query_uuid_treatment = ('''SELECT Uuid FROM EligibleTreatments WHERE Treatments = ? ''')
        conn.execute(query_uuid_treatment, (tretment,))
        uuid_treatment = conn.fetchone()
        query_uuid_TreatmentsCovered = ('''SELECT UuidFunds FROM TreatmentsCovered WHERE UuidEligibleTreatments = ? ''')
        conn.execute(query_uuid_TreatmentsCovered, uuid_treatment)
        UuidFunds = conn.fetchone()
        if str(UuidFunds) != found_uuid:
            conn.execute('''INSERT INTO TreatmentsCovered VALUES(?,?,?)''', (str(uuid.uuid4()), str(found_uuid), str(uuid_treatment)))

def get_data_from_db():
    assistance_program_data={}
    query_funds_table = ('''SELECT * FROM Funds''')
    query_funds_table = ('''SELECT * FROM EligibleTreatments''')
    query_funds_table = ('''SELECT * FROM TreatmentsCovered''')


def extract_details_found(url):
    html_text = requests.get(url).text
    assistance_programs = {}
    eligible_treatments = []
    soup = BeautifulSoup(html_text, 'lxml')
    assistance_program_name = soup.find('h1').text.replace(' ', '').replace('\t', '').replace('\n', '')
    assistance_programs["name"] = assistance_program_name
    details_div = soup.find_all('div', class_="details")[0]
    for h4 in details_div.find_all('h4'):
        if 'Status' in h4:
            status = h4.next_sibling.replace(' ', '').replace('\t', '').replace('\n', '')
            assistance_programs["status"] = status
        if 'MaximumAwardLevel' in h4.text.replace(' ', ''):
            grant_amount = h4.next_sibling.replace(' ', '').replace('\t', '').replace('\n', '')
            assistance_programs["grant amount"] = grant_amount
    treatments = soup.find('div', class_="treatments")
    treatments_list = treatments.find_all('li')
    for treatment in treatments_list:
        eligible_treatments.append(treatment.text)
    assistance_programs["treatments"] = eligible_treatments
    return assistance_programs


def main():
    connection = sqlite3.connect('funds.db')
    conn = connection.cursor()
    # Run one time at the beginning to create the db
    # create_db(conn)
    # Create list of url of the 5 assistance programs
    assistance_programs_url = ['https://www.healthwellfoundation.org/fund/acute-myeloid-leukemia-medicare-access/',
                               'https://www.healthwellfoundation.org/fund/adrenal-insufficiency/',
                               'https://www.healthwellfoundation.org/fund/amyotrophic-lateral-sclerosis/',
                               'https://www.healthwellfoundation.org/fund/chronic-lymphocytic-leukemia-medicare-access/',
                               'https://www.healthwellfoundation.org/fund/congenital-sucrase-isomaltase-deficiency/']
    assistance_program = {}
    for url in assistance_programs_url:
        assistance_program = extract_details_found(url)
        # init_to_db(conn, assistance_program)
        update_db(conn, assistance_program)

    assistance_program_data = get_data_from_db()

    connection.commit()
    # conn.execute('''SELECT * FROM Funds WHERE AssistanceProgramName = "AcuteMyeloidLeukemia" ''')
    # funds = conn.fetchall()


if __name__ == '__main__':
    main()
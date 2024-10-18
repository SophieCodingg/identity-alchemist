import random
import string
import datetime
from datetime import date
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from faker import Faker
from cryptography.fernet import Fernet
import csv
import json
import sqlite3
import re
from collections import Counter

class IdentityGenerator:
    def __init__(self):
        self.fake = Faker()
        self.countries = ['USA', 'Canada', 'UK', 'Australia', 'Germany', 'France', 'Spain', 'Italy', 'Japan', 'Brazil']
        self.ethnicities = ['Caucasian', 'African American', 'Hispanic', 'Asian', 'Middle Eastern', 'Native American', 'Pacific Islander']
        self.education_levels = ['High School', 'Associate', 'Bachelor', 'Master', 'PhD']
        self.occupations = ['Engineer', 'Teacher', 'Doctor', 'Lawyer', 'Accountant', 'Manager', 'Salesperson', 'Artist', 'Programmer', 'Nurse']

    def generate_identity(self):
        gender = random.choice(['Male', 'Female'])
        first_name = self.fake.first_name_male() if gender == 'Male' else self.fake.first_name_female()
        last_name = self.fake.last_name()
        dob = self.fake.date_of_birth(minimum_age=18, maximum_age=80)
        age = (date.today() - dob).days // 365
        country = random.choice(self.countries)
        ethnicity = random.choice(self.ethnicities)
        education = random.choice(self.education_levels)
        occupation = random.choice(self.occupations)
        email = f"{first_name.lower()}.{last_name.lower()}@{self.fake.free_email_domain()}"
        phone = self.fake.phone_number()
        address = self.fake.address()
        credit_card = self.fake.credit_card_full()
        ssn = self.fake.ssn()

        return {
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender,
            'dob': dob.strftime('%Y-%m-%d'),  # Convertir a string para facilitar la serialización
            'age': age,
            'country': country,
            'ethnicity': ethnicity,
            'education': education,
            'occupation': occupation,
            'email': email,
            'phone': phone,
            'address': address,
            'credit_card': credit_card,
            'ssn': ssn
        }

class MachineLearningModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.features = ['age', 'gender', 'ethnicity', 'education', 'occupation']
        self.target = 'country'
        self.ethnicities = ['Caucasian', 'African American', 'Hispanic', 'Asian', 'Middle Eastern', 'Native American', 'Pacific Islander']
        self.education_levels = ['High School', 'Associate', 'Bachelor', 'Master', 'PhD']
        self.occupations = ['Engineer', 'Teacher', 'Doctor', 'Lawyer', 'Accountant', 'Manager', 'Salesperson', 'Artist', 'Programmer', 'Nurse']
        self.countries = ['USA', 'Canada', 'UK', 'Australia', 'Germany', 'France', 'Spain', 'Italy', 'Japan', 'Brazil']
        self.is_trained = False

    def prepare_data(self, identities):
        X = []
        y = []
        for identity in identities:
            features = [
                identity['age'],
                1 if identity['gender'] == 'Male' else 0,
                self.ethnicities.index(identity['ethnicity']),
                self.education_levels.index(identity['education']),
                self.occupations.index(identity['occupation'])
            ]
            X.append(features)
            y.append(self.countries.index(identity['country']))
        return np.array(X), np.array(y)

    def train(self, X, y):
        if len(X) < 2:
            raise ValueError("Not enough data to train the model. Generate more identities first.")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        accuracy = self.model.score(X_test, y_test)
        print(f"Model accuracy: {accuracy:.2f}")
        self.is_trained = True

    def predict(self, identity):
        if not self.is_trained:
            raise Exception("Model has not been trained yet.")
        try:
            features = [
                identity['age'],
                1 if identity['gender'] == 'Male' else 0,
                self.ethnicities.index(identity['ethnicity']),
                self.education_levels.index(identity['education']),
                self.occupations.index(identity['occupation'])
            ]
            prediction = self.model.predict([features])[0]
            return self.countries[prediction]
        except Exception as e:
            print(f"Prediction failed: {str(e)}")
            return None

class DataValidator:
    @staticmethod
    def validate_age(age):
        return 18 <= age <= 100

    @staticmethod
    def validate_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_phone(phone):
        pattern = r'^\+?1?\d{9,15}$'
        return re.match(pattern, phone) is not None

    @staticmethod
    def validate_credit_card(cc_number):
        cc_number = ''.join(filter(str.isdigit, cc_number))
        if not cc_number.isdigit():
            return False
        digits = [int(d) for d in cc_number]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for digit in even_digits:
            checksum += sum(divmod(digit * 2, 10))
        return checksum % 10 == 0

class IdentityEncryptor:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)

    def encrypt_identity(self, identity):
        encrypted_identity = {}
        for key, value in identity.items():
            encrypted_value = self.fernet.encrypt(str(value).encode())
            encrypted_identity[key] = encrypted_value.decode()
        return encrypted_identity

    def decrypt_identity(self, encrypted_identity):
        decrypted_identity = {}
        for key, value in encrypted_identity.items():
            decrypted_value = self.fernet.decrypt(value.encode()).decode()
            decrypted_identity[key] = decrypted_value
        return decrypted_identity

class IdentityAnalyzer:
    def __init__(self, identities):
        self.identities = identities

    def get_age_distribution(self):
        ages = [identity['age'] for identity in self.identities]
        return {
            'mean': sum(ages) / len(ages),
            'median': sorted(ages)[len(ages) // 2],
            'min': min(ages),
            'max': max(ages)
        }

    def get_gender_distribution(self):
        genders = [identity['gender'] for identity in self.identities]
        return {gender: genders.count(gender) / len(genders) for gender in set(genders)}

    def get_country_distribution(self):
        countries = [identity['country'] for identity in self.identities]
        return {country: countries.count(country) / len(countries) for country in set(countries)}

    def get_most_common_names(self, n=10):
        first_names = [identity['first_name'] for identity in self.identities]
        last_names = [identity['last_name'] for identity in self.identities]
        
        return {
            'first_names': dict(Counter(first_names).most_common(n)),
            'last_names': dict(Counter(last_names).most_common(n))
        }

class IdentityExporter:
    @staticmethod
    def export_to_csv(identities, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = identities[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for identity in identities:
                writer.writerow(identity)

    @staticmethod
    def export_to_json(identities, filename):
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(identities, jsonfile, indent=4, ensure_ascii=False)

    @staticmethod
    def export_to_sql(identities, db_name):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS identities
                     (id INTEGER PRIMARY KEY,
                      first_name TEXT,
                      last_name TEXT,
                      gender TEXT,
                      dob DATE,
                      age INTEGER,
                      country TEXT,
                      ethnicity TEXT,
                      education TEXT,
                      occupation TEXT,
                      email TEXT,
                      phone TEXT,
                      address TEXT,
                      credit_card TEXT,
                      ssn TEXT)''')
        
        for identity in identities:
            c.execute('''INSERT INTO identities
                         (first_name, last_name, gender, dob, age, country, ethnicity, education, occupation, email, phone, address, credit_card, ssn)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (identity['first_name'], identity['last_name'], identity['gender'], identity['dob'],
                       identity['age'], identity['country'], identity['ethnicity'], identity['education'],
                       identity['occupation'], identity['email'], identity['phone'], identity['address'],
                       identity['credit_card'], identity['ssn']))
        
        conn.commit()
        conn.close()

class IdentityImporter:
    @staticmethod
    def import_from_csv(filename):
        identities = []
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                identities.append(row)
        return identities

    @staticmethod
    def import_from_json(filename):
        with open(filename, 'r', encoding='utf-8') as jsonfile:
            identities = json.load(jsonfile)
        return identities

    @staticmethod
    def import_from_sql(db_name):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        
        c.execute("SELECT * FROM identities")
        rows = c.fetchall()
        
        column_names = [description[0] for description in c.description]
        identities = []
        for row in rows:
            identity = dict(zip(column_names, row))
            identities.append(identity)
        
        conn.close()
        return identities

class FakeIdentitySystem:
    def __init__(self):
        self.identity_generator = IdentityGenerator()
        self.ml_model = MachineLearningModel()
        self.generated_identities = []
        self.data_validator = DataValidator()
        self.identity_encryptor = IdentityEncryptor()
        self.identity_analyzer = None  # Inicializado como None
        self.identity_exporter = IdentityExporter()
        self.identity_importer = IdentityImporter()

    def generate_identities(self, num_identities):
        for _ in range(num_identities):
            identity = self.identity_generator.generate_identity()
            self.generated_identities.append(identity)
        print(f"Generated {num_identities} fake identities.")
        # Actualizar el analizador después de generar nuevas identidades
        self.identity_analyzer = IdentityAnalyzer(self.generated_identities)

    def train_model(self):
        if not self.generated_identities:
            print("No identities generated yet. Generate some identities first.")
            return
        X, y = self.ml_model.prepare_data(self.generated_identities)
        try:
            self.ml_model.train(X, y)
        except ValueError as e:
            print(f"Error training model: {str(e)}")

    def generate_enhanced_identity(self):
        if not self.ml_model.is_trained:
            print("Model not trained yet. Train the model first.")
            return None
        base_identity = self.identity_generator.generate_identity()
        predicted_country = self.ml_model.predict(base_identity)
        if predicted_country:
            base_identity['country'] = predicted_country
        return base_identity

    def save_identities_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            for identity in self.generated_identities:
                f.write(str(identity) + '\n')
        print(f"Saved {len(self.generated_identities)} identities to {filename}")

    def generate_fake_id_card(self, identity):
        id_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        issue_date = self.identity_generator.fake.date_between(start_date='-5y', end_date='today')
        expiry_date = issue_date + datetime.timedelta(days=365 * 10)  # 10 years validity

        dob = datetime.datetime.strptime(identity['dob'], '%Y-%m-%d').date()

        id_card = f"""
        ================================
        {identity['country'].upper()} IDENTIFICATION CARD
        ================================
        ID Number: {id_number}
        Name: {identity['first_name']} {identity['last_name']}
        Gender: {identity['gender']}
        Date of Birth: {dob.strftime('%Y-%m-%d')}
        Nationality: {identity['country']}
        Address: {identity['address']}
        
        Issue Date: {issue_date.strftime('%Y-%m-%d')}
        Expiry Date: {expiry_date.strftime('%Y-%m-%d')}
        ================================
        """
        return id_card

    def validate_identity(self, identity):
        is_valid = True
        is_valid &= self.data_validator.validate_age(identity['age'])
        is_valid &= self.data_validator.validate_email(identity['email'])
        is_valid &= self.data_validator.validate_phone(identity['phone'])
        is_valid &= self.data_validator.validate_credit_card(identity['credit_card'])
        return is_valid

    def encrypt_identities(self):
        try:
            self.encrypted_identities = [
                self.identity_encryptor.encrypt_identity(identity) 
                for identity in self.generated_identities
            ]
            print("Identities encrypted successfully.")
        except Exception as e:
            print(f"Encryption failed: {str(e)}")


    def decrypt_identities(self):
        self.decrypted_identities = [self.identity_encryptor.decrypt_identity(identity) for identity in self.encrypted_identities]

    def analyze_identities(self):
        age_distribution = self.identity_analyzer.get_age_distribution()
        gender_distribution = self.identity_analyzer.get_gender_distribution()
        country_distribution = self.identity_analyzer.get_country_distribution()
        common_names = self.identity_analyzer.get_most_common_names()
        
        print("Identity Analysis:")
        print(f"Age Distribution: {age_distribution}")
        print(f"Gender Distribution: {gender_distribution}")
        print(f"Country Distribution: {country_distribution}")
        print(f"Most Common Names: {common_names}")

    def export_identities(self, format, filename):
        if format == 'csv':
            self.identity_exporter.export_to_csv(self.generated_identities, filename)
        elif format == 'json':
            self.identity_exporter.export_to_json(self.generated_identities, filename)
        elif format == 'sql':
            self.identity_exporter.export_to_sql(self.generated_identities, filename)
        else:
            print("Invalid export format")

    def import_identities(self, format, filename):
        if format == 'csv':
            self.generated_identities = self.identity_importer.import_from_csv(filename)
        elif format == 'json':
            self.generated_identities = self.identity_importer.import_from_json(filename)
        elif format == 'sql':
            self.generated_identities = self.identity_importer.import_from_sql(filename)
        else:
            print("Invalid import format")

    def run(self):
        print("Fake Identity Generation System")
        print("===============================")
        
        while True:
            print("\nMenu:")
            print("1. Generate fake identities")
            print("2. Train machine learning model")
            print("3. Generate enhanced identity")
            print("4. Save identities to file")
            print("5. Generate fake ID card")
            print("6. Validate identity")
            print("7. Encrypt identities")
            print("8. Decrypt identities")
            print("9. Analyze identities")
            print("10. Export identities")
            print("11. Import identities")
            print("12. Exit")
            
            choice = input("Enter your choice (1-12): ")
            
            if choice == '1':
                num_identities = int(input("Enter the number of fake identities to generate: "))
                self.generate_identities(num_identities)
            
            elif choice == '2':
                self.train_model()
            
            elif choice == '3':
                enhanced_identity = self.generate_enhanced_identity()
                print("\nEnhanced Identity:")
                for key, value in enhanced_identity.items():
                    print(f"{key}: {value}")
            
            elif choice == '4':
                filename = input("Enter the filename to save identities: ")
                self.save_identities_to_file(filename)
            
            elif choice == '5':
                if not self.generated_identities:
                    print("No identities generated yet. Generate some identities first.")
                else:
                    index = int(input(f"Enter the index of the identity (0-{len(self.generated_identities)-1}): "))
                    if 0 <= index < len(self.generated_identities):
                        id_card = self.generate_fake_id_card(self.generated_identities[index])
                        print("\nFake ID Card:")
                        print(id_card)
                    else:
                        print("Invalid index.")
            
            elif choice == '6':
                if not self.generated_identities:
                    print("No identities generated yet. Generate some identities first.")
                else:
                    index = int(input(f"Enter the index of the identity to validate (0-{len(self.generated_identities)-1}): "))
                    if 0 <= index < len(self.generated_identities):
                        is_valid = self.validate_identity(self.generated_identities[index])
                        print(f"Identity is {'valid' if is_valid else 'invalid'}")
                    else:
                        print("Invalid index.")
            
            elif choice == '7':
                self.encrypt_identities()
                print("Identities encrypted successfully.")
            
            elif choice == '8':
                self.decrypt_identities()
                print("Identities decrypted successfully.")
            
            elif choice == '9':
                self.analyze_identities()
            
            elif choice == '10':
                format = input("Enter export format (csv/json/sql): ")
                filename = input("Enter filename for export: ")
                self.export_identities(format, filename)
            
            elif choice == '11':
                format = input("Enter import format (csv/json/sql): ")
                filename = input("Enter filename for import: ")
                self.import_identities(format, filename)
            
            elif choice == '12':
                print("Exiting the program. Goodbye!")
                break
            
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    system = FakeIdentitySystem()
    system.run()
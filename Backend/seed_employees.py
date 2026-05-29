import random
from database.db import get_connection


first_names = [
    "Martin", "Anna", "Jonas", "Sara", "Mikkel", "Emma", "Frederik", "Sofie",
    "Mathias", "Laura", "Andreas", "Julie", "Nikolaj", "Ida", "Christian",
    "Camilla", "Magnus", "Katrine", "Oliver", "Maria"
]

last_names = [
    "Hansen", "Nielsen", "Jensen", "Larsen", "Petersen", "Madsen",
    "Christensen", "Rasmussen", "Andersen", "Poulsen", "Johansen",
    "Møller", "Knudsen", "Olsen", "Pedersen"
]

departments = [
    "Cybersecurity",
    "Cloud Infrastructure",
    "Network Operations",
    "Software Engineering",
    "Service Desk",
    "Data & AI",
    "Project Management",
    "Consulting",
    "Finance",
    "HR"
]

roles = {
    "Cybersecurity": ["Security Analyst", "SOC Analyst", "Threat Hunter"],
    "Cloud Infrastructure": ["Cloud Engineer", "Azure Specialist"],
    "Network Operations": ["Network Engineer", "NOC Technician"],
    "Software Engineering": ["Frontend Developer", "Backend Developer"],
    "Service Desk": ["IT Support Specialist", "Service Desk Analyst"],
    "Data & AI": ["Data Analyst", "ML Engineer"],
    "Project Management": ["Project Manager", "Scrum Master"],
    "Consulting": ["IT Consultant", "Business Consultant"],
    "Finance": ["Finance Coordinator"],
    "HR": ["HR Consultant"]
}


def create_email(first_name, last_name, used_emails):
    base = f"{first_name.lower()}.{last_name.lower()}@dxc.com"
    base = base.replace("ø", "oe").replace("æ", "ae").replace("å", "aa")

    email = base
    counter = 1

    while email in used_emails:
        email = f"{first_name.lower()}.{last_name.lower()}{counter}@dxc.com"
        email = email.replace("ø", "oe").replace("æ", "ae").replace("å", "aa")
        counter += 1

    used_emails.add(email)
    return email


def seed_employees(amount=350):
    conn = get_connection()
    cursor = conn.cursor()

    used_emails = set()

    for _ in range(amount):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        full_name = f"{first_name} {last_name}"

        department = random.choice(departments)
        role = random.choice(roles[department])
        email = create_email(first_name, last_name, used_emails)

        cursor.execute("""
            INSERT INTO employees (
                full_name,
                email,
                department,
                role,
                location,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            full_name,
            email,
            department,
            role,
            "DXC Copenhagen",
            "ACTIVE"
        ))

    conn.commit()
    cursor.close()
    conn.close()

    print(f"{amount} employees inserted successfully.")


if __name__ == "__main__":
    seed_employees(350)
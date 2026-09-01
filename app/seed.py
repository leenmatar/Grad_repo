from sqlalchemy import select

from app.database import engine
from app.models import categories, ticket_solutions, tickets, users

with engine.begin() as connection:
    # --------------------------------
    # User
    # --------------------------------
    user_query = select(users.c.user_id).where(users.c.email == "test@example.com")

    user_id = connection.execute(user_query).scalar_one_or_none()

    if user_id is None:
        user_result = connection.execute(
            users.insert().values(
                full_name="Test User",
                email="test@example.com",
                role="Student",
            )
        )

        user_id = user_result.inserted_primary_key[0]

    # --------------------------------
    # Categories
    # --------------------------------
    category_names = [
        "Account",
        "Network",
        "Software",
        "Hardware",
        "Academic System",
    ]

    category_ids = {}

    for name in category_names:
        category_query = select(categories.c.category_id).where(
            categories.c.category_name == name
        )

        category_id = connection.execute(category_query).scalar_one_or_none()

        if category_id is None:
            category_result = connection.execute(
                categories.insert().values(
                    category_name=name,
                    description=f"{name} related technical issues",
                )
            )

            category_id = category_result.inserted_primary_key[0]

        category_ids[name] = category_id

    # --------------------------------
    # Historical resolved tickets
    # --------------------------------
    sample_tickets = [
        {
            "category": "Account",
            "title": "University Account Login Failure",
            "description": "Student cannot login to the university account.",
            "solution": "Reset the account password and try logging in again.",
        },
        {
            "category": "Network",
            "title": "Campus WiFi Connection Problem",
            "description": "Student cannot connect to the campus WiFi network.",
            "solution": "Forget the WiFi network and reconnect using university credentials.",
        },
        {
            "category": "Software",
            "title": "Application Keeps Crashing",
            "description": "The university application crashes when opened.",
            "solution": "Update the application and restart the computer.",
        },
        {
            "category": "Hardware",
            "title": "Laptop Keyboard Not Working",
            "description": "Several keys on the laptop keyboard are not working.",
            "solution": "Reconnect the keyboard driver and test the hardware.",
        },
        {
            "category": "Academic System",
            "title": "Student Portal Access Problem",
            "description": "Student cannot access the academic student portal.",
            "solution": "Reset the portal session and sign in again.",
        },
    ]

    # --------------------------------
    # Insert tickets and solutions
    # --------------------------------
    for item in sample_tickets:
        ticket_query = select(tickets.c.ticket_id).where(
            tickets.c.title == item["title"]
        )

        ticket_id = connection.execute(ticket_query).scalar_one_or_none()

        if ticket_id is None:
            ticket_result = connection.execute(
                tickets.insert().values(
                    user_id=user_id,
                    category_id=category_ids[item["category"]],
                    title=item["title"],
                    description=item["description"],
                    priority="Medium",
                    status="Resolved",
                )
            )

            ticket_id = ticket_result.inserted_primary_key[0]

        solution_query = select(ticket_solutions.c.solution_id).where(
            ticket_solutions.c.ticket_id == ticket_id
        )

        solution_id = connection.execute(solution_query).scalar_one_or_none()

        if solution_id is None:
            connection.execute(
                ticket_solutions.insert().values(
                    ticket_id=ticket_id,
                    solution_text=item["solution"],
                    is_verified=True,
                )
            )


print("Sample data is ready.")

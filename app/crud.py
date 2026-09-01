from datetime import datetime, timezone

from sqlalchemy import func, select

from app.database import engine
from app.models import (
    categories,
    status_history,
    ticket_analysis,
    tickets,
    users,
)

# -----------------------------
# Create User
# -----------------------------


def create_user(full_name, email, role):
    query = users.insert().values(
        full_name=full_name,
        email=email,
        role=role,
    )

    with engine.begin() as connection:
        result = connection.execute(query)

    return result.inserted_primary_key[0]


# -----------------------------
# Get Category ID
# -----------------------------


def get_category_id(category_name):
    query = select(categories.c.category_id).where(
        categories.c.category_name == category_name
    )

    with engine.connect() as connection:
        category_id = connection.execute(query).scalar_one_or_none()

    return category_id


# -----------------------------
# Create Ticket
# -----------------------------


def create_ticket(
    user_id,
    category_id,
    title,
    description,
    priority,
):
    with engine.begin() as connection:
        ticket_query = tickets.insert().values(
            user_id=user_id,
            category_id=category_id,
            title=title,
            description=description,
            priority=priority,
            status="Open",
        )

        result = connection.execute(ticket_query)

        ticket_id = result.inserted_primary_key[0]

        # Save initial status
        history_query = status_history.insert().values(
            ticket_id=ticket_id,
            old_status=None,
            new_status="Open",
            changed_at=datetime.now(timezone.utc),
        )

        connection.execute(history_query)

    return ticket_id


# -----------------------------
# Save AI Analysis
# -----------------------------


def save_ticket_analysis(
    ticket_id,
    predicted_category_id,
    confidence_score,
    detected_priority,
):
    query = ticket_analysis.insert().values(
        ticket_id=ticket_id,
        predicted_category_id=predicted_category_id,
        confidence_score=confidence_score,
        detected_priority=detected_priority,
        created_at=datetime.now(timezone.utc),
    )

    with engine.begin() as connection:
        result = connection.execute(query)

    return result.inserted_primary_key[0]


# -----------------------------
# Get Ticket Analysis
# -----------------------------


def get_ticket_analysis(ticket_id):
    query = (
        select(
            ticket_analysis.c.analysis_id,
            ticket_analysis.c.ticket_id,
            categories.c.category_name,
            ticket_analysis.c.confidence_score,
            ticket_analysis.c.detected_priority,
            ticket_analysis.c.created_at,
        )
        .select_from(
            ticket_analysis.join(
                categories,
                ticket_analysis.c.predicted_category_id == categories.c.category_id,
            )
        )
        .where(ticket_analysis.c.ticket_id == ticket_id)
        .order_by(ticket_analysis.c.created_at.desc())
    )

    with engine.connect() as connection:
        result = connection.execute(query)

        return [dict(row._mapping) for row in result]


# -----------------------------
# Get All Tickets
# -----------------------------


def get_tickets():
    query = tickets.select().order_by(tickets.c.created_at.desc())

    with engine.connect() as connection:
        result = connection.execute(query)

        return [dict(row._mapping) for row in result]


# -----------------------------
# Get One Ticket
# -----------------------------


def get_ticket(ticket_id):
    query = tickets.select().where(tickets.c.ticket_id == ticket_id)

    with engine.connect() as connection:
        result = connection.execute(query)

        row = result.fetchone()

    if row:
        return dict(row._mapping)

    return None


# -----------------------------
# Update Ticket
# -----------------------------


def update_ticket(
    ticket_id,
    title=None,
    description=None,
    priority=None,
    status=None,
    category_id=None,
):
    with engine.begin() as connection:
        # Get current ticket
        current_query = tickets.select().where(tickets.c.ticket_id == ticket_id)

        current_result = connection.execute(current_query)

        current_ticket = current_result.fetchone()

        if current_ticket is None:
            return False

        current_ticket = dict(current_ticket._mapping)

        old_status = current_ticket["status"]

        values = {}

        if title is not None:
            values["title"] = title

        if description is not None:
            values["description"] = description

        if priority is not None:
            values["priority"] = priority

        if status is not None:
            values["status"] = status

        if category_id is not None:
            values["category_id"] = category_id

        values["updated_at"] = datetime.now(timezone.utc)

        update_query = (
            tickets.update().where(tickets.c.ticket_id == ticket_id).values(**values)
        )

        connection.execute(update_query)

        # Save status change
        if status is not None and status != old_status:
            history_query = status_history.insert().values(
                ticket_id=ticket_id,
                old_status=old_status,
                new_status=status,
                changed_at=datetime.now(timezone.utc),
            )

            connection.execute(history_query)

    return True


# -----------------------------
# Delete Ticket
# -----------------------------


def delete_ticket(ticket_id):
    with engine.begin() as connection:
        # Delete status history
        connection.execute(
            status_history.delete().where(status_history.c.ticket_id == ticket_id)
        )

        # Delete AI analysis
        connection.execute(
            ticket_analysis.delete().where(ticket_analysis.c.ticket_id == ticket_id)
        )

        # Delete ticket
        result = connection.execute(
            tickets.delete().where(tickets.c.ticket_id == ticket_id)
        )

    return result.rowcount > 0


# -----------------------------
# Filter Tickets
# -----------------------------


def filter_tickets(
    category_id=None,
    priority=None,
    status=None,
):
    query = tickets.select()

    if category_id is not None:
        query = query.where(tickets.c.category_id == category_id)

    if priority is not None:
        query = query.where(tickets.c.priority == priority)

    if status is not None:
        query = query.where(tickets.c.status == status)

    query = query.order_by(tickets.c.created_at.desc())

    with engine.connect() as connection:
        result = connection.execute(query)

        return [dict(row._mapping) for row in result]


# -----------------------------
# User Ticket History
# -----------------------------


def get_ticket_history(user_id):
    query = (
        tickets.select()
        .where(tickets.c.user_id == user_id)
        .order_by(tickets.c.created_at.desc())
    )

    with engine.connect() as connection:
        result = connection.execute(query)

        return [dict(row._mapping) for row in result]


# -----------------------------
# Status History
# -----------------------------


def get_status_history(ticket_id):
    query = (
        status_history.select()
        .where(status_history.c.ticket_id == ticket_id)
        .order_by(status_history.c.changed_at.asc())
    )

    with engine.connect() as connection:
        result = connection.execute(query)

        return [dict(row._mapping) for row in result]


# -----------------------------
# Dashboard Statistics
# -----------------------------


def get_dashboard_stats():
    with engine.connect() as connection:
        total_tickets = connection.execute(
            select(func.count()).select_from(tickets)
        ).scalar_one()

        open_tickets = connection.execute(
            select(func.count()).select_from(tickets).where(tickets.c.status == "Open")
        ).scalar_one()

        resolved_tickets = connection.execute(
            select(func.count())
            .select_from(tickets)
            .where(tickets.c.status == "Resolved")
        ).scalar_one()

        category_query = (
            select(
                categories.c.category_name,
                func.count(tickets.c.ticket_id),
            )
            .select_from(
                categories.outerjoin(
                    tickets,
                    categories.c.category_id == tickets.c.category_id,
                )
            )
            .group_by(categories.c.category_name)
        )

        category_result = connection.execute(category_query)

        tickets_by_category = {row[0]: row[1] for row in category_result}

        priority_query = (
            select(
                tickets.c.priority,
                func.count(tickets.c.ticket_id),
            )
            .select_from(tickets)
            .group_by(tickets.c.priority)
        )

        priority_result = connection.execute(priority_query)

        tickets_by_priority = {row[0]: row[1] for row in priority_result}

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "resolved_tickets": resolved_tickets,
        "tickets_by_category": tickets_by_category,
        "tickets_by_priority": tickets_by_priority,
    }

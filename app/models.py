from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    LargeBinary,
    MetaData,
    String,
    Table,
    Text,
)

metadata = MetaData()


# -----------------------------
# Users
# -----------------------------

users = Table(
    "users",
    metadata,
    Column(
        "user_id",
        Integer,
        primary_key=True,
    ),
    Column(
        "full_name",
        String(100),
        nullable=False,
    ),
    Column(
        "email",
        String(150),
        nullable=False,
        unique=True,
    ),
    Column(
        "role",
        String(50),
        nullable=False,
    ),
)


# -----------------------------
# Categories
# -----------------------------

categories = Table(
    "categories",
    metadata,
    Column(
        "category_id",
        Integer,
        primary_key=True,
    ),
    Column(
        "category_name",
        String(100),
        nullable=False,
        unique=True,
    ),
    Column(
        "description",
        Text,
    ),
)


# -----------------------------
# Tickets
# -----------------------------

tickets = Table(
    "tickets",
    metadata,
    Column(
        "ticket_id",
        Integer,
        primary_key=True,
    ),
    Column(
        "user_id",
        Integer,
        ForeignKey("users.user_id"),
        nullable=False,
    ),
    Column(
        "category_id",
        Integer,
        ForeignKey("categories.category_id"),
    ),
    Column(
        "title",
        String(200),
        nullable=False,
    ),
    Column(
        "description",
        Text,
        nullable=False,
    ),
    Column(
        "priority",
        String(20),
        nullable=False,
    ),
    Column(
        "status",
        String(20),
        nullable=False,
        default="Open",
    ),
    Column(
        "created_at",
        DateTime,
        default=datetime.now,
    ),
    Column(
        "updated_at",
        DateTime,
        default=datetime.now,
    ),
)


# -----------------------------
# Ticket Analysis
# -----------------------------

ticket_analysis = Table(
    "ticket_analysis",
    metadata,
    Column(
        "analysis_id",
        Integer,
        primary_key=True,
    ),
    Column(
        "ticket_id",
        Integer,
        ForeignKey("tickets.ticket_id"),
        nullable=False,
    ),
    Column(
        "predicted_category_id",
        Integer,
        ForeignKey("categories.category_id"),
        nullable=False,
    ),
    Column(
        "confidence_score",
        Float,
        nullable=False,
    ),
    Column(
        "detected_priority",
        String(20),
        nullable=False,
    ),
    Column(
        "created_at",
        DateTime,
        default=datetime.now,
    ),
)


# -----------------------------
# Ticket Embeddings
# -----------------------------

ticket_embeddings = Table(
    "ticket_embeddings",
    metadata,
    Column(
        "ticket_id",
        Integer,
        ForeignKey("tickets.ticket_id"),
        primary_key=True,
    ),
    Column(
        "embedding",
        LargeBinary,
        nullable=False,
    ),
)


# -----------------------------
# Ticket Solutions
# -----------------------------

ticket_solutions = Table(
    "ticket_solutions",
    metadata,
    Column(
        "solution_id",
        Integer,
        primary_key=True,
    ),
    Column(
        "ticket_id",
        Integer,
        ForeignKey("tickets.ticket_id"),
        nullable=False,
    ),
    Column(
        "solution_text",
        Text,
        nullable=False,
    ),
    Column(
        "is_verified",
        Boolean,
        default=False,
    ),
)


# -----------------------------
# Status History
# -----------------------------

status_history = Table(
    "status_history",
    metadata,
    Column(
        "history_id",
        Integer,
        primary_key=True,
    ),
    Column(
        "ticket_id",
        Integer,
        ForeignKey("tickets.ticket_id"),
        nullable=False,
    ),
    Column(
        "old_status",
        String(20),
        nullable=True,
    ),
    Column(
        "new_status",
        String(20),
        nullable=False,
    ),
    Column(
        "changed_at",
        DateTime,
        default=datetime.now,
        nullable=False,
    ),
)

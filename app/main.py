from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.classifier import predict_category
from app.crud import (
    create_ticket,
    delete_ticket,
    filter_tickets,
    get_category_id,
    get_dashboard_stats,
    get_status_history,
    get_ticket,
    get_ticket_analysis,
    get_ticket_history,
    get_tickets,
    save_ticket_analysis,
    update_ticket,
)
from app.priority import detect_priority
from app.semantic_search import (
    create_ticket_embedding,
    find_similar_tickets,
)

# --------------------------------
# FastAPI Application
# --------------------------------

app = FastAPI(
    title="AI Support Ticket Intelligence Platform",
    version="1.0.0",
)


# --------------------------------
# CORS
# --------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------
# Pydantic Models
# --------------------------------


class TicketCreate(BaseModel):
    user_id: int
    title: str
    description: str


class TicketUpdate(BaseModel):
    category_id: int | None = None
    title: str | None = None
    description: str | None = None
    priority: str | None = None
    status: str | None = None


class TicketAnalyze(BaseModel):
    description: str


# --------------------------------
# Root
# --------------------------------


@app.get("/")
def root():

    return {"message": "AI Support Ticket Intelligence Platform API"}


# --------------------------------
# Create Ticket
# --------------------------------


@app.post("/api/tickets")
def add_ticket(ticket: TicketCreate):

    # --------------------------------
    # AI Category Prediction
    # --------------------------------

    predicted_category, confidence = predict_category(ticket.description)

    # --------------------------------
    # AI Priority Detection
    # --------------------------------

    priority = detect_priority(ticket.description)

    # --------------------------------
    # Get Category ID
    # --------------------------------

    category_id = get_category_id(predicted_category)

    if category_id is None:
        raise HTTPException(
            status_code=400,
            detail=("Predicted category does not exist in the database"),
        )

    # --------------------------------
    # Create Ticket
    # --------------------------------

    ticket_id = create_ticket(
        user_id=ticket.user_id,
        category_id=category_id,
        title=ticket.title,
        description=ticket.description,
        priority=priority,
    )

    # --------------------------------
    # Save Ticket Embedding
    # --------------------------------

    create_ticket_embedding(
        ticket_id=ticket_id,
        description=ticket.description,
    )

    # --------------------------------
    # Save AI Analysis
    # --------------------------------

    save_ticket_analysis(
        ticket_id=ticket_id,
        predicted_category_id=category_id,
        confidence_score=confidence,
        detected_priority=priority,
    )

    # --------------------------------
    # Response
    # --------------------------------

    return {
        "message": "Ticket created successfully",
        "ticket_id": ticket_id,
        "predicted_category": predicted_category,
        "confidence": confidence,
        "priority": priority,
    }


# --------------------------------
# Get All Tickets
# --------------------------------


@app.get("/api/tickets")
def list_tickets():

    return get_tickets()


# --------------------------------
# Filter Tickets
# --------------------------------


@app.get("/api/tickets/filter/")
def filter_ticket_list(
    category_id: int | None = None,
    priority: str | None = None,
    status: str | None = None,
):

    return filter_tickets(
        category_id=category_id,
        priority=priority,
        status=status,
    )


# --------------------------------
# Analyze Ticket
# --------------------------------


@app.post("/api/tickets/analyze")
def analyze_ticket(ticket: TicketAnalyze):

    predicted_category, confidence = predict_category(ticket.description)

    priority = detect_priority(ticket.description)

    return {
        "predicted_category": predicted_category,
        "confidence": confidence,
        "priority": priority,
    }


# --------------------------------
# Dashboard Statistics
# --------------------------------


@app.get("/api/dashboard/stats")
def dashboard_stats():

    return get_dashboard_stats()


# --------------------------------
# User Ticket History
# --------------------------------


@app.get("/api/users/{user_id}/tickets")
def ticket_history(user_id: int):

    return get_ticket_history(user_id)


# --------------------------------
# Get One Ticket
# --------------------------------


@app.get("/api/tickets/{ticket_id}")
def read_ticket(ticket_id: int):

    ticket = get_ticket(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    return ticket


# --------------------------------
# Ticket Status History
# --------------------------------


@app.get("/api/tickets/{ticket_id}/history")
def ticket_status_history(ticket_id: int):

    ticket = get_ticket(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    history = get_status_history(ticket_id)

    return {
        "ticket_id": ticket_id,
        "status_history": history,
    }


# --------------------------------
# Ticket AI Analysis
# --------------------------------


@app.get("/api/tickets/{ticket_id}/analysis")
def ticket_ai_analysis(ticket_id: int):

    ticket = get_ticket(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    analysis = get_ticket_analysis(ticket_id)

    return {
        "ticket_id": ticket_id,
        "analysis": analysis,
    }


# --------------------------------
# Similar Tickets
# --------------------------------


@app.get("/api/tickets/{ticket_id}/similar")
def similar_tickets(ticket_id: int):

    ticket = get_ticket(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    results = find_similar_tickets(
        ticket["description"],
        top_n=3,
    )

    return {
        "ticket_id": ticket_id,
        "similar_tickets": results,
    }


# --------------------------------
# Update Ticket
# --------------------------------


@app.put("/api/tickets/{ticket_id}")
def edit_ticket(
    ticket_id: int,
    ticket: TicketUpdate,
):

    updated = update_ticket(
        ticket_id=ticket_id,
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        status=ticket.status,
        category_id=ticket.category_id,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    return {"message": "Ticket updated successfully"}


# --------------------------------
# Delete Ticket
# --------------------------------


@app.delete("/api/tickets/{ticket_id}")
def remove_ticket(ticket_id: int):

    deleted = delete_ticket(ticket_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    return {"message": "Ticket deleted successfully"}

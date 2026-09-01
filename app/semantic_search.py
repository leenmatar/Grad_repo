import pickle

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import select

from app.database import engine
from app.models import (
    ticket_embeddings,
    ticket_solutions,
    tickets,
)

# ==========================================
# Load Sentence Transformer Model
# ==========================================

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# ==========================================
# Generate Embedding
# ==========================================


def generate_embedding(text):
    embedding = embedding_model.encode(
        text,
        convert_to_numpy=True,
    )

    return np.array(
        embedding,
        dtype=np.float32,
    )


# ==========================================
# Save Ticket Embedding
# ==========================================


def save_ticket_embedding(
    ticket_id,
    embedding,
):
    embedding_bytes = pickle.dumps(embedding)

    query = ticket_embeddings.insert().values(
        ticket_id=ticket_id,
        embedding=embedding_bytes,
    )

    with engine.begin() as connection:
        connection.execute(query)


# ==========================================
# Get Stored Embedding
# ==========================================


def get_ticket_embedding(ticket_id):

    query = select(ticket_embeddings.c.embedding).where(
        ticket_embeddings.c.ticket_id == ticket_id
    )

    with engine.connect() as connection:
        result = connection.execute(query)

        row = result.fetchone()

    if row is None:
        return None

    return pickle.loads(row.embedding)


# ==========================================
# Create / Update Ticket Embedding
# ==========================================


def create_ticket_embedding(
    ticket_id,
    description,
):

    embedding = generate_embedding(description)

    existing_embedding = get_ticket_embedding(ticket_id)

    if existing_embedding is None:
        save_ticket_embedding(
            ticket_id,
            embedding,
        )

    else:
        embedding_bytes = pickle.dumps(embedding)

        query = (
            ticket_embeddings.update()
            .where(ticket_embeddings.c.ticket_id == ticket_id)
            .values(embedding=embedding_bytes)
        )

        with engine.begin() as connection:
            connection.execute(query)

    return embedding


# ==========================================
# Get Resolved Tickets
# ==========================================


def get_resolved_tickets():

    query = (
        select(
            tickets.c.ticket_id,
            tickets.c.title,
            tickets.c.description,
            ticket_solutions.c.solution_text,
            ticket_embeddings.c.embedding,
        )
        .select_from(
            tickets.join(
                ticket_solutions,
                tickets.c.ticket_id == ticket_solutions.c.ticket_id,
            ).join(
                ticket_embeddings,
                tickets.c.ticket_id == ticket_embeddings.c.ticket_id,
            )
        )
        .where(tickets.c.status == "Resolved")
        .where(ticket_solutions.c.is_verified.is_(True))
    )

    with engine.connect() as connection:
        result = connection.execute(query)

        rows = []

        for row in result:
            ticket = dict(row._mapping)

            ticket["embedding"] = pickle.loads(ticket["embedding"])

            rows.append(ticket)

        return rows


# ==========================================
# Find Similar Tickets
# ==========================================


def find_similar_tickets(
    description,
    top_n=3,
):

    resolved_tickets = get_resolved_tickets()

    if not resolved_tickets:
        return []

    # Generate embedding for new ticket
    new_embedding = generate_embedding(description)

    results = []

    # Compare with stored embeddings
    for ticket in resolved_tickets:
        old_embedding = ticket["embedding"]

        similarity = cosine_similarity(
            [new_embedding],
            [old_embedding],
        )[0][0]

        results.append(
            {
                "ticket_id": ticket["ticket_id"],
                "title": ticket["title"],
                "description": ticket["description"],
                "similarity": round(
                    float(similarity) * 100,
                    2,
                ),
                "solution": ticket["solution_text"],
            }
        )

    # Highest similarity first
    results.sort(
        key=lambda item: item["similarity"],
        reverse=True,
    )

    # Return Top N
    return results[:top_n]


# ==========================================
# Test
# ==========================================

if __name__ == "__main__":
    results = find_similar_tickets("I cannot login to my university account")

    for ticket in results:
        print("\nTitle:", ticket["title"])

        print("Description:", ticket["description"])

        print("Similarity:", ticket["similarity"], "%")

        print("Solution:", ticket["solution"])

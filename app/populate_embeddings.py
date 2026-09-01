import pickle

from sqlalchemy import select

from app.database import engine
from app.models import ticket_embeddings, tickets
from app.semantic_search import generate_embedding


def populate_embeddings():

    query = select(
        tickets.c.ticket_id,
        tickets.c.description,
    )

    with engine.connect() as connection:
        result = connection.execute(query)
        existing_tickets = result.fetchall()

    print("Found tickets:", len(existing_tickets))

    for ticket in existing_tickets:
        ticket_id = ticket.ticket_id
        description = ticket.description

        # Check if embedding already exists
        check_query = select(ticket_embeddings.c.ticket_id).where(
            ticket_embeddings.c.ticket_id == ticket_id
        )

        with engine.connect() as connection:
            existing = connection.execute(check_query).fetchone()

        if existing:
            print(f"Ticket {ticket_id}: embedding already exists")

            continue

        # Generate embedding
        embedding = generate_embedding(description)

        # Convert embedding to bytes
        embedding_bytes = pickle.dumps(embedding)

        # Save embedding
        insert_query = ticket_embeddings.insert().values(
            ticket_id=ticket_id,
            embedding=embedding_bytes,
        )

        with engine.begin() as connection:
            connection.execute(insert_query)

        print(f"Ticket {ticket_id}: embedding created successfully")

    print("\nEmbedding population completed.")


if __name__ == "__main__":
    populate_embeddings()

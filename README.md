# Grad_repo
# AI Support Ticket Intelligence Platform

An AI-powered support ticket management platform that analyzes technical support requests, predicts their category and priority, finds similar historical tickets, and provides verified solutions.

## Project Overview

The AI Support Ticket Intelligence Platform combines machine learning, semantic search, PostgreSQL, FastAPI, and React to create an intelligent support ticket management system.

When a user submits a ticket, the system analyzes the ticket description and automatically predicts its category and priority. The ticket is then stored in PostgreSQL together with its AI analysis, status history, and semantic embedding.

The system can also search previously resolved tickets using Sentence Transformers and cosine similarity. It returns the Top 3 most similar resolved tickets and displays their verified solutions.

## Main Features

- AI ticket category classification
- Automatic priority detection
- Ticket creation
- Ticket viewing
- Ticket updating
- Ticket deletion
- Ticket status management
- Ticket status history
- AI analysis storage
- Semantic similarity search
- Top 3 similar resolved tickets
- Verified solution retrieval
- Ticket embeddings stored in PostgreSQL
- User ticket history
- Category filtering
- Priority filtering
- Status filtering
- Dashboard statistics
- React frontend
- FastAPI backend
- PostgreSQL database
- SQLAlchemy Core
- Alembic migrations
- Machine learning model saved with Joblib

## Technologies

### Backend

- Python
- FastAPI
- SQLAlchemy Core
- PostgreSQL
- Alembic
- Pydantic

### Machine Learning

- Scikit-learn
- TF-IDF
- Logistic Regression
- Joblib
- Pandas
- NumPy

### Semantic Search

- Sentence Transformers
- all-MiniLM-L6-v2
- Cosine Similarity

### Frontend

- React
- JavaScript
- CSS

### Code Quality

- Ruff

## System Architecture

The system follows this workflow:

User → React Frontend → FastAPI Backend → AI Classification and Priority Detection → PostgreSQL Database → Semantic Search → Similar Resolved Tickets → Verified Solutions

## Machine Learning Classification

The ticket classification system uses a supervised machine learning pipeline based on TF-IDF and Logistic Regression.

The classification process is:

Ticket Description → Text Preprocessing → TF-IDF Feature Extraction → Logistic Regression → Predicted Category → Confidence Score

The system supports five ticket categories:

- Account
- Network
- Software
- Hardware
- Academic System

## Text Preprocessing

Before training the classifier, ticket descriptions are cleaned by converting text to lowercase, removing non-alphabetic characters, and removing extra whitespace.

The cleaned text is then passed to the TF-IDF vectorizer.

## TF-IDF

TF-IDF is used to convert ticket descriptions into numerical feature vectors.

The vectorizer uses unigrams and bigrams, allowing the model to learn individual words as well as combinations of words such as university account, campus wifi, student portal, printer working, and application crashing.

## Logistic Regression

Logistic Regression is used as the classification algorithm.

The model predicts one of the five supported categories and provides a probability-based confidence score.

The trained model and TF-IDF vectorizer are saved together using Joblib.

The saved model is located at:

saved_model/ticket_classifier.joblib

## Model Training

The training dataset contains 100 examples with balanced categories:

Account: 20  
Network: 20  
Software: 20  
Hardware: 20  
Academic System: 20

The dataset is divided into 80 training samples and 20 testing samples.

The current model evaluation produced:

Accuracy: 0.80  
Precision: 0.87  
Recall: 0.80  
F1-score: 0.77

The model is evaluated using Accuracy, Precision, Recall, F1-score, Confusion Matrix, and Classification Report.

## Training the Model

To retrain the classification model, run:

python -m app.train_model

The trained model is saved to:

saved_model/ticket_classifier.joblib

## Priority Detection

The system automatically detects the priority of a support ticket based on its description.

Supported priorities are:

- Low
- Medium
- High
- Critical

The detected priority is stored together with the ticket and its AI analysis.

## Semantic Search

The platform uses semantic search to find previously resolved tickets that are similar to a newly submitted ticket.

The Sentence Transformer model used is:

sentence-transformers/all-MiniLM-L6-v2

The system converts ticket descriptions into numerical embeddings.

These embeddings are stored in PostgreSQL in the ticket_embeddings table.

## Semantic Search Pipeline

The semantic search workflow is:

New Ticket Description → Sentence Transformer → New Ticket Embedding → Stored Historical Embeddings → Cosine Similarity → Sort by Similarity → Top 3 Similar Resolved Tickets → Verified Solutions

Only resolved tickets with verified solutions are considered for the final semantic-search results.

Each similar-ticket result contains:

- Ticket ID
- Title
- Description
- Similarity percentage
- Verified solution

## Ticket Embeddings

Every newly created ticket receives a semantic embedding.

The embedding is stored in the PostgreSQL database.

Existing tickets can be populated with embeddings using:

python -m app.populate_embeddings

The embedding table contains one embedding for each ticket.

## Verified Solutions

The system stores solutions in the ticket_solutions table.

Each solution contains:

- Solution ID
- Ticket ID
- Solution text
- Verification status

Only solutions marked as verified are returned by semantic search.

Example:

Ticket: Campus WiFi Connection Problem

Verified Solution: Forget the WiFi network and reconnect using university credentials.

## Ticket Status History

The platform keeps a history of ticket status changes.

Supported statuses include:

- Open
- In Progress
- Resolved

For example:

Open → In Progress → Resolved

Each status change is stored in the status_history table.

The system records:

- History ID
- Ticket ID
- Old status
- New status
- Change timestamp

When a new ticket is created, its initial status is recorded as:

NULL → Open

If the ticket is later updated:

Open → In Progress

another history record is created.

## Database

The project uses PostgreSQL as the main relational database.

SQLAlchemy Core is used for database operations.

The database contains the following tables:

- users
- categories
- tickets
- ticket_analysis
- ticket_embeddings
- ticket_solutions
- status_history
- alembic_version

## Database Tables

### users

Stores information about system users.

Fields include:

- user_id
- full_name
- email
- role

### categories

Stores the available support ticket categories.

Fields include:

- category_id
- category_name
- description

### tickets

Stores submitted support tickets.

Important fields include:

- ticket_id
- user_id
- category_id
- title
- description
- priority
- status
- created_at
- updated_at

### ticket_analysis

Stores AI analysis results.

Fields include:

- analysis_id
- ticket_id
- predicted_category_id
- confidence_score
- detected_priority
- created_at

### ticket_embeddings

Stores semantic embeddings for ticket descriptions.

Fields include:

- ticket_id
- embedding

### ticket_solutions

Stores solutions associated with tickets.

Fields include:

- solution_id
- ticket_id
- solution_text
- is_verified

### status_history

Stores changes made to ticket statuses.

Fields include:

- history_id
- ticket_id
- old_status
- new_status
- changed_at

## FastAPI Backend

FastAPI is used to provide the REST API for the application.

The backend handles:

- Ticket management
- AI classification
- Priority detection
- AI analysis
- Semantic search
- Status history
- Dashboard statistics
- Ticket filtering

## API Endpoints

### Root

GET /

Returns information about the API.

### Create Ticket

POST /api/tickets

Creates a new ticket and automatically predicts the category, detects the priority, creates the ticket, saves the AI analysis, generates the ticket embedding, and stores the embedding.

### Get All Tickets

GET /api/tickets

Returns all tickets.

### Get One Ticket

GET /api/tickets/{ticket_id}

Returns the details of a specific ticket.

### Update Ticket

PUT /api/tickets/{ticket_id}

Updates ticket information such as title, description, category, priority, and status.

Status changes are automatically recorded in the status history.

### Delete Ticket

DELETE /api/tickets/{ticket_id}

Deletes a ticket.

### Filter Tickets

GET /api/tickets/filter/

Supports filtering by category, priority, and status.

Example:

/api/tickets/filter/?status=Open

### Analyze Ticket

POST /api/tickets/analyze

Analyzes a ticket description without creating a ticket.

The response contains the predicted category, confidence, and priority.

### Get AI Analysis

GET /api/tickets/{ticket_id}/analysis

Returns the stored AI analysis for a ticket.

### Get User Ticket History

GET /api/users/{user_id}/tickets

Returns tickets submitted by a specific user.

### Get Status History

GET /api/tickets/{ticket_id}/history

Returns all status changes for a ticket.

Example:

NULL → Open  
Open → In Progress  
In Progress → Resolved

### Find Similar Tickets

GET /api/tickets/{ticket_id}/similar

Returns the Top 3 most similar resolved tickets with verified solutions.

### Dashboard Statistics

GET /api/dashboard/stats

Returns total tickets, open tickets, resolved tickets, tickets by category, and tickets by priority.

## FastAPI Documentation

After starting the backend, the interactive API documentation is available at:

http://127.0.0.1:8000/docs

The documentation allows API endpoints to be tested directly through Swagger UI.

## React Frontend

The frontend is built using React.

The React application provides the main user interface for the support ticket platform.

### Main Frontend Features

- Ticket submission
- Ticket analysis
- Ticket list
- Ticket details
- Ticket editing
- Ticket deletion
- Category filters
- Priority filters
- Status filters
- Dashboard statistics
- User ticket history
- Status history
- Similar resolved tickets
- Verified solutions

## Dashboard

The dashboard displays statistics retrieved from the FastAPI backend.

It includes:

### Total Tickets

Shows the total number of tickets in the database.

### Open Tickets

Shows tickets currently marked as Open.

### Resolved Tickets

Shows tickets currently marked as Resolved.

### Tickets by Category

Displays the number of tickets in each category:

- Account
- Network
- Software
- Hardware
- Academic System

### Tickets by Priority

Displays the number of tickets for each priority.

### Ticket Status

Displays the distribution of ticket statuses.

## Example Ticket Workflow

A complete ticket workflow is:

1. User submits a support ticket.
2. AI predicts the category.
3. AI detects the priority.
4. Ticket is stored in PostgreSQL.
5. AI analysis is stored.
6. Ticket embedding is generated.
7. Embedding is stored.
8. Similar resolved tickets are searched.
9. Top 3 similar tickets are returned.
10. Verified solutions are displayed.
11. Support staff updates the ticket status.
12. Status change is stored in history.

## Example

A user submits:

Title: Printer Not Working

Description: The printer in the university lab is not responding and I cannot print my assignment.

The system analyzes the ticket and predicts a category, confidence score, priority, and status.

Example result:

Predicted Category: Hardware  
Confidence: 35.12%  
Priority: Low  
Status: Open

The system then searches historical resolved tickets and returns similar tickets with their verified solutions.

## Project Structure

Grad_repo/

app/
- classifier.py
- crud.py
- database.py
- main.py
- models.py
- populate_embeddings.py
- priority.py
- seed.py
- semantic_search.py
- train_model.py

alembic/
- versions/

data/
- tickets.csv

frontend/
- React application

saved_model/
- ticket_classifier.joblib

alembic.ini  
requirements.txt  
README.md

## Installation

### 1. Clone the Repository

git clone <YOUR_GITHUB_REPOSITORY_URL>

Navigate into the project:

cd Grad_repo

### 2. Create Virtual Environment

python3 -m venv venv

Activate it:

source venv/bin/activate

### 3. Install Python Dependencies

pip install -r requirements.txt

## PostgreSQL Setup

Create the PostgreSQL database:

support_ticket_db

Configure the database connection in the project according to your local PostgreSQL credentials.

## Run Database Migrations

Apply all Alembic migrations:

alembic upgrade head

## Seed the Database

Run:

python -m app.seed

This creates the initial users, categories, tickets, and verified solutions.

## Train the Model

Run:

python -m app.train_model

The model will be saved to:

saved_model/ticket_classifier.joblib

## Populate Existing Embeddings

For existing tickets, run:

python -m app.populate_embeddings

This generates and stores embeddings for tickets that do not already have an embedding.

## Run FastAPI

Activate the virtual environment:

source venv/bin/activate

Start the backend:

uvicorn app.main:app --reload

The backend will run at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs

## Run React

Open another terminal.

Navigate to the frontend:

cd frontend

Install the frontend dependencies:

npm install

Start the development server:

npm run dev

The React application provides the user interface and communicates with the FastAPI backend.

## Code Quality

Ruff is used to check and format the Python code.

Check the project:

ruff check .

Format the project:

ruff format .

A successful check should return:

All checks passed!

## Testing the System

The system can be tested through the React frontend or FastAPI Swagger documentation.

Recommended test cases include:

### Account

I cannot login to my university account.

Expected category: Account

### Network

My laptop cannot connect to the university WiFi.

Expected category: Network

### Software

The university application keeps crashing.

Expected category: Software

### Hardware

The printer in the university lab is not responding.

Expected category: Hardware

### Academic System

I cannot access the student portal.

Expected category: Academic System

## Final Project Status

The platform includes the main required components:

- PostgreSQL database
- SQLAlchemy Core
- Alembic migrations
- Ticket CRUD
- AI classification
- TF-IDF
- Logistic Regression
- Model evaluation
- Joblib model saving
- Priority detection
- Sentence Transformer embeddings
- Stored ticket embeddings
- Cosine similarity
- Top 3 similar tickets
- Verified solutions
- Status history
- FastAPI backend
- React frontend
- Dashboard
- Ticket filtering
- User ticket history
- Code quality with Ruff

## Conclusion

The AI Support Ticket Intelligence Platform provides an intelligent workflow for managing technical support requests.

By combining machine learning classification, automatic priority detection, semantic similarity search, verified solutions, PostgreSQL storage, FastAPI APIs, and a React interface, the system helps support staff analyze and manage tickets more efficiently.
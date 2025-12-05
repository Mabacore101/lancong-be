# Tourism Cuy KG Backend

A FastAPI-based knowledge graph backend for tourism data, powered by Neo4j graph database. This API provides endpoints for searching places, querying tourism packages, and exploring tourism-related information through a graph database.

## Overview

This project implements a REST API that interfaces with a Neo4j knowledge graph containing tourism data. It provides semantic search capabilities, package management, and flexible query execution for tourism places and related entities.

### Key Features

#### Mandatory Features ✅
- **Place Search**: Search for tourism places by name with fuzzy matching
- **InfoBox**: Retrieve detailed information about specific places
- **Package Management**: Browse tourism packages and their included places
- **Query Console**: Execute custom Cypher queries against the knowledge graph

#### Advanced Features ✅
- **Vector Embedding**: Semantic representation of places using sentence transformers
- **Semantic Search**: AI-powered search using vector similarity
- **Reranking**: Cross-encoder model for improved search result relevance
- **Graph Database**: Neo4j-powered knowledge graph for complex relationship queries

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Neo4j**: Graph database for storing and querying tourism data
- **Python 3.x**: Core programming language
- **Sentence Transformers**: For semantic search capabilities (planned)
- **Uvicorn**: ASGI server for running the application

## Project Structure

```
KG Local/
├── config.py                      # Configuration and environment variables
├── main.py                        # FastAPI application entry point
├── embedding.py                   # Script to generate embeddings for all places
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── RERANKING_TEST.md             # Reranking testing guide
├── RERANKING_EXAMPLES.md         # Reranking comparison examples
├── .env                          # Environment variables (not in git)
├── .gitignore                    # Git ignore rules
├── database/
│   └── neo4j_connection.py       # Neo4j database connection handler
├── models/
│   └── schemas.py                # Pydantic models for data validation
├── routers/
│   ├── infobox.py                # InfoBox endpoint routes
│   ├── packages.py               # Package management routes
│   ├── query_console.py          # Query console routes
│   └── search.py                 # Search endpoints (keyword, semantic, reranking)
└── services/
    ├── neo4j_service.py          # Neo4j service layer
    ├── package_service.py        # Package business logic
    ├── place_service.py          # Place business logic
    ├── search_service.py         # Search business logic (semantic + reranking)
    ├── reranking_service.py      # Reranking service with cross-encoder
    └── wikidata.py               # External KG integration (WikiData)
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Neo4j Database (local or remote instance)
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "KG Local"
   ```

2. **Create a virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root with the following content:
   ```env
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_password_here
   ```
   
   Replace `your_password_here` with your actual Neo4j password.

5. **Set up Neo4j database**
   - Install Neo4j Desktop or use a Neo4j cloud instance
   - Start the database
   - Ensure it's running on the URI specified in `.env`
   - Import your tourism data into the database

### Running the Application

Start the development server with auto-reload:

```powershell
uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

### API Documentation

Once the server is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

### Search
- `GET /search/?query={query}` - Basic keyword search for places by name
- `GET /search/semanticly?query={query}&k={k}` - Semantic search using vector embeddings
- `GET /search/rerank?query={query}&initial_k={initial_k}&top_k={top_k}` - Semantic search with reranking
- `GET /search/rerank-advanced?query={query}&initial_k={initial_k}&top_k={top_k}&use_description={bool}` - Advanced reranking with description

### InfoBox
- `GET /infobox/{place_id}` - Get detailed information about a place

### Packages
- `GET /packages/` - List all tourism packages
- `GET /packages/{package_id}/places` - Get places included in a package

### Query Console
- `POST /query/` - Execute custom Cypher queries
  ```json
  {
    "cypher": "MATCH (p:Place) RETURN p LIMIT 10"
  }
  ```

## Advanced Features Details

### Vector Embedding
All tourism places are embedded using `sentence-transformers/all-MiniLM-L6-v2` model. Embeddings are stored in Neo4j for efficient vector similarity search.

**Setup:**
```bash
python embedding.py
```

This will:
1. Load all places from Neo4j
2. Generate embeddings for each place name
3. Store embeddings back to Neo4j

### Semantic Search (`/search/semanticly`)
Uses bi-encoder model for fast semantic similarity search:
- Fast retrieval (~50-100ms)
- Handles synonyms and related concepts
- Uses Neo4j vector index for efficient querying

### Reranking (`/search/rerank`)
Two-stage retrieval for improved accuracy:

**Stage 1 - Candidate Retrieval:**
- Vector search retrieves initial_k candidates (default: 20)
- Fast bi-encoder model (all-MiniLM-L6-v2)

**Stage 2 - Reranking:**
- Cross-encoder model (`cross-encoder/ms-marco-MiniLM-L-6-v2`) scores each candidate
- More accurate but slower
- Returns top_k best results (default: 5)

**Performance:**
- Speed: ~200-500ms (depends on initial_k)
- Accuracy: Higher precision than vector search alone
- Trade-off: Speed vs accuracy via initial_k parameter

**Advanced Mode:**
- Considers both name and description
- Weighted scoring (70% name, 30% description by default)
- Best for descriptive queries like "tempat wisata alam dengan air terjun"

## Database Schema

The Neo4j database contains the following node types and relationships:

### Nodes
- **Place**: Tourism destinations (properties: id, name, city, category, rating)
- **Package**: Tourism packages (properties: id, name, description, price)

### Relationships
- `(Package)-[:INCLUDES]->(Place)`: Links packages to their included places

## Features Status

### ✅ Implemented (Mandatory)
1. **Search**: Basic keyword search with fuzzy matching
2. **InfoBox**: Detailed place information display
3. **Query Console**: Execute custom Cypher queries
4. **Packages**: Browse tourism packages and their places

### ✅ Implemented (Advanced/Bonus)
5. **Vector Embedding**: All places embedded using sentence transformers
6. **Semantic Search**: AI-powered search using vector similarity
7. **Reranking**: Cross-encoder for improved result relevance (Stage 1 & 2 retrieval)

### 🔄 To Be Implemented (Optional Enhancement)

#### High Priority
1. **External Knowledge Graph Integration**: Link with DBpedia/Wikidata (partially done with WikiData service)
2. **Enhanced Place Models**: Extend `models/schemas.py` with more detailed schemas
3. **Error Handling**: Implement comprehensive error handling and validation
4. **Filtering**: Advanced filtering for place search (by category, rating, city)

#### Medium Priority
5. **Question Answering**: Natural language QA system over knowledge graph
6. **RAG Chatbot**: Combine KG with LLM for conversational interface
7. **Recommendation System**: Place recommendation based on user preferences
8. **Graph Analytics**: Endpoints for graph statistics and analytics
9. **Pagination**: Implement pagination for list endpoints

#### Low Priority
10. **Testing**: Unit tests and integration tests
11. **Docker**: Containerize the application
12. **CI/CD**: Set up continuous integration and deployment
13. **Caching**: Add Redis caching for frequently accessed data
14. **Authentication**: Add API authentication and authorization
15. **Monitoring**: Add application monitoring and metrics

## Development Notes

- The `.env` file format should be `KEY=value` without quotes around keys
- Use `load_dotenv()` to load environment variables before accessing them
- All file paths should use absolute paths when calling tools
- The Neo4j connection is established lazily on first query


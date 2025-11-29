# Tourism Cuy KG Backend

A FastAPI-based knowledge graph backend for tourism data, powered by Neo4j graph database. This API provides endpoints for searching places, querying tourism packages, and exploring tourism-related information through a graph database.

## Overview

This project implements a REST API that interfaces with a Neo4j knowledge graph containing tourism data. It provides semantic search capabilities, package management, and flexible query execution for tourism places and related entities.

### Key Features

- **Place Search**: Search for tourism places by name with fuzzy matching
- **InfoBox**: Retrieve detailed information about specific places
- **Package Management**: Browse tourism packages and their included places
- **Query Console**: Execute custom Cypher queries against the knowledge graph
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
├── config.py                 # Configuration and environment variables
├── main.py                   # FastAPI application entry point
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not in git)
├── .gitignore               # Git ignore rules
├── database/
│   └── neo4j_connection.py  # Neo4j database connection handler
├── models/
│   └── schemas.py           # Pydantic models for data validation
├── routers/
│   ├── infobox.py           # InfoBox endpoint routes
│   ├── packages.py          # Package management routes
│   ├── query_console.py     # Query console routes
│   └── search.py            # Search endpoint routes
└── services/
    ├── neo4j_service.py     # Neo4j service layer (to be implemented)
    ├── package_service.py   # Package business logic
    ├── place_service.py     # Place business logic
    └── search_service.py    # Search business logic
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
- `GET /search/?query={query}` - Search for places by name

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

## Database Schema

The Neo4j database contains the following node types and relationships:

### Nodes
- **Place**: Tourism destinations (properties: id, name, city, category, rating)
- **Package**: Tourism packages (properties: id, name, description, price)

### Relationships
- `(Package)-[:INCLUDES]->(Place)`: Links packages to their included places

## To Be Implemented

The following features and files are planned or need implementation:

### High Priority
1. **Semantic Search**: Integrate sentence-transformers for semantic search capabilities
2. **Neo4j Service Layer** (`services/neo4j_service.py`): Create reusable Neo4j query functions
3. **Enhanced Place Models**: Extend `models/schemas.py` with more detailed schemas
4. **Error Handling**: Implement comprehensive error handling and validation
5. **Authentication**: Add API authentication and authorization

### Medium Priority
6. **Recommendation System**: Implement place recommendation based on user preferences
7. **Graph Analytics**: Add endpoints for graph statistics and analytics
8. **Filtering**: Advanced filtering for place search (by category, rating, city)
9. **Pagination**: Implement pagination for list endpoints
10. **Caching**: Add Redis caching for frequently accessed data

### Low Priority
11. **Testing**: Unit tests and integration tests
12. **Docker**: Containerize the application
13. **CI/CD**: Set up continuous integration and deployment
14. **Logging**: Implement structured logging
15. **Monitoring**: Add application monitoring and metrics

## Development Notes

- The `.env` file format should be `KEY=value` without quotes around keys
- Use `load_dotenv()` to load environment variables before accessing them
- All file paths should use absolute paths when calling tools
- The Neo4j connection is established lazily on first query

## Contributing

When contributing to this project:
1. Follow PEP 8 style guidelines
2. Add docstrings to new functions and classes
3. Update this README if adding new features
4. Test endpoints using the Swagger UI at `/docs`

## License

[Add your license information here]

## Contact

[Add contact information here]

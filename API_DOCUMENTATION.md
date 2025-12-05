# Tourism Cuy API Documentation
**Backend-Frontend Integration Guide**

Base URL: `http://localhost:8000` (Development)  
Version: 1.0.0

---

## 📋 Table of Contents
1. [Search Endpoints](#search-endpoints)
2. [Places Endpoint](#places-endpoint)
3. [InfoBox Endpoint](#infobox-endpoint)
4. [Package Endpoints](#package-endpoints)
5. [Query Console Endpoint](#query-console-endpoint)
6. [Response Format](#response-format)
7. [Error Handling](#error-handling)
8. [Integration Examples](#integration-examples)

---

## 🔍 Search Endpoints

### 1. Basic Keyword Search
**GET** `/search/`

Simple keyword-based search. Fastest but limited to exact/partial name matching. Results are enriched with Wikidata by default.

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | ✅ Yes | - | Search keyword |
| `enrich` | boolean | ❌ No | true | Enrich with Wikidata (image, entity, description) |
| `max_enrich` | integer | ❌ No | 5 | Maximum results to enrich (for performance) |

**Example Request:**
```http
GET /search/?query=museum&enrich=true&max_enrich=5
```

**Example Response:**
```json
[
  {
    "place": {
      "id": 1,
      "name": "Museum Fatahillah",
      "description": "Museum Sejarah Jakarta...",
      "category": "Budaya",
      "city": "Jakarta",
      "price": 5000,
      "rating": 4.5,
      "time_minutes": 120,
      "lat": -6.135,
      "long": 106.814,
      "image": "http://commons.wikimedia.org/wiki/Special:FilePath/Museum%20Fatahillah.jpg",
      "wikidata_entity": "http://www.wikidata.org/entity/Q12345",
      "description_id": "Museum sejarah di Jakarta"
    }
  }
]
```

**Use Case:** Quick autocomplete, simple searches  
**Performance:** ~10-30ms (without enrichment), ~50-100ms (with enrichment)

---

### 2. Semantic Search
**GET** `/search/semanticly`

AI-powered semantic search using vector embeddings. Understands meaning, not just keywords. Results are enriched with Wikidata by default.

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | ✅ Yes | - | Search query (natural language) |
| `k` | integer | ❌ No | 5 | Number of results to return |
| `enrich` | boolean | ❌ No | true | Enrich with Wikidata (image, entity, description) |

**Example Request:**
```http
GET /search/semanticly?query=monumen&k=5&enrich=true
```

**Example Response:**
```json
[
  {
    "place": {
      "id": 1,
      "name": "Monumen Nasional",
      "description": "...",
      "category": "Budaya",
      "city": "Jakarta",
      "price": 20000,
      "rating": 4.6,
      "vector_score": 0.8523,
      "image": "http://commons.wikimedia.org/wiki/Special:FilePath/Monas.jpg",
      "wikidata_entity": "http://www.wikidata.org/entity/Q67890",
      "description_id": "Monumen ikonik di Jakarta"
    }
  }
]
```

**Additional Fields:**
- `vector_score`: Similarity score (0-1, higher = more similar)
- `image`: Wikidata image URL (if enriched)
- `wikidata_entity`: Wikidata entity URI (if enriched)
- `description_id`: Indonesian description from Wikidata (if enriched)

**Use Case:** General search, handles typos and synonyms  
**Performance:** ~50-100ms (without enrichment), ~150-200ms (with enrichment)

---

### 3. Semantic Search with Reranking
**GET** `/search/rerank`

Two-stage retrieval: fast vector search + accurate cross-encoder reranking. Results are automatically enriched with Wikidata.

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | ✅ Yes | - | Search query |
| `initial_k` | integer | ❌ No | 20 | Initial candidates from vector search |
| `top_k` | integer | ❌ No | 5 | Final results after reranking |

**Example Request:**
```http
GET /search/rerank?query=museum sejarah&initial_k=20&top_k=5
```

**Example Response:**
```json
[
  {
    "place": {
      "id": 1,
      "name": "Museum Fatahillah",
      "description": "Museum Sejarah Jakarta...",
      "category": "Budaya",
      "city": "Jakarta",
      "price": 5000,
      "rating": 4.5,
      "vector_score": 0.7823,
      "rerank_score": 14.52,
      "image": "http://commons.wikimedia.org/wiki/Special:FilePath/Museum%20Fatahillah.jpg",
      "wikidata_entity": "http://www.wikidata.org/entity/Q12345",
      "description_id": "Museum sejarah di Jakarta"
    }
  }
]
```

**Additional Fields:**
- `vector_score`: Initial similarity score
- `rerank_score`: Cross-encoder relevance score (higher = more relevant)
- `image`: Wikidata image URL
- `wikidata_entity`: Wikidata entity URI
- `description_id`: Indonesian description from Wikidata

**Use Case:** Main search results, precise ranking needed  
**Performance:** ~200-500ms (includes automatic Wikidata enrichment)

**Tuning Tips:**
- `initial_k=10, top_k=3`: Faster (~150ms)
- `initial_k=50, top_k=10`: More comprehensive (~600ms)

---

### 4. Advanced Reranking with Description
**GET** `/search/rerank-advanced`

Considers both name AND description for matching. Best for descriptive queries. Results are automatically enriched with Wikidata.

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | ✅ Yes | - | Descriptive search query |
| `initial_k` | integer | ❌ No | 20 | Initial candidates |
| `top_k` | integer | ❌ No | 5 | Final results |
| `use_description` | boolean | ❌ No | true | Include description in matching |

**Example Request:**
```http
GET /search/rerank-advanced?query=tempat wisata dengan pemandangan laut&top_k=5&use_description=true
```

**Example Response:**
```json
[
  {
    "place": {
      "id": 15,
      "name": "Pulau Pelangi",
      "description": "Resort dengan pohon rimbun menghadap laut biru...",
      "category": "Bahari",
      "city": "Jakarta",
      "price": 900000,
      "rating": 4.8,
      "vector_score": 0.7145,
      "name_score": 8.52,
      "description_score": 12.34,
      "rerank_score": 9.63,
      "image": "http://commons.wikimedia.org/wiki/Special:FilePath/Pulau%20Pelangi.jpg",
      "wikidata_entity": "http://www.wikidata.org/entity/Q54321",
      "description_id": "Pulau resort di Kepulauan Seribu"
    }
  }
]
```

**Additional Fields:**
- `name_score`: Relevance score from name matching
- `description_score`: Relevance score from description matching
- `rerank_score`: Combined score (70% name + 30% description)
- `image`: Wikidata image URL
- `wikidata_entity`: Wikidata entity URI
- `description_id`: Indonesian description from Wikidata

**Use Case:** Complex/descriptive queries, detailed searches  
**Performance:** ~300-800ms (includes automatic Wikidata enrichment)

**Best For:**
- "tempat wisata alam dengan air terjun"
- "museum sejarah kolonial belanda"
- "pantai untuk snorkeling dan diving"

---

## 📍 Places Endpoint

### Get Place by ID
**GET** `/places/{place_id}`

Get basic information about a specific place by its ID.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `place_id` | integer | ✅ Yes | Unique place identifier |

**Example Request:**
```http
GET /places/1
```

**Example Response:**
```json
{
  "id": 1,
  "name": "Monumen Nasional",
  "description": "Monumen Nasional atau yang populer disingkat dengan Monas...",
  "category": "Budaya",
  "city": "Jakarta",
  "price": 20000,
  "rating": 4.6,
  "time_minutes": 15,
  "lat": -6.1753924,
  "long": 106.8271528
}
```

**Error Response (404):**
```json
{
  "detail": "Place not found"
}
```

**Use Case:** Simple place information retrieval  
**Performance:** ~15-30ms

---

## 📦 InfoBox Endpoint

### Get Place Details with Related Data
**GET** `/infobox/{place_id}`

Get complete information about a specific place including related places and packages.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `place_id` | integer | ✅ Yes | Unique place identifier |

**Example Request:**
```http
GET /infobox/1
```

**Example Response:**
```json
{
  "id": 2,
  "name": "Kota Tua",
  "description": "Kota tua di Jakarta, yang juga bernama Kota Tua, berpusat di Alun-Alun Fatahillah...",
  "category": "Budaya",
  "city": "Jakarta",
  "price": 0,
  "rating": 4.6,
  "time_minutes": 90,
  "lat": -6.1376448,
  "long": 106.8171245,
  "image": "http://commons.wikimedia.org/wiki/Special:FilePath/Dome%20of%20the%20Rock%20by%20Peter%20Mulligan.jpg",
  "wikidata_entity": "http://www.wikidata.org/entity/Q213274",
  "description_id": "kota di Palestina"
}
```

**Response Fields:**
- Standard place fields (id, name, description, category, city, price, rating, time_minutes, lat, long)
- `image`: Image URL from Wikidata (if available)
- `wikidata_entity`: Wikidata entity URI (if enriched with external data)
- `description_id`: Indonesian description from Wikidata (if available)

**Error Response (404):**
```json
{
  "error": "Place not found"
}
```

**Use Case:** Detailed place page, info panel with external knowledge enrichment  
**Performance:** ~20-50ms

---

## 📦 Package Endpoints

### 1. List All Packages
**GET** `/packages/`

Get list of all tourism packages.

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | integer | ❌ No | 10 | Maximum number of packages |

**Example Request:**
```http
GET /packages/?limit=10
```

**Example Response:**
```json
[
  {
    "package": {
      "id": 1,
      "name": "Jakarta Heritage Tour",
      "city": "Jakarta",
      "places_count": 3
    }
  },
  {
    "package": {
      "id": 2,
      "name": "Island Hopping Adventure",
      "city": "Jakarta",
      "places_count": 5
    }
  }
]
```

**Use Case:** Package listing page  
**Performance:** ~30-60ms

---

### 2. Get Package Details
**GET** `/packages/{package_id}`

Get detailed information about a specific package including all places.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `package_id` | integer | ✅ Yes | Package identifier |

**Example Request:**
```http
GET /packages/1
```

**Example Response:**
```json
{
  "package": {
    "id": 1,
    "name": "Jakarta Heritage Tour",
    "city": "Jakarta"
  },
  "places": [
    {
      "id": 1,
      "name": "Monumen Nasional",
      "category": "Budaya",
      "price": 20000,
      "rating": 4.6
    },
    {
      "id": 2,
      "name": "Kota Tua",
      "category": "Budaya",
      "price": 0,
      "rating": 4.6
    }
  ]
}
```

**Error Response (404):**
```json
{
  "detail": "Package not found"
}
```

**Use Case:** Package detail page  
**Performance:** ~40-80ms

---

## 🔧 Query Console Endpoint

### Execute Custom Cypher Query
**POST** `/query/`

Execute custom Cypher queries on the Neo4j database. For advanced users.

**Request Body:**
```json
{
  "query": "MATCH (p:Place) WHERE p.rating > 4.5 RETURN p.name, p.rating ORDER BY p.rating DESC LIMIT 5"
}
```

**Example Request:**
```http
POST /query/
Content-Type: application/json

{
  "query": "MATCH (p:Place {category: 'Budaya'}) RETURN p.name, p.price LIMIT 10"
}
```

**Example Response:**
```json
[
  {
    "p.name": "Museum Fatahillah",
    "p.price": 5000
  },
  {
    "p.name": "Monumen Nasional",
    "p.price": 20000
  }
]
```

**Security Restrictions:**
Forbidden keywords (for safety):
- `DELETE`, `DETACH`, `REMOVE`
- `APOC.`, `DBMS.`
- `DROP`, `CREATE DATABASE`

**Error Response (400):**
```json
{
  "error": "Query mengandung keyword berbahaya: delete"
}
```

**Use Case:** Advanced filtering, custom analytics  
**Performance:** Varies (10-500ms depending on query complexity)

---

## 📤 Response Format

### Success Response Structure
All successful responses follow this structure:

```json
[
  {
    "place": { /* Place object */ }
  }
]
```

or for single place:

```json
{
  "place": { /* Place object */ },
  "related_places": [ /* Array */ ],
  "packages": [ /* Array */ ]
}
```

### Place Object Schema
```typescript
{
  id: number;
  name: string;
  description?: string;
  category: string;
  city: string;
  price: number;
  rating: number;
  time_minutes?: number;
  lat: number;
  long: number;
  
  // Optional - External Knowledge Graph enrichment (from Wikidata)
  image?: string;                // Image URL from Wikidata
  wikidata_entity?: string;      // Wikidata entity URI
  description_id?: string;       // Indonesian description from Wikidata
  
  // Optional - Search-specific scores (depending on endpoint)
  vector_score?: number;         // 0-1 (semantic similarity)
  rerank_score?: number;         // typically -10 to +15 (relevance)
  name_score?: number;           // name matching score
  description_score?: number;    // description matching score
}
```

---

## ⚠️ Error Handling

### HTTP Status Codes
| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Request completed successfully |
| 400 | Bad Request | Invalid query, forbidden keywords |
| 404 | Not Found | Place/Package ID doesn't exist |
| 422 | Validation Error | Missing required parameters |
| 500 | Server Error | Database connection failed |

### Error Response Format
```json
{
  "error": "Error message here",
  "detail": "Additional details (optional)"
}
```

### Common Errors

**1. Empty Query**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["query", "query"],
      "msg": "Field required"
    }
  ]
}
```

**2. Invalid Place ID**
```json
{
  "error": "Place not found"
}
```

**3. Forbidden Query**
```json
{
  "error": "Query mengandung keyword berbahaya: delete"
}
```

---

## 💻 Integration Examples

### JavaScript/TypeScript (Fetch API)

```javascript
// Basic Search
async function searchPlaces(query) {
  const response = await fetch(
    `http://localhost:8000/search/?query=${encodeURIComponent(query)}`
  );
  return await response.json();
}

// Semantic Search
async function semanticSearch(query, k = 5) {
  const response = await fetch(
    `http://localhost:8000/search/semanticly?query=${encodeURIComponent(query)}&k=${k}`
  );
  return await response.json();
}

// Reranking Search
async function rerankSearch(query, topK = 5) {
  const response = await fetch(
    `http://localhost:8000/search/rerank?query=${encodeURIComponent(query)}&top_k=${topK}`
  );
  return await response.json();
}

// Get Place (basic info)
async function getPlace(placeId) {
  const response = await fetch(`http://localhost:8000/places/${placeId}`);
  if (!response.ok) {
    throw new Error('Place not found');
  }
  return await response.json();
}

// Get Place Details (with related data)
async function getPlaceDetails(placeId) {
  const response = await fetch(`http://localhost:8000/infobox/${placeId}`);
  if (!response.ok) {
    throw new Error('Place not found');
  }
  return await response.json();
}

// Get Packages
async function getPackages(limit = 10) {
  const response = await fetch(`http://localhost:8000/packages/?limit=${limit}`);
  return await response.json();
}

// Custom Query
async function executeQuery(cypherQuery) {
  const response = await fetch('http://localhost:8000/query/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query: cypherQuery }),
  });
  return await response.json();
}
```

### React Hooks Example

```typescript
import { useState, useEffect } from 'react';

// Search Hook
function useSearch(query: string, method: 'basic' | 'semantic' | 'rerank' = 'semantic') {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!query) return;

    const searchEndpoints = {
      basic: `/search/?query=${query}`,
      semantic: `/search/semanticly?query=${query}&k=10`,
      rerank: `/search/rerank?query=${query}&top_k=10`,
    };

    setLoading(true);
    fetch(`http://localhost:8000${searchEndpoints[method]}`)
      .then(res => res.json())
      .then(data => {
        setResults(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [query, method]);

  return { results, loading, error };
}

// Usage in Component
function SearchComponent() {
  const [query, setQuery] = useState('');
  const { results, loading, error } = useSearch(query, 'rerank');

  return (
    <div>
      <input 
        value={query} 
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search places..."
      />
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      {results.map(item => (
        <div key={item.place.id}>
          <h3>{item.place.name}</h3>
          <p>{item.place.description}</p>
          <p>Score: {item.place.rerank_score?.toFixed(2)}</p>
        </div>
      ))}
    </div>
  );
}
```

### Python Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Search
def search_places(query, method="semantic", k=5):
    if method == "basic":
        response = requests.get(f"{BASE_URL}/search/", params={"query": query})
    elif method == "semantic":
        response = requests.get(f"{BASE_URL}/search/semanticly", params={"query": query, "k": k})
    elif method == "rerank":
        response = requests.get(f"{BASE_URL}/search/rerank", params={"query": query, "top_k": k})
    
    return response.json()

# Get Place (basic)
def get_place(place_id):
    response = requests.get(f"{BASE_URL}/places/{place_id}")
    if response.status_code == 404:
        return None
    return response.json()

# Get Place Details (with related data)
def get_place_details(place_id):
    response = requests.get(f"{BASE_URL}/infobox/{place_id}")
    if response.status_code == 404:
        return None
    return response.json()

# Execute Query
def run_cypher_query(cypher):
    response = requests.post(
        f"{BASE_URL}/query/",
        json={"query": cypher}
    )
    return response.json()

# Usage
results = search_places("museum", method="rerank", k=5)
for item in results:
    place = item['place']
    print(f"{place['name']}: {place.get('rerank_score', 0):.2f}")
```

---

## 🎯 Best Practices

### 1. Endpoint Selection Guide

| Use Case | Recommended Endpoint | Why |
|----------|---------------------|-----|
| Autocomplete | `/search/` | Fastest response |
| Main search | `/search/rerank` | Best accuracy |
| Detailed search | `/search/rerank-advanced` | Considers description |
| Explore similar | `/search/semanticly` | Good balance |

### 2. Performance Optimization

**For Real-Time Search (Autocomplete):**
- Use `/search/` or `/search/semanticly` with `k=5`
- Debounce input (wait 300ms after typing stops)

**For Main Search Results:**
- Use `/search/rerank` with `initial_k=20, top_k=10`
- Show loading indicator (can take 200-500ms)

**For Advanced Filters:**
- Use `/search/rerank-advanced`
- Cache frequent queries
- Consider pagination for large result sets

### 3. Error Handling

```javascript
async function safeSearch(query) {
  try {
    const response = await fetch(`/search/rerank?query=${query}`);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    
    const data = await response.json();
    
    if (data.error) {
      console.error('API Error:', data.error);
      return [];
    }
    
    return data;
  } catch (error) {
    console.error('Network Error:', error);
    return [];
  }
}
```

### 4. Caching Strategy

```javascript
const cache = new Map();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

async function cachedSearch(query) {
  const cacheKey = `search:${query}`;
  const cached = cache.get(cacheKey);
  
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data;
  }
  
  const data = await searchPlaces(query);
  cache.set(cacheKey, {
    data,
    timestamp: Date.now()
  });
  
  return data;
}
```

---

## 📊 Testing Endpoints

Use the interactive API documentation:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

Or use cURL:

```bash
# Basic Search
curl "http://localhost:8000/search/?query=museum"

# Semantic Search
curl "http://localhost:8000/search/semanticly?query=museum&k=5"

# Reranking
curl "http://localhost:8000/search/rerank?query=museum%20sejarah&top_k=5"

# Places
curl "http://localhost:8000/places/1"

# InfoBox
curl "http://localhost:8000/infobox/1"

# Packages
curl "http://localhost:8000/packages/"

# Query Console
curl -X POST "http://localhost:8000/query/" \
  -H "Content-Type: application/json" \
  -d '{"query": "MATCH (p:Place) RETURN p.name LIMIT 5"}'
```

---

## 🔗 Additional Resources

- **API Docs (Interactive):** http://localhost:8000/docs
- **Repository:** [GitHub Link]
- **Support:** [Contact Information]

---

**Last Updated:** December 5, 2025  
**API Version:** 1.0.0

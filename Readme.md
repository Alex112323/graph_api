# Graph API Service

A FastAPI-based service for working with directed acyclic graphs (DAGs). Provides endpoints for creating, reading, and manipulating graph structures.

## Table of Contents
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Request/Response Examples](#requestresponse-examples)
- [Error Handling](#error-handling)
- [Installation](#installation)
- [Development](#development)
- [License](#license)

## Features

- Create new acyclic graphs
- Retrieve graph information in different representations
- Delete nodes from graphs
- Get adjacency lists (both standard and reverse)
- Health check endpoint
- Input validation

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/health` | Service health status |
| `POST` | `/api/graph/` | Create a new graph |
| `GET`  | `/api/graph/{graph_id}/` | Read graph structure |
| `DELETE` | `/api/graph/{graph_id}/node/{node_name}` | Delete a node from graph |
| `GET`  | `/api/graph/{graph_id}/adjacency_list` | Get adjacency list representation |
| `GET`  | `/api/graph/{graph_id}/reverse_adjacency_list` | Get reverse adjacency list (transposed graph) |

## Request/Response Examples

### Create Graph
```json
POST /api/graph/
Request Body:
{
  "nodes": [
    {"name": "A"},
    {"name": "B"},
    {"name": "C"}
  ],
  "edges": [
    {"source": "A", "target": "B"},
    {"source": "B", "target": "C"}
  ]
}

Response:
{
  "id": 1,
  "message": "successful"
}
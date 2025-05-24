from fastapi import APIRouter, Depends, Path, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db_models.get_db import get_db
from app.db_models.models import Graph, Vertex, Edge
from app.schemas import (
    GraphCreate,
    GraphCreateResponse,
    GraphReadResponse,
    ErrorResponse,
    HTTPValidationError
)
from app.core.utils import is_acyclic
from typing import List, Dict

router = APIRouter()

@router.get("/health")
async def health_check():
    return JSONResponse(content={"status": "ok"})

@router.post(
    "/api/graph/",
    response_model=GraphCreateResponse,
    status_code=201,
    responses={
        201: {"description": "Successful response", "model": GraphCreateResponse},
        400: {"description": "Failed to add graph", "model": ErrorResponse},
        422: {"description": "Validation Error", "model": HTTPValidationError},
    },
    summary="Create Graph",
    description="Ручка для создания графа, принимает граф в виде списка вершин и списка ребер."
)
def create_graph(graph: GraphCreate, db: Session = Depends(get_db)):
    node_names = [node.name for node in graph.nodes]
    edge_list = [(edge.source, edge.target) for edge in graph.edges]

    if not is_acyclic(node_names, edge_list):
        raise HTTPException(
            status_code=400,
            detail={"message": "Graph contains a cycle"}
        )

    new_graph = Graph()
    name_to_vertex = {}

    for node in graph.nodes:
        vertex = Vertex(name=node.name, graph=new_graph)
        db.add(vertex)
        name_to_vertex[node.name] = vertex

    for edge in graph.edges:
        source_vertex = name_to_vertex.get(edge.source)
        target_vertex = name_to_vertex.get(edge.target)

        if not source_vertex or not target_vertex:
            raise HTTPException(
                status_code=400,
                detail={"message": f"Invalid edge: {edge.source} -> {edge.target}"}
            )

        db.add(Edge(
            from_vertex=source_vertex,
            to_vertex=target_vertex,
            graph=new_graph
        ))

    db.add(new_graph)
    db.commit()

    return {"id": new_graph.id, "message" : "successful"}

@router.get(
    "/api/graph/{graph_id}/",
    response_model=GraphReadResponse,
    responses={
        200: {"description": "Successful Response", "model": GraphReadResponse},
        404: {"description": "Graph entity not found", "model": ErrorResponse},
        422: {"description": "Validation Error", "model": HTTPValidationError},
    },
    summary="Read Graph",
    description="Ручка для чтения графа в виде списка вершин и списка ребер.",
)
def read_graph(graph_id: int = Path(..., title="Graph Id"), db: Session = Depends(get_db)):
    graph = db.query(Graph).filter(Graph.id == graph_id).first()
    if not graph:
        raise HTTPException(
            status_code=404,
            detail={"message": "Graph entity not found"}
        )

    nodes = [{"name": v.name} for v in graph.vertices]
    edges = [{"source": e.from_vertex.name, "target": e.to_vertex.name} for e in graph.edges]

    return {"id": graph_id, "nodes": nodes, "edges": edges}

@router.delete(
    "/api/graph/{graph_id}/node/{node_name}",
    status_code=204,
    responses={
        204: {"description": "Successful Response"},
        404: {"description": "Graph entity not found", "model": ErrorResponse},
        422: {"description": "Validation Error", "model": HTTPValidationError},
    },
    summary="Delete Node",
    description="Ручка для удаления вершины из графа по ее имени.",
)
def delete_node(
    graph_id: int = Path(..., title="Graph Id"),
    node_name: str = Path(..., title="Node Name"),
    db: Session = Depends(get_db)
):
    graph = db.query(Graph).filter(Graph.id == graph_id).first()
    if not graph:
        raise HTTPException(
            status_code=404,
            detail={"message": "Graph not found"}
        )

    node = db.query(Vertex).filter(Vertex.graph_id == graph_id, Vertex.name == node_name).first()
    if not node:
        raise HTTPException(
            status_code=404,
            detail={"message": "Node not found"}
        )

    db.query(Edge).filter((Edge.from_vertex_id == node.id) | (Edge.to_vertex_id == node.id)).delete(synchronize_session=False)
    db.delete(node)
    db.commit()
    return Response(status_code=204)

@router.get(
    "/api/graph/{graph_id}/adjacency_list",
    response_model=Dict[str, List[str]],
    responses={
        200: {
            "description": "Successful Response", 
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/AdjacencyListResponse"}
                }
            }
        },
        404: {
            "description": "Graph entity not found",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ErrorResponse"
                    }
                }
            }
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/HTTPValidationError"
                    }
                }
            }
        },
    },
    summary="Get Adjacency List",
    description="Ручка для чтения графа в виде списка смежности.\nСписок смежности представлен в виде пар ключ - значение, где\n- ключ - имя вершины графа,\n- значение - список имен всех смежных вершин (всех потомков ключа).",
)
def get_adjacency_list(
    graph_id: int = Path(..., title="Graph Id"),
    db: Session = Depends(get_db)
):
    graph = db.query(Graph).filter(Graph.id == graph_id).first()
    if not graph:
        raise HTTPException(
            status_code=404,
            detail={"message": "Graph entity not found"}
        )

    adjacency_list = {}
    
    vertices = db.query(Vertex).filter(Vertex.graph_id == graph_id).all()
    
    for vertex in vertices:
        edges = db.query(Edge).join(Vertex, Edge.to_vertex_id == Vertex.id)\
                            .filter(Edge.from_vertex_id == vertex.id)\
                            .all()
        adjacency_list[vertex.name] = [edge.to_vertex.name for edge in edges]
    
    return adjacency_list

@router.get(
    "/api/graph/{graph_id}/reverse_adjacency_list",
    response_model=Dict[str, List[str]],
    responses={
        200: {"description": "Successful Response", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/AdjacencyListResponse"}}}},
        404: {"description": "Graph entity not found", "model": ErrorResponse},
        422: {"description": "Validation Error", "model": HTTPValidationError},
    },
    summary="Get Reverse Adjacency List",
    description="Ручка для чтения транспонированного графа в виде списка смежности.\nСписок смежности представлен в виде пар ключ - значение, где\n- ключ - имя вершины графа,\n- значение - список имен всех смежных вершин (всех предков ключа в исходном графе).",
)
def get_reverse_adjacency_list(
    graph_id: int = Path(..., title="Graph Id"),
    db: Session = Depends(get_db)
):
    graph = db.query(Graph).filter(Graph.id == graph_id).first()
    if not graph:
        raise HTTPException(
            status_code=404,
            detail={"message": "Graph entity not found"}
        )

    reverse_adjacency_list = {}
    
    vertices = db.query(Vertex).filter(Vertex.graph_id == graph_id).all()
    
    for vertex in vertices:
        reverse_adjacency_list[vertex.name] = []
    
    edges = db.query(Edge).filter(Edge.graph_id == graph_id).all()
    for edge in edges:
        reverse_adjacency_list[edge.to_vertex.name].append(edge.from_vertex.name)
    
    return reverse_adjacency_list
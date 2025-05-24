from sqlalchemy import (
    Column, Integer, String, ForeignKey, Index, 
    UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()

class Graph(Base):
    __tablename__ = 'graphs'
    
    id = Column(Integer, primary_key=True)
    
    vertices = relationship("Vertex", back_populates="graph", cascade="all, delete-orphan")
    edges = relationship("Edge", back_populates="graph", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_graphs_id", "id", postgresql_using='btree'),
    )

class Vertex(Base):
    __tablename__ = 'vertices'
    
    id = Column(Integer, primary_key=True)
    graph_id = Column(Integer, ForeignKey('graphs.id', ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    
    graph = relationship("Graph", back_populates="vertices")
    outgoing_edges = relationship("Edge", foreign_keys="[Edge.from_vertex_id]", back_populates="from_vertex")
    incoming_edges = relationship("Edge", foreign_keys="[Edge.to_vertex_id]", back_populates="to_vertex")

    __table_args__ = (
        UniqueConstraint('graph_id', 'name', name='uq_vertex_graph_name'),
        CheckConstraint("name ~ '^[a-zA-Z]+$'", name='check_vertex_name'),
        Index("ix_vertices_graph_id", "graph_id", postgresql_using='btree'),
        Index("ix_vertices_name", "name", postgresql_using='btree'),
    )

class Edge(Base):
    __tablename__ = 'edges'
    
    id = Column(Integer, primary_key=True)
    graph_id = Column(Integer, ForeignKey('graphs.id', ondelete="CASCADE"), nullable=False)
    from_vertex_id = Column(Integer, ForeignKey('vertices.id', ondelete="CASCADE"), nullable=False)
    to_vertex_id = Column(Integer, ForeignKey('vertices.id', ondelete="CASCADE"), nullable=False)
    
    graph = relationship("Graph", back_populates="edges")
    from_vertex = relationship("Vertex", foreign_keys=[from_vertex_id], back_populates="outgoing_edges")
    to_vertex = relationship("Vertex", foreign_keys=[to_vertex_id], back_populates="incoming_edges")

    __table_args__ = (
        UniqueConstraint('graph_id', 'from_vertex_id', 'to_vertex_id', name='uq_edge_graph_vertices'),
        CheckConstraint("from_vertex_id != to_vertex_id", name='check_no_self_loop'),
        Index("ix_edges_graph_id", "graph_id", postgresql_using='btree'),
        Index("ix_edges_from_vertex", "from_vertex_id", postgresql_using='btree'),
        Index("ix_edges_to_vertex", "to_vertex_id", postgresql_using='btree'),
    )
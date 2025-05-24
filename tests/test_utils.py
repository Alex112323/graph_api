from app.core.utils import is_acyclic

def test_is_acyclic_returns_true_for_acyclic_graph():
    nodes = ["A", "B", "C"]
    edges = [("A", "B"), ("B", "C")]
    assert is_acyclic(nodes, edges) is True

def test_is_acyclic_returns_false_for_cyclic_graph():
    nodes = ["A", "B", "C"]
    edges = [("A", "B"), ("B", "C"), ("C", "A")]
    assert is_acyclic(nodes, edges) is False

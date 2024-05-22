import io
import json
import random

import networkx as nx

from .graph_drawer import GraphDrawer


class OutputFormat:
    """A class to represent various output formats of a graph.

    Attributes:
        graph (Graph): An instance of the Graph class.
    """

    def __init__(self, graph):
        """Inits OutputFormat with a graph.

        Args:
            graph (Graph): An instance of the Graph class.
        """
        self.graph = graph

    def to_format(self, format_type: str) -> str:
        """Converts the graph to a specified format.

        Args:
            format_type (str): The format type to convert the graph into.

        Returns:
            str: The graph in the specified format.
        """
        format_methods = {'graphml': self._to_graphml, 'yarspg': self._to_yarspg, 'yarspg-rdf': self._to_yarspg_rdf, 'gexf': self._to_gexf,
            'gml': self._to_gml, 'svg': self._to_svg, 'adjacency_list': self._to_adjacency_list,
            'multiline_adjacency_list': self._to_multiline_adjacency_list, 'edge_list': self._to_edge_list,
            'json': self._to_json}
        return format_methods[format_type]()

    def _to_graphml(self) -> str:
        """Converts the graph to GraphML format.

        Returns:
            str: The graph in GraphML format.
        """
        return '\n'.join(nx.generate_graphml(self.graph.graph))

    def _to_yarspg(self) -> str:
        """Converts the graph to YARS-PG format.

        Returns:
            str: The graph in YARS-PG format.
        """
        nodes_output = [self._format_node_yarspg(node) for node in self.graph.graph.nodes(data=True)]
        edges_output = [self._format_edge_yarspg(edge) for edge in self.graph.graph.edges(data=True)]
        return '\n'.join(nodes_output + edges_output)

    def _to_yarspg_rdf(self) -> str:
        """Converts the graph to YARS-PG RDF format.

        Returns:
            str: The graph in YARS-PG RDF format.
        """
        nodes_section = '# Nodes\n'
        edges_section = '\n# Edges\n'
        nodes_output = [self._format_node_yarspg_rdf(node) for node in self.graph.graph.nodes(data=True)]
        edges_output = [self._format_edge_yarspg_rdf(edge) for edge in self.graph.graph.edges(data=True)]

        # Konwertowanie list na stringi i dołączanie do sekcji
        nodes_output_str = '\n'.join(nodes_output)
        edges_output_str = '\n'.join(edges_output)

        # Składanie wszystkiego w jeden wynikowy string
        return f"{nodes_section}{nodes_output_str}{edges_section}{edges_output_str}"

    @staticmethod
    def _format_node_yarspg(node: tuple) -> str:
        """Formats a node in YARS-PG format.

        Args:
            node (tuple): A tuple containing the node ID and attributes.

        Returns:
            str: The node in YARS-PG format.
        """
        node_id, attributes = node
        label = attributes.get('label', 'label')
        prop_list = ', '.join([f'"{key}": "{value}"' for key, value in attributes.items() if key != 'label'])
        return f"({node_id} {{\"{label}\"}}[{prop_list}])"

    @staticmethod
    def _format_edge_yarspg(edge: tuple) -> str:
        """Formats an edge in YARS-PG format.

        Args:
            edge (tuple): A tuple containing the source node, target node, and attributes.

        Returns:
            str: The edge in YARS-PG format.
        """
        u, v, attributes = edge
        label = attributes.get('label', 'label')
        prop_list = ', '.join([f'"{key}": "{value}"' for key, value in attributes.items() if key != 'label'])
        return f"({u})-({{\"{label}\"}}[{prop_list}])->({v})"

    @staticmethod
    def _format_node_yarspg_rdf(node: tuple) -> str:
        """Formats a node in YARS-PG RDF format.

        Args:
            node (tuple): A tuple containing the node ID and attributes.

        Returns:
            str: The node in YARS-PG format.
        """
        node_id = node[0]
        attributes = {'label': 'IRI', '@value': 'https://w3id.org/MON/person.owl#Person'}
        label = attributes.get('label', 'label')
        prop_list = ', '.join([f'"{key}": "{value}"' for key, value in attributes.items() if key != 'label'])
        return f"({node_id} {{\"{label}\"}}[{prop_list}])"

    @staticmethod
    def _format_edge_yarspg_rdf(edge: tuple) -> str:
        """Formats an edge in YARS-PG RDF format.

        Args:
            edge (tuple): A tuple containing the source node, target node, and attributes.

        Returns:
            str: The edge in YARS-PG format.
        """
        u, v = edge[:2]
        attributes = {'label': 'IRI', '@value': 'https://w3id.org/MON/person.owl#friendOf'}
        label = attributes.get('label', 'label')
        prop_list = ', '.join([f'"{key}": "{value}"' for key, value in attributes.items() if key != 'label'])
        return f"({u})-({{\"{label}\"}}[{prop_list}])->({v})"

    def _to_svg(self) -> str:
        """Converts the graph to SVG format.

        Returns:
            str: The graph in SVG format.
        """
        drawer = GraphDrawer(self.graph.graph)
        with io.BytesIO() as buffer:
            drawer._draw_to_buffer(buffer)
            return buffer.getvalue().decode('utf-8')

    def _to_gexf(self) -> str:
        """Converts the graph to GEXF format.

        Returns:
            str: The graph in GEXF format.
        """
        return '\n'.join(nx.generate_gexf(self.graph.graph))

    def _to_gml(self) -> str:
        """Converts the graph to GML format.

        Returns:
            str: The graph in GML format.
        """
        return '\n'.join(nx.generate_gml(self.graph.graph))

    def _to_adjacency_list(self) -> str:
        """Converts the graph to adjacency list format.

        Returns:
            str: The graph in adjacency list format.
        """
        return '\n'.join(nx.generate_adjlist(self.graph.graph))

    def _to_multiline_adjacency_list(self) -> str:
        """Converts the graph to multiline adjacency list format.

        Returns:
            str: The graph in multiline adjacency list format.
        """
        return '\n'.join(nx.generate_multiline_adjlist(self.graph.graph))

    def _to_edge_list(self) -> str:
        """Converts the graph to edge list format.

        Returns:
            str: The graph in edge list format.
        """
        return '\n'.join(nx.generate_edgelist(self.graph.graph, data=True))

    def _to_json(self) -> str:
        """Converts the graph to JSON format.

        Returns:
            str: The graph in JSON format.
        """
        return json.dumps(nx.node_link_data(self.graph.graph))

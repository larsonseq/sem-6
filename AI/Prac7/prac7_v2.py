class Node:
    def __init__(self, name, parents=None):
        self.name = name
        self.parents = parents if parents else []
        self.cpt = {}  # Conditional Probability Table
    
    def add_probability(self, parent_values, prob_true):
        # Create a tuple of parent values (True/False) to use as key
        key = tuple(parent_values)
        self.cpt[key] = (prob_true, 1.0 - prob_true)
    
    def get_probability(self, value, parent_values):
        key = tuple(parent_values)
        if key in self.cpt:
            return self.cpt[key][0] if value else self.cpt[key][1]
        else:
            return None

class BayesianNetwork:
    def __init__(self):
        self.nodes = {}
        self.levels = []
        self.all_nodes = []
    
    def add_node(self, level, node):
        if level >= len(self.levels):
            self.levels.extend([[] for _ in range(level - len(self.levels) + 1)])
        self.levels[level].append(node.name)
        self.nodes[node.name] = node
        if node.name not in self.all_nodes:
            self.all_nodes.append(node.name)
    
    def get_all_nodes(self):
        return self.all_nodes
    
    def calculate_conditional_probability(self, query_node, evidence):
        """
        Calculate probability for a query node given evidence
        evidence is a dictionary {node_name: value (True/False)}
        """
        node = self.nodes[query_node]
        parent_values = [evidence.get(parent, None) for parent in node.parents]
        
        # Check if all parent values are provided
        if None not in parent_values:
            return node.get_probability(evidence.get(query_node, True), parent_values)
        else:
            # More complex calculation required for incomplete evidence
            return "Complex probability calculation not implemented for incomplete evidence"
    
    def calculate_joint_probability(self, evidence):
        """
        Calculate joint probability P(X1=x1, X2=x2, ..., Xn=xn)
        evidence is a dictionary {node_name: value (True/False)}
        """
        if not all(node in evidence for node in self.nodes):
            return "Joint probability requires values for all nodes"
        
        # Calculate P(X1,X2,...,Xn) = ∏ P(Xi | parents(Xi))
        joint_prob = 1.0
        for node_name, node in self.nodes.items():
            node_value = evidence[node_name]
            parent_values = [evidence[parent] for parent in node.parents]
            prob = node.get_probability(node_value, parent_values)
            joint_prob *= prob
        
        return joint_prob

def main():
    network = BayesianNetwork()
    
    # Get number of levels
    num_levels = int(input("Enter number of levels in the Bayesian network: "))
    
    # Get nodes at each level
    for level in range(num_levels):
        print(f"\nLevel {level + 1}:")
        nodes = input("Enter node names (separated by space): ").strip().split()
        
        for node_name in nodes:
            parent_nodes = []
            
            # For nodes beyond the first level, ask for parent nodes from any previous level
            if level > 0:
                print(f"\nFor node '{node_name}', select parent nodes from any previous level:")
                available_nodes = []
                for l in range(level):
                    available_nodes.extend(network.levels[l])
                print(f"Available nodes: {available_nodes}")
                parents = input("Enter parent node names (separated by space): ").strip().split()
                
                # Validate that parents exist in previous levels
                parent_nodes = [p for p in parents if p in available_nodes]
                if len(parent_nodes) != len(parents):
                    print("Warning: Some specified parents do not exist in previous levels.")
            
            node = Node(node_name, parent_nodes)
            network.add_node(level, node)
            
            # If node has parents, get probabilities
            if parent_nodes:
                print(f"\nEnter probabilities for node '{node_name}':")
                # Generate all possible parent combinations
                combinations = generate_combinations(len(parent_nodes))
                
                for combination in combinations:
                    condition = ", ".join([f"{parent_nodes[i]} = {['False', 'True'][combination[i]]}" for i in range(len(parent_nodes))])
                    prob = float(input(f"P({node_name} = True | {condition}): "))
                    node.add_probability(combination, prob)
            else:
                # No parents, just need a prior probability
                prob = float(input(f"P({node_name} = True): "))
                node.add_probability((), prob)
    
    # Query the network
    while True:
        print("\n--- Query the Bayesian Network ---")
        print("Choose query type:")
        print("1. Conditional Probability")
        print("2. Joint Probability")
        print("3. Exit")
        choice = input("Your choice: ")
        
        if choice == '3':
            break
        
        if choice == '1':
            # Conditional probability query
            print("Available nodes:", list(network.nodes.keys()))
            query_node = input("Enter the node you want to query: ")
            
            if query_node not in network.nodes:
                print("Invalid node name.")
                continue
            
            evidence = {}
            print("Enter evidence (node values):")
            for node_name in network.nodes:
                if node_name != query_node:
                    value = input(f"Is {node_name} True? (y/n/skip): ").lower()
                    if value == 'y':
                        evidence[node_name] = True
                    elif value == 'n':
                        evidence[node_name] = False
            
            prob = network.calculate_conditional_probability(query_node, evidence)
            print(f"P({query_node} = True | evidence) = {prob}")
            print(f"P({query_node} = False | evidence) = {1 - prob if isinstance(prob, float) else 'N/A'}")
        
        elif choice == '2':
            # Joint probability query
            evidence = {}
            print("Enter values for all nodes (This must include every node):")
            for node_name in network.nodes:
                while True:
                    value = input(f"Is {node_name} True? (y/n): ").lower()
                    if value == 'y':
                        evidence[node_name] = True
                        break
                    elif value == 'n':
                        evidence[node_name] = False
                        break
                    else:
                        print("Please enter 'y' or 'n'.")
            
            # Print the joint probability query in natural language
            query_desc = ", ".join([f"{node} = {'True' if val else 'False'}" for node, val in evidence.items()])
            print(f"\nCalculating P({query_desc})")
            
            prob = network.calculate_joint_probability(evidence)
            print(f"Joint Probability = {prob}")
        
        else:
            print("Invalid choice.")

def generate_combinations(n):
    """Generate all possible True/False combinations for n variables"""
    if n == 0:
        return [()]
    
    result = []
    smaller_combinations = generate_combinations(n - 1)
    for combo in smaller_combinations:
        result.append(combo + (True,))
        result.append(combo + (False,))
    return result

if __name__ == "__main__":
    print("Bayesian Belief Network Calculator")
    main()
class BlockWorldProblem:
    def __init__(self, initial, goalstate):
        self.initial = initial
        self.goal = goalstate
        self.state = dict(initial)
        self.plan = []
    
    def block_on(self, block):
        return [b for b, pos in self.state.items() if pos == block]

    def do_move(self, block, dest):
        if self.state.get(block) == dest:
            return
        self.plan.append(f"Moved {block} to {dest}")
        self.state[block] = dest

    def clear(self, block):
        for b in list(self.block_on(block)):
            self.clear(b)
            self.do_move(b, "Table")

    def move(self, block, dest):
        if self.state.get(block) == dest:
            return
        self.clear(block)
        if dest != "Table":
            self.clear(dest)
        self.do_move(block, dest)

    def generate_plan(self):
        def goal_depth(block):
            depth = 0
            p = self.goal.get(block)
            while p and p != "Table":
                depth += 1
                p = self.goal.get(p)
            return depth
        for block, dest in sorted(self.goal.items(), key=lambda x: goal_depth(x[0])):
            self.move(block, dest)

    def display_plan(self):
        """Print out the final plan, one step per line."""
        print("Final Plan:")
        for step in self.plan:
            print(f"- {step}")


if __name__ == "__main__":
    initial_state = {"A": "B", "B": "C", "C": "D", "D":"Table"}
    goal_state = {"D": "C", "C": "B", "B": "A", "A": "Table"}

    planner = BlockWorldProblem(initial_state, goal_state)
    planner.generate_plan()
    planner.display_plan()
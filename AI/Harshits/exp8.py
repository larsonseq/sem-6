class BlockWorldPlanner:
    def __init__(self, initial_state, goal_state):
        # initial_state and goal_state are dicts: block -> supporting block or "Table"
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.state = dict(initial_state)   # will track current world as we build the plan
        self.plan = []

    def blocks_on(self, block):
        """Return a list of blocks currently sitting directly on top of `block`."""
        return [b for b, pos in self.state.items() if pos == block]

    def clear(self, block):
        """
        Ensure that no block is on top of `block`.
        If there is, recursively clear that block and move it to the table.
        """
        for b in list(self.blocks_on(block)):
            # first clear anything on top of b
            self.clear(b)
            # then move b to the table
            self._do_move(b, "Table")

    def _do_move(self, block, dest):
        """Issue the move (updating state and appending to the plan)."""
        if self.state[block] == dest:
            return
        # perform the move
        self.plan.append(f"Move {block} to {dest}")
        self.state[block] = dest

    def move(self, block, dest):
        """
        Move `block` to `dest` (which is either another block or "Table"), 
        clearing both block and dest first.
        """
        if self.state[block] == dest:
            return
        # clear anything on top of our block
        self.clear(block)
        # if dest is a block, clear it too
        if dest != "Table":
            self.clear(dest)
        # now do the actual move
        self._do_move(block, dest)

    def generate_plan(self):
        """
        Build the plan by moving each block to its goal position.
        We sort blocks by their “depth” in the goal stack, so that
        bottom‐most blocks get placed first.
        """
        def goal_depth(block):
            # number of steps from `block` down to the table in goal_state
            depth = 0
            p = self.goal_state.get(block)
            while p and p != "Table":
                depth += 1
                p = self.goal_state.get(p)
            return depth

        # sort so that blocks supporting others (lower in stack) go first
        for block, dest in sorted(self.goal_state.items(), key=lambda x: goal_depth(x[0])):
            self.move(block, dest)

    def display_plan(self):
        """Print out the final plan, one step per line."""
        print("Final Plan:")
        for step in self.plan:
            print(f"- {step}")


if __name__ == "__main__":
    # Example run with your test case
    initial_state = {"A": "B", "B": "C", "C": "D", "D":"Table"}
    goal_state    = {"D": "C", "C": "B", "B": "A", "A": "Table"}

    planner = BlockWorldPlanner(initial_state, goal_state)
    planner.generate_plan()
    planner.display_plan()

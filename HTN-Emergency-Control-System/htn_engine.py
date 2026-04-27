class HTNPlanner:
    def __init__(self, methods, operators):
        self.methods = methods
        self.operators = operators
        self.plan = []
        self.tree_edges = []

    def plan_tasks(self, state, tasks, parent="ROOT"):
        if not tasks:
            return True

        task = tasks[0]
        remaining_tasks = tasks[1:]
        task_name = task[0]

        self.tree_edges.append((parent, str(task)))

        # Primitive task
        if task_name in self.operators:
            new_state = self.operators[task_name](state, *task[1:])

            if new_state is not None:
                self.plan.append(task)
                return self.plan_tasks(new_state, remaining_tasks, parent)

            return False

        # Compound task
        if task_name in self.methods:
            for method in self.methods[task_name]:
                subtasks = method(state, *task[1:])

                if subtasks is not None:
                    method_name = method.__name__
                    self.tree_edges.append((str(task), method_name))

                    saved_plan = list(self.plan)
                    saved_edges = list(self.tree_edges)

                    success = self.plan_tasks(
                        state,
                        subtasks + remaining_tasks,
                        method_name
                    )

                    if success:
                        return True

                    self.plan = saved_plan
                    self.tree_edges = saved_edges

        return False
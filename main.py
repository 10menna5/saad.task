import networkx as nx


def get_input():
    activities = {}  # dictionary
    dependencies = []  # list to store task dependencies as tuples

    while True:
        task_name = input("Enter task name (or type 'finish' to finish): ").strip()
        if task_name.lower() == 'finish':
            break
        try:
            duration = float(input(f"Enter duration for task {task_name}: ").strip())
        except ValueError:
            print("Please enter a valid float for duration.")
            continue
        activities[task_name] = duration

        depends_on = input(
            f"Enter tasks that {task_name} depends on (comma separated, or leave empty if none): ").strip()
        if depends_on:
            for dependency in depends_on.split(','):
                dependency = dependency.strip()
                if dependency == task_name:
                    print(f"Task {task_name} cannot depend on itself.")
                    continue
                if dependency not in activities:
                    print(f"Dependency {dependency} has not been defined yet.")
                    continue
                dependencies.append((dependency, task_name))

    # Print the data entered for activities and dependencies
    print("\nActivities:", activities)
    print("Dependencies:", dependencies)

    return activities, dependencies


def main():
    activities, dependencies = get_input()

    G = nx.DiGraph()

    for activity, duration in activities.items():
        G.add_node(activity, duration=duration)

    G.add_edges_from(dependencies)

    # (Critical Path)
    # Find the longest path using the max and sum method
    sorted_edges = sorted(G.edges(), key=lambda x: G.nodes[x[1]]['duration'], reverse=True)
    critical_path = []
    max_duration = 0

    for i in range(len(sorted_edges)):
        path = [sorted_edges[i][0]]
        path_duration = G.nodes[sorted_edges[i][0]]['duration']  # Initialize with the duration of the first task
        current = sorted_edges[i][1]

        while current in G:
            path.append(current)
            path_duration += G.nodes[current]['duration']  # Add duration of the current node
            current = next((v for u, v in sorted_edges if u == current), None)  # Find node after current
            if current is None:
                break

        # Compare based on total duration
        if path_duration > max_duration:
            max_duration = path_duration
            critical_path = path


    print(f'Critical Path: {" -> ".join(critical_path)}')
    print(f'Critical Path Duration: {max_duration}')


    # (Total Duration)
    total_duration = sum(nx.get_node_attributes(G, 'duration').values())
    print(f'\nTotal Duration of all tasks: {total_duration}')


if __name__ == "__main__":
    main()

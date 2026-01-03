from ortools.sat.python import cp_model

def schedule_orders(orders, horizon=100):
    model = cp_model.CpModel()

    machine_intervals = {}
    starts, ends = {}, {}

    objective_terms = []

    for o in orders:
        machine = o["machine_required"]
        if machine not in machine_intervals:
            machine_intervals[machine] = []

        start = model.NewIntVar(0, horizon, f"start_{o['order_id']}")
        end = model.NewIntVar(0, horizon, f"end_{o['order_id']}")

        interval = model.NewIntervalVar(
            start,
            o["processing_time"],
            end,
            f"interval_{o['order_id']}"
        )

        model.Add(end <= o["deadline"])

        machine_intervals[machine].append(interval)
        starts[o["order_id"]] = start
        ends[o["order_id"]] = end

        # ---- OBJECTIVE TERMS ----
        # Smaller deadline → higher weight
        deadline_weight = 1000 - o["deadline"]      # EDF dominance
        priority_weight = o["priority"] * 10        # Secondary importance

        objective_terms.append(deadline_weight * end)
        objective_terms.append(-priority_weight * end)

    # Machine capacity
    for machine, intervals in machine_intervals.items():
        model.AddNoOverlap(intervals)

    # ---- OBJECTIVE ----
    model.Minimize(sum(objective_terms))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return {
            "feasible": True,
            "schedule": sorted(
                [
                    {
                        "order_id": o["order_id"],
                        "machine": o["machine_required"],
                        "start": solver.Value(starts[o["order_id"]]),
                        "end": solver.Value(ends[o["order_id"]]),
                        "priority": o["priority"],
                        "deadline": o["deadline"]
                    }
                    for o in orders
                ],
                key=lambda x: x["start"]
            )
        }

    return {
        "feasible": False,
        "reason": "Deadline or machine capacity violation"
    }

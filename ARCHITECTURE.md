# Architecture Overview

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         WEB DASHBOARD                            │
│  (http://127.0.0.1:5000 - dashboard.html + AJAX)               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Controls: Start | Step | Run | Stop                      │  │
│  │ Metrics: Vehicles, Wait Time, Travel Time, Completed     │  │
│  │ History: Saved experiments list                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────┬───────────────────────────────────────────┘
                     │ AJAX/JSON
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│                       FLASK API (app/main.py)                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ POST /api/simulation/start   → Initialize              │  │
│  │ POST /api/simulation/step    → Execute 1 timestep      │  │
│  │ POST /api/simulation/run     → Execute N timesteps     │  │
│  │ POST /api/simulation/stop    → Save & stop             │  │
│  │ GET  /api/metrics            → Get current stats       │  │
│  │ GET  /api/experiments        → List saved runs         │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────┬───────────────────────────────────────────┘
                     │
            ┌────────┴────────┐
            ↓                 ↓
      ┌──────────────┐  ┌──────────────────┐
      │ Simulation   │  │ Database         │
      │ Engine       │  │ (SQLite)         │
      └──────────────┘  └──────────────────┘
            ↑                    ↑
            │                    │
            └────────┬───────────┘
                     │
            ┌────────┴──────────┐
            │                   │
            ↓                   ↓
        ┌─────────────┐  ┌──────────────┐
        │  SIMULATOR  │  │ CONTROLLERS  │
        ├─────────────┤  ├──────────────┤
        │ World       │  │ FixedTime    │
        │ Generator   │  │ Adaptive     │
        │ Engine      │  └──────────────┘
        └─────────────┘
```

## Component Details

### 1. Simulation Layer (`app/simulator/`)

```
World (Grid Network)
├── Intersections[N×N]
│   ├── traffic_light (phase: 0/1/2)
│   ├── queue_ns (N-S vehicles)
│   └── queue_ew (E-W vehicles)
│
├── RoadSegments (directed edges)
│   ├── from_intersection
│   ├── to_intersection
│   ├── direction (N/S/E/W)
│   └── vehicles[capacity]
│
Generator
├── Creates vehicles using Poisson process
├── Random origin/destination assignment
└── Tracks vehicle type, time_created

Engine
├── Main loop: step()
├── Moves vehicles via routing
├── Applies controller
└── Tracks metrics
```

### 2. Control Layer (`app/controllers/`)

```
Controller (Interface)
│
├── FixedTimeController
│   ├── cycle_length (e.g., 60s)
│   ├── green_time_ns (30s)
│   ├── green_time_ew (30s)
│   └── Follows predetermined schedule
│
└── AdaptiveController
    ├── min_green (10s)
    ├── max_green (60s)
    ├── queue_threshold (5 vehicles)
    ├── Extends green when queue > threshold
    └── Tracks per-intersection state
```

### 3. Data Layer (`app/models/`)

```
SQLite Database
│
├── ExperimentRecord
│   ├── name, description
│   ├── controller_type
│   ├── grid_size, arrival_rate
│   ├── vehicles_generated/completed
│   ├── avg_travel_time, avg_wait_time
│   └── created_at, completed_at
│
├── TimestepRecord
│   ├── experiment_id (FK)
│   ├── timestep
│   ├── vehicles_in_system
│   └── avg_queue_length
│
└── VehicleRecord
    ├── experiment_id (FK)
    ├── vehicle_id, type
    ├── origin, destination
    ├── distance_traveled
    ├── wait_time, travel_time
    └── completed_at
```

## Data Flow

### Scenario: "User clicks Run for 100 steps"

```
1. Dashboard (browser)
   └─→ POST /api/simulation/run {steps: 100}

2. Flask API (app/main.py)
   └─→ engine.run(100)

3. Simulation Engine
   └─→ for each timestep:
       ├─→ generator.generate_vehicles()
       ├─→ world.step() [advance traffic lights]
       ├─→ engine._move_vehicles() [route all vehicles]
       ├─→ controller.control_step() [update lights]
       └─→ engine._update_metrics()

4. Return results
   └─→ JSON {state, metrics}

5. Dashboard updates display
   └─→ Show metrics in real-time
```

## Routing Algorithm

```
Current Position: Intersection A
Target: Intersection Z

Algorithm: Greedy Manhattan Distance
├── For each outgoing road from A:
│   ├── Check if road is full
│   ├── Calculate distance from next intersection to Z
│   ├── Select road that reduces distance most
│   └── Move vehicle to that intersection
└── Repeat until reached Z
```

## Controller Decision Making

### Fixed Time

```
Time within cycle: 0-30s → Green N-S (phase=1)
Time within cycle: 30-60s → Green E-W (phase=2)
Repeats every 60s
```

### Adaptive

```
State: {phase: 1/2, time_in_phase, current_green_time}

Per timestep:
├── Increment time_in_phase
├── If can_extend AND time < max_green AND queue > threshold:
│   └─→ current_green_time += extension_increment
├── If time >= current_green_time:
│   ├─→ Switch phase (1 ↔ 2)
│   ├─→ Reset time_in_phase
│   └─→ Reset current_green_time to min_green
└── Update intersection.light_phase
```

## Metrics Calculation

```
After each vehicle completes journey:
├── travel_time = current_time - time_created
├── wait_time = (accumulated during journey)
└── distance_traveled = (incremented per move)

Aggregated metrics:
├── vehicles_generated = total created
├── vehicles_completed = total finished
├── avg_travel_time = sum(travel_time) / completed
├── avg_wait_time = sum(wait_time) / completed
└── vehicles_in_system = active vehicles now
```

## Extension Points

```
To add a new controller:
1. Create app/controllers/my_controller.py
2. Implement: class MyController:
   └─→ def control_step(self, world, current_time)
3. Update main.py to import and use it

To add new metrics:
1. Add fields to engine.metrics {}
2. Update _update_metrics() method
3. Display in dashboard

To use different routing:
1. Modify engine._find_next_position()
2. Implement BFS/Dijkstra if needed
```

---

## Performance Characteristics

| Aspect | Complexity | Notes |
|--------|-----------|-------|
| Simulation step | O(V + I + R) | V=vehicles, I=intersections, R=roads |
| Vehicle routing | O(I) | Greedy; could be O(I log I) with BFS |
| Database save | O(V) | Batch insert of vehicle records |
| Memory | O(V + I + R) | Linear with network size |

## Scalability

- **Network size**: Tested with 4×4 (16) to 10×10 (100) intersections
- **Vehicle count**: Supports 1000+ vehicles per simulation
- **Timesteps**: Can run 10,000+ steps per simulation
- **Database**: SQLite efficient for < 100 experiments

For larger networks (1000+ intersections), consider:
- Migrating to PostgreSQL
- Implementing spatial indexing
- Batch vehicle processing

---

This architecture enables easy extension and modification while maintaining clean separation of concerns.

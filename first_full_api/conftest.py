TEST_DB_FILE = "test_tasks.csv"

TEST_TASKS_CSV = [
    {
        "id": 1,
        "title": "test task one",
        "description": "Test description one",
        "status": "Incomplete",
    },
    {
        "id": 2,
        "title": "Test Task Two",
        "description": "Test Description Two",
        "status": "Ongoing",
    },
]

TEST_TASKS = [{**task_json, "id": int(task_json["id"])} for task_json in TEST_TASKS_CSV]

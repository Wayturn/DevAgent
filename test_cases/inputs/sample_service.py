class TaskService:
    def create_task(self, title, description, due_date, user_id):
        if title is None or title == "":
            raise ValueError("title required")

        if user_id is None or user_id <= 0:
            raise ValueError("invalid user_id")

        clean_title = title.strip()
        if clean_title == "":
            raise ValueError("title required")

        task = {
            "title": clean_title,
            "description": description,
            "due_date": due_date,
            "status": "todo",
            "user_id": user_id,
        }

        return task

    def update_task_status(self, task, status, user_id):
        if task is None:
            raise ValueError("task required")

        if user_id is None or user_id <= 0:
            raise ValueError("invalid user_id")

        if task["user_id"] != user_id:
            raise PermissionError("forbidden")

        if status != "todo" and status != "doing" and status != "done":
            raise ValueError("invalid status")

        task["status"] = status
        if status == "done":
            task["completed_at"] = "now"

        return task

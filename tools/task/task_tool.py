import json
import uuid
from typing import Any, Dict, List, Literal, Annotated

from storage import storage
from tools.util import sisyphus_register, sisyphus_tool


class Task:
    id: str
    content: str
    status: str

    def __init__(self, content: str):
        self.content = content
        self.status = "pending"
        self.id = str(uuid.uuid4())

    def to_dict(self):
        return {"id": self.id, "content": self.content, "status": self.status}


class Section:
    id: str
    title: str
    tasks: List[Task]

    def __init__(self, title: str):
        self.id = str(uuid.uuid4())
        self.title = title
        self.tasks = []

    def to_dict(self):
        return {"id": self.id, "title": self.title, "tasks": [t.to_dict() for t in self.tasks]}


class TaskTool:
    def __init__(self):
        sisyphus_register(self)

    @sisyphus_tool
    def create_tasks(self, sections: List[Dict[str, Any]]):
        """
        Create tasks organized by sections. Creates sections automatically if they don't exist. IMPORTANT: Create tasks in the exact order they will be executed. Each task should represent a single, specific operation that can be completed independently. Break down complex operations into individual, sequential tasks to maintain the one-task-at-a-time execution principle.

        Arguments:
            sections: List of sections with their tasks for batch creation. Each section must contain 2 parts: 'title' and 'tasks'.
                      'title' is the title of this section, and 'tasks' is the list of tasks for this section.
                      Below is an example:
                        [
                            {
                                "title": "Setup & Planning",
                                "tasks": [
                                    "Research requirements",
                                    "Create project plan"
                                ]
                            },
                            {
                                "title": "Development",
                                "tasks": [
                                    "Setup environment",
                                    "Write code",
                                    "Add tests"
                                ]
                            },
                            {
                                "title": "Deployment",
                                "tasks": [
                                    "Deploy to staging",
                                    "Run tests",
                                    "Deploy to production"
                                ]
                            }
                        ]

        Returns:
            status: Success or Failed.
            sections: The created data containing allocated ids for each section and task. You should always use the id in the following processing. For example:
                {
                    "status": "Success",
                    "sections": [
                        {
                            "id": "9d5e2b73-701e-4a95-92b2-84aaf0e93ccd",
                            "title": "Setup & Planning",
                            "tasks": [
                                {
                                    "id": "ba5eea4c-d1e7-4ec8-80b6-1646a5bb8eb7",
                                    "content": "Research requirements",
                                    "status": "completed"
                                },
                                {
                                    "id": "8ee55ba6-f0a8-4410-b4d6-88fee6c1687e",
                                    "content": "Create project plan",
                                    "status": "pending"
                                }
                            ]
                        },
                        {
                            "id": "2d7b8ab0-1b15-486a-8ffe-dbc0c25e5ae1",
                            "title": "Development",
                            "tasks": [
                                {
                                    "id": "b273802c-b2cf-4da3-a400-e8662f1e2a76",
                                    "content": "Setup environment",
                                    "status": "pending"
                                },
                                {
                                    "id": "98449602-9578-4d79-ba79-3e12b4cdaeb9",
                                    "content": "Write code",
                                    "status": "pending"
                                },
                                {
                                    "id": "05ead582-e901-4faa-b597-d564d657d2ba",
                                    "content": "Add tests",
                                    "status": "pending"
                                }
                            ]
                        },
                    ]
                }
        """

        created_sections = []
        for section_data in sections:
            section_title_input = section_data["title"]
            task_list = section_data["tasks"]

            target_section = Section(title=section_title_input)

            for task_content in task_list:
                new_task = Task(content=task_content)
                target_section.tasks.append(new_task)
            created_sections.append(target_section)

        storage.set_value("sections", created_sections)
        return json.dumps({"status": "Success", "sections": [s.to_dict() for s in created_sections]})

    @sisyphus_tool
    def view_tasks(self) -> str:
        """
        View current tasks.

        Example return:
        {
            "status": "Success",
            "sections": [
                {
                    "id": "9d5e2b73-701e-4a95-92b2-84aaf0e93ccd",
                    "title": "Setup & Planning",
                    "tasks": [
                        {
                            "id": "ba5eea4c-d1e7-4ec8-80b6-1646a5bb8eb7",
                            "content": "Research requirements",
                            "status": "completed"
                        },
                        {
                            "id": "8ee55ba6-f0a8-4410-b4d6-88fee6c1687e",
                            "content": "Create project plan",
                            "status": "pending"
                        }
                    ]
                },
                {
                    "id": "2d7b8ab0-1b15-486a-8ffe-dbc0c25e5ae1",
                    "title": "Development",
                    "tasks": [
                        {
                            "id": "b273802c-b2cf-4da3-a400-e8662f1e2a76",
                            "content": "Setup environment",
                            "status": "pending"
                        },
                        {
                            "id": "98449602-9578-4d79-ba79-3e12b4cdaeb9",
                            "content": "Write code",
                            "status": "pending"
                        },
                        {
                            "id": "05ead582-e901-4faa-b597-d564d657d2ba",
                            "content": "Add tests",
                            "status": "pending"
                        }
                    ]
                },
            ]
        }
        """
        return json.dumps({"status": "Success", "sections": [s.to_dict() for s in storage.get_value("sections")]})

    @sisyphus_tool
    def update_task(self,
                    section_id: Annotated[str, "Section ID to which task(s) belong"],
                    task_ids: Annotated[List[
                        str], "Task ID (string) or array of task IDs to update. EFFICIENT APPROACH: Batch multiple completed tasks into a single call rather than making multiple consecutive update calls. Always maintain sequential execution order."],
                    status: Annotated[Literal[
                        "pending", "completed", "cancelled"], "New status for the task(s). Set to 'completed' for finished tasks. Batch multiple completed tasks when possible."],
                    ) -> str:
        """
        Update one or more tasks. EFFICIENT BATCHING: Before calling this tool, think about what tasks you have completed and batch them into a single update call. This is more efficient than making multiple consecutive update calls. Always execute tasks in the exact sequence they appear, but batch your updates when possible. Update task status to 'completed' after finishing each task, and consider batching multiple completed tasks into one call rather than updating them individually.
        """
        current_sections = storage.get_value("sections")

        # section_map = [section.id for section in current_sections]
        # if section_id not in section_map:
        #     return f"Invalid section id. Current section ids: {section_map}"

        for i, section in enumerate(current_sections):
            if section.id == section_id:
                for j, task in enumerate(section.tasks):
                    if task.id in task_ids:
                        task.status = status
                        current_sections[i].tasks[j] = task

        storage.set_value("sections", current_sections)

        return json.dumps({"status": "Success", "sections": [s.to_dict() for s in storage.get_value("sections")]})

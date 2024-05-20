import os
import pickle
import json
import csv
import collections
import matplotlib.pyplot as plt
import pandas as pd
from plyer import notification
from colorama import Fore, Style, init

# Инициализация colorama
init(autoreset=True)


class Task:
    def __init__(self, description, priority, due_date=None, labels=None, completed=False,
                 subtasks=None, category=None, is_priority=False, notes=None):
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.labels = labels if labels else []
        self.completed = completed
        self.subtasks = subtasks if subtasks else []
        self.category = category
        self.is_priority = is_priority
        self.notes = notes if notes else ""

    def __repr__(self):
        return (f"Task(description='{self.description}', priority='{self.priority}', "
                f"due_date='{self.due_date}', labels={self.labels}, completed={self.completed}, "
                f"subtasks={self.subtasks}, category={self.category}, is_priority={self.is_priority}, "
                f"notes='{self.notes}')")


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def delete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            del self.tasks[task_index]
            print("Task deleted successfully.")
        else:
            print("Invalid task index.")

    def edit_task(self, task_index, new_description, new_priority, new_due_date, new_labels, new_notes):
        if 0 <= task_index < len(self.tasks):
            task = self.tasks[task_index]
            task.description = new_description
            task.priority = new_priority
            task.due_date = new_due_date
            task.labels = new_labels
            task.notes = new_notes
            print("Task edited successfully.")
        else:
            print("Invalid task index.")

    def save_tasks(self, file_name):
        with open(file_name, 'wb') as f:
            pickle.dump(self.tasks, f)
        print("Tasks saved successfully.")

    def load_tasks(self, file_name):
        if os.path.exists(file_name):
            with open(file_name, 'rb') as f:
                self.tasks = pickle.load(f)
            print("Tasks loaded successfully.")
        else:
            print("No saved tasks found.")

    def search_tasks_by_keyword(self, keyword):
        found_tasks = [task for task in self.tasks if keyword.lower() in task.description.lower()]
        if found_tasks:
            print("Found tasks:")
            for task in found_tasks:
                print(f"{task.description} - Priority: {task.priority} - Due Date: {task.due_date}")
        else:
            print("No tasks found with the given keyword.")

    def set_task_completed(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].completed = True
            print("Task marked as completed.")
        else:
            print("Invalid task index.")

    def sort_tasks(self, criterion):
        if criterion == "priority":
            self.tasks.sort(key=lambda x: x.priority)
        elif criterion == "due_date":
            self.tasks.sort(key=lambda x: x.due_date or "")
        elif criterion == "status":
            self.tasks.sort(key=lambda x: x.completed)
        print("Tasks sorted successfully.")

    def add_subtask(self, task_index, subtask_description):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].subtasks.append(subtask_description)
            print("Subtask added successfully.")
        else:
            print("Invalid task index.")

    def set_label_priority(self, label, priority):
        for task in self.tasks:
            if label in task.labels:
                task.priority = priority
        print("Label priority set successfully.")

    def filter_tasks_by_label_priority(self, label, priority):
        filtered_tasks = [task for task in self.tasks if label in task.labels and task.priority == priority]
        if filtered_tasks:
            print("Filtered tasks:")
            for task in filtered_tasks:
                print(f"{task.description} - Priority: {task.priority} - Due Date: {task.due_date}")
        else:
            print("No tasks matching the filter.")

    def export_tasks_to_json(self, json_file):
        with open(json_file, 'w') as f:
            json.dump([task.__dict__ for task in self.tasks], f, indent=4)
        print("Tasks exported to JSON successfully.")

    def import_tasks_from_json(self, json_file):
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                tasks_data = json.load(f)
                self.tasks = [Task(**data) for data in tasks_data]
            print("Tasks imported from JSON successfully.")
        else:
            print("No JSON file found.")

    def export_tasks_to_csv(self, csv_file):
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['Description', 'Priority', 'Due Date', 'Labels', 'Completed', 'Subtasks', 'Category', 'Is Priority',
                 'Notes'])
            for task in self.tasks:
                writer.writerow([task.description, task.priority, task.due_date, ",".join(task.labels), task.completed,
                                 ",".join(task.subtasks), task.category, task.is_priority, task.notes])
        print("Tasks exported to CSV successfully.")

    def import_tasks_from_csv(self, csv_file):
        if os.path.exists(csv_file):
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                self.tasks = [Task(row['Description'], row['Priority'], row['Due Date'], row['Labels'].split(','),
                                   row['Completed'] == 'True', row['Subtasks'].split(','), row['Category'],
                                   row['Is Priority'] == 'True', row['Notes']) for row in reader]
            print("Tasks imported from CSV successfully.")
        else:
            print("No CSV file found.")

    def visualize_task_priorities(self):
        priorities = [task.priority for task in self.tasks]
        priority_counts = pd.Series(priorities).value_counts()
        priority_counts.plot(kind='bar')
        plt.xlabel('Priority')
        plt.ylabel('Number of Tasks')
        plt.title('Task Priorities')
        plt.show()

    def analyze_task_due_dates(self):
        due_dates = [task.due_date for task in self.tasks if task.due_date]
        due_dates_counts = pd.Series(due_dates).value_counts().sort_index()
        due_dates_counts.plot(kind='bar')
        plt.xlabel('Due Date')
        plt.ylabel('Number of Tasks')
        plt.title('Task Due Dates')
        plt.show()

    def filter_tasks_by_due_date(self, due_date):
        filtered_tasks = [task for task in self.tasks if task.due_date == due_date]
        if filtered_tasks:
            print("Filtered tasks:")
            for task in filtered_tasks:
                print(f"{task.description} - Priority: {task.priority} - Due Date: {task.due_date}")
        else:
            print("No tasks matching the filter.")

    def analyze_task_completion_days(self):
        if self.tasks:
            completed_tasks = [task for task in self.tasks if task.completed]
            if completed_tasks:
                completion_dates = pd.to_datetime([task.due_date for task in completed_tasks])
                completion_dates.dt.dayofweek.value_counts().sort_index().plot(kind='bar')
                plt.xlabel('Day of Week (0=Monday, 6=Sunday)')
                plt.ylabel('Number of Completed Tasks')
                plt.title('Task Completion by Day of Week')
                plt.show()
            else:
                print("No completed tasks to analyze.")
        else:
            print("No tasks to analyze.")

    def set_task_category(self, task_index, category):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].category = category
            print("Task category set successfully.")
        else:
            print("Invalid task index.")

    def filter_tasks_by_category(self, category):
        filtered_tasks = [task for task in self.tasks if task.category == category]
        if filtered_tasks:
            print("Filtered tasks:")
            for task in filtered_tasks:
                print(f"{task.description} - Priority: {task.priority} - Due Date: {task.due_date}")
        else:
            print("No tasks matching the filter.")

    def generate_productivity_report(self, start_date, end_date):
        if self.tasks:
            completed_tasks = [task for task in self.tasks if
                               task.completed and start_date <= task.due_date <= end_date]
            incomplete_tasks = [task for task in self.tasks if
                                not task.completed and start_date <= task.due_date <= end_date]
            print(f"Productivity Report ({start_date} to {end_date}):")
            print(f"Completed Tasks: {len(completed_tasks)}")
            print(f"Incomplete Tasks: {len(incomplete_tasks)}")
            if completed_tasks:
                print("Completed tasks:")
                for task in completed_tasks:
                    print(f"{task.description} - Priority: {task.priority} - Due Date: {task.due_date}")
            if incomplete_tasks:
                print("Incomplete tasks:")
                for task in incomplete_tasks:
                    print(f"{task.description} - Priority: {task.priority} - Due Date: {task.due_date}")
        else:
            print("No tasks to report.")

    def notify_due_tasks(self):
        for task in self.tasks:
            if not task.completed and task.due_date:
                due_date = pd.to_datetime(task.due_date)
                if pd.Timestamp.now() > due_date:
                    notification_title = f"Task '{task.description}' is overdue!"
                    notification_message = f"The due date for task '{task.description}' was {task.due_date}"
                    notification.notify(title=notification_title, message=notification_message,
                                        app_name="Task Manager", timeout=10)
                elif (due_date - pd.Timestamp.now()).days == 1:
                    notification_title = f"Task '{task.description}' is due tomorrow!"
                    notification_message = f"The due date for task '{task.description}' is tomorrow, {task.due_date}"
                    notification.notify(title=notification_title, message=notification_message,
                                        app_name="Task Manager", timeout=10)

    def mark_task_as_priority(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].is_priority = True
            print("Task marked as priority.")
        else:
            print("Invalid task index.")

    def view_tasks_with_priority(self):
        if self.tasks:
            print("Tasks:")
            for index, task in enumerate(self.tasks):
                status = "Completed" if task.completed else "Pending"
                priority_indicator = (Fore.RED + "[Priority]" + Style.RESET_ALL
                                      if task.is_priority else "")
                print(f"{index + 1}. {priority_indicator} {task.description} - "
                      f"Priority: {task.priority} - Due Date: {task.due_date} - Status: {status}")
                if task.subtasks:
                    print("   Subtasks:")
                    for subtask in task.subtasks:
                        print(f"   - {subtask}")
                if task.notes:
                    print(f"   Notes: {task.notes}")
        else:
            print("No tasks.")

    def add_task_notes(self, task_index, notes):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].notes = notes
            print("Notes added successfully.")
        else:
            print("Invalid task index.")

    def count_tasks_by_priority(self):
        priority_counts = collections.Counter(task.priority for task in self.tasks)
        print("Task counts by priority:")
        for priority, count in priority_counts.items():
            print(f"Priority {priority}: {count} task(s)")

    def count_tasks_by_category(self):
        category_counts = collections.Counter(task.category for task in self.tasks)
        print("Task counts by category:")
        for category, count in category_counts.items():
            print(f"Category {category}: {count} task(s)")

    def view_tasks(self):
        if self.tasks:
            print("Tasks:")
            for index, task in enumerate(self.tasks):
                status = "Completed" if task.completed else "Pending"
                priority_indicator = (Fore.RED + "[Priority]" + Style.RESET_ALL
                                      if task.is_priority else "")
                print(f"{index + 1}. {priority_indicator} {task.description} - "
                      f"Priority: {task.priority} - Due Date: {task.due_date} - Status: {status}")
                print(f"   Category: {task.category}")
                print(f"   Labels: {', '.join(task.labels)}")
                if task.subtasks:
                    print("   Subtasks:")
                    for subtask in task.subtasks:
                        print(f"   - {subtask}")
                if task.notes:
                    print(f"   Notes: {task.notes}")
        else:
            print("No tasks.")

    def list_all_labels(self):
        label_counts = collections.Counter(label for task in self.tasks for label in task.labels)
        print("All labels and task counts:")
        for label, count in label_counts.items():
            print(f"Label {label}: {count} task(s)")

    def merge_task_lists(self, other_task_manager):
        self.tasks.extend(other_task_manager.tasks)
        print("Task lists merged successfully.")

    def generate_daily_report(self):
        today = pd.Timestamp.now().strftime('%Y-%m-%d')
        tasks_today = [task for task in self.tasks if task.due_date == today]
        print(f"Daily Report for {today}:")
        print(f"Total tasks: {len(tasks_today)}")
        for task in tasks_today:
            status = "Completed" if task.completed else "Pending"
            priority_indicator = (Fore.RED + "[Priority]" + Style.RESET_ALL
                                  if task.is_priority else "")
            print(f"{task.description} - Priority: {task.priority} - Status: {status} {priority_indicator}")
            if task.subtasks:
                print("   Subtasks:")
                for subtask in task.subtasks:
                    print(f"   - {subtask}")

    @staticmethod
    def save_report_to_file(report, filename):
        with open(filename, 'w') as f:
            f.write(report)
        print(f"Report saved to {filename} successfully.")


def main():
    task_manager = TaskManager()
    file_name = "tasks.pkl"

    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. Delete Task")
        print("3. View Tasks")
        print("4. Edit Task")
        print("5. Save Tasks")
        print("6. Load Tasks")
        print("7. Search Tasks by Keyword")
        print("8. Set Task Completed")
        print("9. Sort Tasks")
        print("10. Add Subtask")
        print("11. Set Label Priority")
        print("12. Filter Tasks by Label Priority")
        print("13. Export Tasks to JSON")
        print("14. Import Tasks from JSON")
        print("15. Export Tasks to CSV")
        print("16. Import Tasks from CSV")
        print("17. Visualize Task Priorities")
        print("18. Analyze Task Due Dates")
        print("19. Filter Tasks by Due Date")
        print("20. Analyze Task Completion Days")
        print("21. Set Task Category")
        print("22. Filter Tasks by Category")
        print("23. Generate Productivity Report")
        print("24. Notify Due Tasks")
        print("25. Mark Task as Priority")
        print("26. View Tasks with Priority")
        print("27. Add Notes to Task")
        print("28. Sort Tasks by Status")
        print("29. Count Tasks by Priority")
        print("30. Count Tasks by Category")
        print("31. List All Labels")
        print("32. Merge Task Lists")
        print("33. Generate Daily Report")
        print("34. Save Report to File")
        print("35. Exit")

        choice = input("Enter your choice: ")

        match choice:
            case '1':
                description = input("Enter task description: ")
                priority = input("Enter task priority: ")
                due_date = input("Enter due date (optional, format: YYYY-MM-DD): ")
                labels = input("Enter task labels (optional, separated by comma): ").split(',')
                task = Task(description, priority, due_date, labels)
                task_manager.add_task(task)
            case '2':
                task_index = int(input("Enter task index to delete: ")) - 1
                task_manager.delete_task(task_index)
            case '3':
                task_manager.view_tasks()
            case '4':
                task_index = int(input("Enter task index to edit: ")) - 1
                new_description = input("Enter new description: ")
                new_priority = input("Enter new priority: ")
                new_due_date = input("Enter new due date (optional, format: YYYY-MM-DD): ")
                new_labels = input("Enter new labels (optional, separated by comma): ").split(',')
                new_notes = input("Enter new notes (optional): ")
                task_manager.edit_task(task_index, new_description, new_priority, new_due_date, new_labels, new_notes)
            case '5':
                task_manager.save_tasks(file_name)
            case '6':
                task_manager.load_tasks(file_name)
            case '7':
                keyword = input("Enter keyword to search: ")
                task_manager.search_tasks_by_keyword(keyword)
            case '8':
                task_index = int(input("Enter task index to mark as completed: ")) - 1
                task_manager.set_task_completed(task_index)
            case '9':
                criterion = input("Enter sort criterion (priority, due_date, status): ")
                task_manager.sort_tasks(criterion)
            case '10':
                task_index = int(input("Enter task index to add subtask: ")) - 1
                subtask_description = input("Enter subtask description: ")
                task_manager.add_subtask(task_index, subtask_description)
            case '11':
                label = input("Enter label name: ")
                priority = input("Enter priority for the label: ")
                task_manager.set_label_priority(label, priority)
            case '12':
                label = input("Enter label name: ")
                priority = input("Enter priority for the label: ")
                task_manager.filter_tasks_by_label_priority(label, priority)
            case '13':
                json_file = input("Enter JSON file name to export tasks: ")
                task_manager.export_tasks_to_json(json_file)
            case '14':
                json_file = input("Enter JSON file name to import tasks from: ")
                task_manager.import_tasks_from_json(json_file)
            case '15':
                csv_file = input("Enter CSV file name to export tasks: ")
                task_manager.export_tasks_to_csv(csv_file)
            case '16':
                csv_file = input("Enter CSV file name to import tasks from: ")
                task_manager.import_tasks_from_csv(csv_file)
            case '17':
                task_manager.visualize_task_priorities()
            case '18':
                task_manager.analyze_task_due_dates()
            case '19':
                due_date = input("Enter due date to filter tasks (format: YYYY-MM-DD): ")
                task_manager.filter_tasks_by_due_date(due_date)
            case '20':
                task_manager.analyze_task_completion_days()
            case '21':
                task_index = int(input("Enter task index to set category: ")) - 1
                category = input("Enter category: ")
                task_manager.set_task_category(task_index, category)
            case '22':
                category = input("Enter category to filter tasks: ")
                task_manager.filter_tasks_by_category(category)
            case '23':
                start_date = input("Enter start date for productivity report (format: YYYY-MM-DD): ")
                end_date = input("Enter end date for productivity report (format: YYYY-MM-DD): ")
                task_manager.generate_productivity_report(start_date, end_date)
            case '24':
                task_manager.notify_due_tasks()
            case '25':
                task_index = int(input("Enter task index to mark as priority: ")) - 1
                task_manager.mark_task_as_priority(task_index)
            case '26':
                task_manager.view_tasks_with_priority()
            case '27':
                task_index = int(input("Enter task index to add notes: ")) - 1
                notes = input("Enter notes: ")
                task_manager.add_task_notes(task_index, notes)
            case '28':
                criterion = "status"
                task_manager.sort_tasks(criterion)
            case '29':
                task_manager.count_tasks_by_priority()
            case '30':
                task_manager.count_tasks_by_category()
            case '31':
                task_manager.list_all_labels()
            case '32':
                other_task_manager = TaskManager()
                task_manager.merge_task_lists(other_task_manager)
            case '33':
                task_manager.generate_daily_report()
            case '34':
                report = input("Enter the report text: ")
                filename = input("Enter the filename to save the report: ")
                task_manager.save_report_to_file(report, filename)
            case '35':
                break
            case _:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

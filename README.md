
# PriorityPath

PriorityPath is a comprehensive task management application built with Django, designed to streamline task assignment, tracking, and completion. It offers features for managing tasks, workers, teams, projects, and more, with a user-friendly interface for efficient workflow management.

## Project Description

PriorityPath provides a robust platform for managing tasks and projects within an organization. The application supports features such as task creation, updating, deletion, and completion tracking. It also allows for managing workers, teams, and project details, with advanced functionalities like search, dynamic progress bars, and deadline warnings.

## Check it out!
[it task manager project deployed to Render](https://it-task-manager-qef9.onrender.com)

## Technologies Used

- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Bootstrap 5**: A popular CSS framework for building responsive, mobile-first websites.
- **Crispy Forms**: A Django package for enhancing the appearance of forms.
- **SQLite**: Default database for development; can be replaced with other databases like PostgreSQL for production.
- **HTML/CSS**: For structuring and styling web pages.
- **JavaScript**: For client-side interactions and dynamic content updates.

## Database Schema
![image](https://github.com/user-attachments/assets/24c1b4c8-3f0e-43d3-bc0d-3f0aa73edf25)


### Models

- **Position**
  - `name`: CharField (unique)
  - *Represents a job position within the organization.*

- **TaskType**
  - `name`: CharField (unique)
  - *Represents a type of task.*

- **Tag**
  - `name`: CharField
  - *Represents tags that can be associated with tasks.*

- **Team**
  - `name`: CharField
  - *Represents a team in the organization.*

- **Project**
  - `name`: CharField
  - `description`: TextField
  - `teams`: ManyToManyField (Team)
  - *Represents a project that can be associated with multiple teams.*

- **Worker**
  - `user`: OneToOneField (AbstractUser)
  - `position`: ForeignKey (Position)
  - `team`: ForeignKey (Team)
  - *Represents a worker, extending Django's AbstractUser to include additional fields.*

- **Task**
  - `name`: CharField
  - `description`: TextField
  - `deadline`: DateField
  - `is_completed`: BooleanField
  - `priority`: CharField (choices: Urgent, High, Medium, Low)
  - `task_type`: ForeignKey (TaskType)
  - `assignees`: ManyToManyField (Worker)
  - `tags`: ManyToManyField (Tag)
  - `project`: ForeignKey (Project)
  - *Represents a task with various attributes including priority, status, and relationships to other models.*
 
    ## Screenshots
### Login page
![image](https://github.com/user-attachments/assets/7bd395c6-ff7a-4a1e-a028-949160caa1b4)

### Homepage
![image](https://github.com/user-attachments/assets/acf74c90-e676-4268-bfde-d17010e7ec26)

*Description: The main dashboard of PriorityPath showing task statistics and recent activities.*

### Task List
![image](https://github.com/user-attachments/assets/d491e23a-d314-47d1-a56c-617074178330)

*Description: The task list view displaying tasks with options search.*

### Task Detail
![image](https://github.com/user-attachments/assets/763adeb8-45ea-4105-8313-c604a62d5d39)

*Description: The detailed view of a specific task with options for updating and managing task details.*
![image](https://github.com/user-attachments/assets/a6d018fe-159c-44d3-a26a-16cee0eb9e0f)

### User Task
![image](https://github.com/user-attachments/assets/86e17a1d-ef7a-426b-a525-b6ec1bc512fd)
*Description: The page displaying tasks assigned to the logged-in user

### Completed Tasks
![image](https://github.com/user-attachments/assets/f82eaba3-cce7-42d6-90c1-c6054071e3f8)
*Description: The page showing a list of completed tasks for all users.*

### Create/Edit Task and deleted
![image](https://github.com/user-attachments/assets/61d6f8c4-31c0-4aaf-9798-0ea78c4a445d)
![image](https://github.com/user-attachments/assets/adb382e4-3e6d-47c1-8ba5-02bb4d645a3a)
*Description: The form for creating or editing and deleted a task.*

### Task Type List
![image](https://github.com/user-attachments/assets/b24e78cf-b913-46a2-89e7-9c7b7c946842)

*Description: The page displaying the list of task types.*

### Position List
![image](https://github.com/user-attachments/assets/84bf51fa-d46b-4e7e-871f-4842a95e9d0f)

*Description: The page displaying the list of positions.*

### Delete Position
![image](https://github.com/user-attachments/assets/928e0c3f-7554-4858-8a12-71845731724b)

*Description: The confirmation page for deleting a position.*

### Logout
![image](https://github.com/user-attachments/assets/73de101c-e4ab-4675-a02e-aef187fbf9c7)

*Description: The logout page allowing users to log out of the application.*

<br />

## Installation Instructions

> 👉 Download the code  

```bash
$ git clone https://github.com/OLENA-KALITSINSKA/it-task-manager.git
$ cd prioritypath
```

<br />

> 👉 Install modules via `VENV`  

```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

<br />

> 👉 Set Up Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> 👉 Create the Superuser

```bash
$ python manage.py createsuperuser
```

<br />

> 👉 Start the app

```bash
$ python manage.py runserver
```

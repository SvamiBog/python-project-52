# Task Manager

### Hexlet tests and linter status:
[![Actions Status](https://github.com/SvamiBog/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/SvamiBog/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/2fbf38fc875542473abe/maintainability)](https://codeclimate.com/github/SvamiBog/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/2fbf38fc875542473abe/test_coverage)](https://codeclimate.com/github/SvamiBog/python-project-52/test_coverage)


## About

This project is a simple task management system built using Django. It allows users to create, update, and delete tasks, assign labels and statuses to tasks, and filter tasks by various criteria (e.g., executor, label, status). The project demonstrates the implementation of CRUD operations, user authentication, and authorization, as well as the use of Django's class-based views and forms.

The main goal of this project is to provide a platform for managing tasks and enhancing productivity by organizing work efficiently. Users can track the progress of tasks, assign responsibility, and manage workflows effectively within a team environment.

The system is built with scalability in mind and can be easily extended with additional features, such as task notifications, more complex filtering, or integration with third-party services.


## Demo

The demo version is available on Railway platform: https://python-project-52-production-a013.up.railway.app/

## Features

- **User Authentication and Authorization**: Secure registration, login, and user access control using Django's built-in authentication system.
- **Task Management**: Create, update, and delete tasks with fields such as task name, description, status, and executor.
- **Task Statuses**: Assign custom statuses (e.g., "New", "In Progress", "Completed") to tasks for better organization.
- **Labeling System**: Create and assign labels to tasks for categorization and easy filtering.
- **Task Filtering**: Filter tasks by executor, label, status, and the author of the task, helping users focus on specific tasks.
- **CRUD Operations**: Fully functional CRUD (Create, Read, Update, Delete) operations for tasks, statuses, and labels.
- **Protection Against Deletion**: Tasks, statuses, and labels that are in use are protected from deletion to avoid accidental data loss.
- **Multilingual Support**: The application uses Django's translation features to provide multi-language support (e.g., English, Russian).
- **Responsive UI**: User-friendly and responsive design for both desktop and mobile use.
- **Success and Error Messages**: User feedback with success and error messages for actions like creating, updating, or deleting tasks and labels.


## Details

This task management application allows users to create, update, and delete tasks with assigned statuses, labels, and executors. Below are some key details about the application:

- **Technology Stack**:
  - Python 3.10
  - Django 5.0: Web framework for building the application.
  - Bootstrap: Used for responsive UI design.
  - PostgreSQL: Database system for storing data.
  
- **Core Models**:
  - **User**: Handles user authentication and permissions.
  - **Task**: Represents tasks with fields like name, description, status, and executor.
  - **Status**: Used to manage the different states a task can be in (e.g., "New", "Completed").
  - **Label**: Categorizes tasks for better filtering and management.

- **Task Workflow**:
  1. Users can create new tasks, assign statuses and labels, and designate executors.
  2. Tasks can be filtered based on status, executor, or label.
  3. Tasks can be updated with new details, status changes, or reassignments.
  4. Users can delete tasks that are no longer relevant, with appropriate protections to prevent accidental deletions.

- **Security Features**:
  - Only authenticated users can perform actions such as creating, editing, or deleting tasks.
  - Deletion of entities like labels or statuses is protected if they are associated with tasks.
  
- **Internationalization**:
  - The application is equipped with support for multiple languages using Django’s translation system.
  
- **Testing**:
  - The application includes unit tests to ensure the stability of its features and functionality.

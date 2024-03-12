# Tiko Energy

Coding challenge by Tiko Energy.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Testing](#testing)
7. [Code coverage](#Code-coverage)
8. [API Documentation](#api-documentation)


## Introduction

This is an Event manager app which allow organisers to create and manage events and allow users to attend the events.

## Features
- Users can register an account using Email and password.
- Users can log in to get access token and refresh token.
- Access token with lifetime of 1 hour.
- Refresh token with lifetime of 1 day.
- Users can Create event after login.
- Users can Update only events they have created.
- Users can list all events.
- Users can filter events by owner and other fields.
- Users can cancel only events they have created.
- Users can subscribe or unsubscribe to events
- Events have validation


## Requirements

Requirements can be found in the requirements.txt file

## Installation

1. Create venv and Clone the repository:
   ```bash
   mkdir app
   python3.11 -m venv venv 
   source venv/bin/activate    
   cd app
   git clone https://github.com/hashaaamm/tiko_energy.git
   cd app
   ```
   
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
3. Run migrations:
   ```bash
   python manage.py makemigrations 
   python manage.py migrate
   ```

## Usage

1. Create superuser:
   ```bash
   python manage.py createsuperuser 
   ```

2. Start the server:
   ```bash
   python manage.py runserver
   ```
3. Access admin at http://127.0.0.1:8000/admin/

## Testing

1. Run Test:
   ```bash
   pytest
   ```

## Code coverage

1. To check coverage:
   ```bash
   pytest -p no:warnings --cov=.
   ```

## API Documentation

1. Access API docs at http://127.0.0.1:8000/api/swagger-docs/

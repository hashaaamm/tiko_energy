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

This is an Event manager app which allow organisers to create and manage events and allow users to attend the events

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

## Code coverage

## API Documentation

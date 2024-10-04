# just-words

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Setup Instructions](#setup-instructions)
4. [Usage Guide](#usage-guide)

## Project Overview
Personalized AI email generator based on user profile and recommendations

## Technology Stack
- Frontend: React with TypeScript, Ant Design
- Backend: Python with FastAPI
- Database: PostgreSQL
- AI Integration: OpenAI's GPT models

## Setup Instructions

### Prerequisites
- Node.js and npm
- Python 3.8+
- PostgreSQL
- OpenAI API key

### Backend Setup
1. Clone the repository:
   ```
   git clone [https://github.com/TanviBhardwaj24/just-words.git)](https://github.com/TanviBhardwaj24/just-words.git)
   cd just-words/backend
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  
   ```

3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your api key 
   DATABASE_URL=Set up your PostgreSQL database and update the url
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```
   cd ../frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

## Usage Guide

### Running the Application
1. Start the backend server:
   ```
   cd backend
   uvicorn main:app --reload
   ```

2. In a new terminal, start the frontend development server:
   ```
   cd frontend
   npm start
   ```

3. Access the application at `http://localhost:3000`



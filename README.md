# APITransUnity

TransUnity is a straightforward project dedicated to unifying the public transportation systems across Chile, leveraging public APIs available from transportation providers. Through innovative web scraping techniques, we aggregate real-time information on routes, schedules, and other essential data.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://https://github.com/Sladon/APITransUnity.git
   cd APITransUnity
   ```

2. **Create a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate    # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```sh
   pip install -r requirements.txt
   ```

### Environment Variables

Create a `.env` file in the root directory of your project and add the following environment variables:

```env
DTPM_POSITION_SERVICE_USER=your_user_name
DTPM_POSITION_SERVICE_PASSWORD=your_password
```

### Running the Application

#### Development

To start the application in development mode with live reload capability,

run: `uvicorn app:app --reload`

#### Production

To start the application in production mode,

run: `uvicorn app:app --host 0.0.0.0 --port 8000`

### API Documentation

Once the application is running, you can access the API documentation at:

Development: http://127.0.0.1:8000/docs
Production: http://yourdomain.com/docs

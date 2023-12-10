# WebSite

## My Django API Project

This is a Django project that implements a simple API endpoint following the structure `api/v1/hello-world-{variant}`.

## Getting Started

### Prerequisites

Make sure you have Python and pip installed on your system. You can install the project dependencies using:

```bash
pip install -r requirements.txt
```

### Running the Project

1. Clone the repository:

   ```bash
   git clone https://github.com/SqueshSvyt/WebSite.git  
   ```

2. Go to the project dir:

   ```bash
   cd .\WebSite
   ```

3. Run migration using command:

    ```bash
   python manage.py makemigrations
   ```
   
    ```bash
   python manage.py migrate
   ```

4. Run the development server:

   ```bash
   python manage.py runserver
   ```

The server will be running at http://127.0.0.1:8000/.

## API Endpoint

### Hello World API

You can download Api documentation by:

```bash
curl http://127.0.0.1:8000/schema/
```

## Testing the API

You can test the API using tools like curl, httpie, or Postman. For example:

```bash
curl http://127.0.0.1:8000/api/v1/hello-world-1/
```

## Contributing

Feel free to contribute to this project. Create a fork, make your changes, and submit a pull request.

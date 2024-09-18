# **MMC Technical Test**

This repository contains the submission for a technical test with a full-stack application consisting of a [React](https://reactjs.org/) frontend and a [FastAPI](https://fastapi.tiangolo.com/) backend.
The project also includes a solution that requires [Solr](https://solr.apache.org/) and [Redis](https://redis.io/) for search and caching functionality.

Please use the following instructions to run the full stack on your local machine.

# **Project Structure**

- `./frontend`: Contains the React application.
- `./backend`: Contains the FastAPI application and related components.
- `./solr-core`: Contains a backup of the Solr core component required for the `/db` endpoint. This is restored to the Docker container when built.

# **Prerequisites**

- You need to have Docker & Docker-Compose installed and running on your machine to build and run the associated Docker containers.

- To check you can run:

  - `docker --version`
  - `docker-compose --version`

# **Setup Instructions**

## **1\. Clone the Repository**

- `git clone https://github.com/rgreenegit/MMC_Test.git`
- `cd MMC_Test`

## **2\. Build Docker Images**

- From within the MMC_test directory, run the following to buid the Docker images using the included `docker-compose.yml` file.

- `docker-compose build`

## **3\. Run Docker Containers**

- `docker-compose up`

## **4\. Accessing the Application**

- **Frontend:**
  - [http://localhost:3000](http://localhost:3000)  
    Three routes have been included in the front end to demonstrate three approaches to the auto complete functionality:
    - [http://localhost:3000](http://localhost:3000) \= Basic prefix matching based solution
    - [http://localhost:3000/trie](http://localhost:3000/trie) \= Trie based solution
    - [http://localhost:3000/db](http://localhost:3000/db) \= Solr & Redis based solution
- **Backend:**
  - [http://localhost:8000](http://localhost:8000)
    - [http://localhost:8000/docs](http://localhost:8000) \= FastAPI Swagger API UI
- **Solr Admin UI:**
  - http://localhost:8983/solr
- **Redis CLI:** Connect to the Redis server with `redis-cli`

## **6\. Tests**

A collection of backend unit tests have been included to demonstrate the use of PyTest and FastAPI testing.

**Run Backend Unit Tests:**

- From the `./backend` directory run:
  - `pytest -v`

## **7\. Troubleshooting**

If you encounter issues with any of the services, make sure they are running and properly configured. Check their respective logs for more details.

- Check Solr is running at http://localhost:8983/solr and check if autocomplete_core exists
- Check Redis is running using `redis-cli` command
- Check FastAPI backend is running at http://localhost:8000/docs and perform API execution tests
- Check React is running at http://localhost:3000

## **8\. Reference**

- [Docker](https://www.docker.com/)
- [React](https://reactjs.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Solr](https://solr.apache.org/)
- [Redis](https://redis.io/)

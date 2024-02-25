# Tokka Assignment

This repository contains the code for the Tokka Assignment, which includes a Flask application with REST endpoints and Docker configuration for containerization.

## Prerequisites

- Docker installed on your system

## Running the Docker Container

1. Clone this repository to your local machine:

    ```bash
    git clone <repository-url>
    ```

2. Navigate to the project directory:

    ```bash
    cd tokka-assignment
    ```

3. Build the Docker image:

    ```bash
    docker build -t tokka_assignment .
    ```

4. Run the Docker container:

    ```bash
    docker run -p 80:80 tokka_assignment
    ```

5. Access the application in your web browser at [http://localhost:80](http://localhost:80).

## Using the REST Endpoints
Once the Docker container is running, please access [http://localhost:80/api/docs](http://localhost:80/api/docs) for the swagger documentation.

If for some reason the swagger endpoint is not working, please refer to the below on the endpoints:

- **Get Fee for Transaction**

    - Endpoint: `http://localhost/api/getFee`
    - Description: Gets fee for a specified transaction hash in USDT.
    - Method: `GET`
    - Parameters: 
        - `transaction_hash`: Transaction hash for which fee needs to be retrieved.
    - Example:
        ```bash
        curl -X GET "http://localhost/api/getFee?transaction_hash=<transaction_hash>"
        ```

- **Get Fee Statistics**

    - Endpoint: `http://localhost/api/getFeeStatistics`
    - Description: Provides min, max and average fee in USDT for transactions that happen between the provided start and end time.
    - Method: `GET`
    - Parameters: 
        - `start_time_ms`: Start time in milliseconds.
        - `end_time_ms`: End time in milliseconds.
    - Example:
        ```bash
        curl -X GET "http://localhost/api/getFeeStatistics?start_time_ms=<start_time_ms>&end_time_ms=<end_time_ms>"
        ```
##Example
<img width="1362" alt="image" src="https://github.com/alages97/tokka-assignment/assets/42828112/919dc983-7ea6-4a27-91dd-ac5df1dc7529">
![image](https://github.com/alages97/tokka-assignment/assets/42828112/ffa526e7-ba77-4bd3-be06-34360df09a89)
As you can see, the output by the system of 14.45 matches what we see on etherscan.io

##Design of system

# 🛰️🖼️ CBERS Color Corrector Backend

## Description

The CBERS Color Corrector Backend is the server-side component of the CBERS Color Corrector plugin for QGIS. It provides the necessary API endpoints for the frontend to correct the colors of CBERS images. The backend processes image tiles and matches them to a reference dataset for color correction.

## Features

1. Process image tiles received from the frontend.
2. Calculate the embedding for each tile using a fine-tuned CLIP (Contrastive Language - Image Pre training) deep learning model.
3. Query the database for the best match using cosine similarity.
4. Return the Cumulative Distribution Function (CDF) of the best match to the frontend.

## Installation

This project utilizes Docker for easy setup. To install:

1. Clone the repository to your local machine.
2. Open your terminal and navigate to the project directory.
3. Run `docker-compose up -d` to start the server.

## Usage

### Server

Once the server is running, the frontend can send requests to the server's exposed endpoints.

### Database

The backend also exposes an endpoint for populating the database with CBERS imagery data.

## Contributing

We welcome any contributions to the CBERS Color Corrector project. Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License - see the LICENSE file for more details.

## Contact

If you have any questions, feedback, or issues, please feel free to contact us.

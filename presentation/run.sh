source config.sh

# Run the Docker image, mounting the slides directory
${CMGR} run --rm -v $(pwd)/slides:/slides -p 8080:8080 ${TAG}

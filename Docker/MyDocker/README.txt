# Check Docker compose Version
docker-compose --version

# Get all the docker image ids
docker image ls -q

# Clean up all the images
docker image rm $(docker image ls -q)

# Clean up all the containers
docker container -f rm $(docker container ls -a -q)

#!sh

# sanity checks and defaults

# if running as root, no need to use sudo
if [ "$UID" = "0" ]; then
    SUDO=""
else
    SUDO=$(which sudo 2>/dev/null)
    if [ ! -x "$SUDO" ]; then
	echo "\`sudo\` is required to run the script!"
	exit 1
    fi
fi

# check for docker-compose
DOCKER_COMPOSE=$(which docker-compose 2>/dev/null)
if [ ! -x "$DOCKER_COMPOSE" ]; then

    # try to run docker compose
    `docker compose > /dev/null 2>&1`
    if [ $? -eq 0 ]; then
	DOCKER_COMPOSE="docker compose"
	echo "Using \`docker compose\`"
    else
	echo "\`docker-compose\` not installed, cannot proceed"
	exit 2
    fi
fi



DOCKER_IMAGE_TO_RUN=$1

# if not an image specified, use the default
if [ -z "$DOCKER_IMAGE_TO_RUN" ]; then
    DOCKER_IMAGE_TO_RUN=pagila_postgresql_docker
    echo "Using default image <$DOCKER_IMAGE_TO_RUN>"
fi

if [ ! -d $DOCKER_IMAGE_TO_RUN ]; then
    echo "Cannot find docker image directory <$DOCKER_IMAGE_TO_RUN>"
    exit 1
fi


cd $DOCKER_IMAGE_TO_RUN
ls 
# check there are the files to run the image
if [ ! -f "docker-compose.yml" ]; then
    echo "Cannot find file 'docker-compose.yml'"
    exit 3
fi

if [ ! -f "Dockerfile" ]; then
    echo "Dockerfile is missing"
    exit 4
fi


echo "Downloading Pagila Database..."
# Download the Pagila schema and data if not already present
if [ ! -f ./init/pagila-schema.sql ]; then
    curl -o ./init/002-pagila-schema.sql https://raw.githubusercontent.com/devrimgunduz/pagila/master/pagila-schema.sql
fi

if [ ! -f ./init/pagila-data.sql ]; then
    curl -o ./init/003-pagila-data.sql https://raw.githubusercontent.com/devrimgunduz/pagila/master/pagila-data.sql
fi
echo "Pagila Database files downloaded."


# now build the container
DOCKER_CONTAINER_NAME=${DOCKER_IMAGE_TO_RUN}_pagiladb_1 
$SUDO $DOCKER_COMPOSE build --force-rm --no-cache
$SUDO $DOCKER_COMPOSE up -d --remove-orphans

if [ $? -ne 0 ]; then
    echo "Cannot start the container $DOCKER_CONTAINER_NAME"
    exit 10
fi


DOCKER_ID=$($SUDO docker ps -qf "name=$DOCKER_CONTAINER_NAME" | awk '{print $1;}' )


SECS=5
echo "Waiting $SECS secs for the container <$DOCKER_CONTAINER_NAME> -> <$DOCKER_ID> to complete starting up..."
sleep $SECS

$SUDO docker exec --user postgres --workdir /var/lib/postgresql -it  $DOCKER_ID /bin/bash

if [ $? -ne 0 ]; then
    echo "Getting the logs to understand what went wrong"
    $SUDO docker logs $DOCKER_CONTAINER_NAME
fi

echo "Stopping the container $DOCKER_CONTAINER_NAME"
$SUDO docker stop $DOCKER_CONTAINER_NAME

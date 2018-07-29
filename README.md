# MOOS Reflector Service
This is a lightweight JSON reflector for connecting two (or more) MOOS communities.

# Requirements
This service requires only a publicly visible IP, docker, and docker-compose. It has been tested with the following versions:
* Docker version 18.06.0-ce, build 0ffa825
* docker-compose version 1.21.2, build a133471

# Theory of Operation
The reflector has a set of channels, each of which can be read or written to via REST calls. Each channel maps to a single REDIS key, and may in principle contain any data that can be stored in a REDIS byte string, but typical payload is a JSON string. Each write to a channel overwrites all previous data. Therefore, the typical mode of operation is that each channel is a one-way one-to-one or one-to-many communication on each channel. Therefore, a bidrectional communication, such as between ship and shore, takes two channels -- a ship to shore and a shore to ship channel.

# Configuration
The only internal configuration required is a file containing a list of channel ids and keys, which is named by the KEY_FILE environment variable in the docker-compose.yml file. The file must conform to the reflector/schema/key_schema.json schema; an example is present in reflector/private/keys-sample.json

# Running the Reflector Service
Start the service by running docker-compose up --build -d in the top level directory.

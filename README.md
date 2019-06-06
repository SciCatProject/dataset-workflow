# dataset-workflow

## Setup Guide

### 1. OpenWhisk

* Clone the [Openwhisk repository](https://github.com/apache/incubator-openwhisk-devtools) and start the Docker containers
  ```
  $ git clone https://github.com/apache/incubator-openwhisk-devtools.git
  $ cd incubator-openwhisk-devtools/docker-compose
  $ make quick-start
  ```
  
  ---
  *To increase the maximum memory limit (default 512 mB) of the OpenWhisk runtimes, open the file* docker-whisk-controller.env *inside the* docker-compose *directory, add the following environment variable and then restart the containers*
  
  ```
  CONFIG_whisk_memory_max=[value in mB, e.g., 2048]m
  ```
  ---

* Copy the file *.wskprops*, located inside the current directory, to your home directory
  ```
  $ cp .wskprops $HOME/
  ```

### 2. OpenWhisk CLI

To interact with OpenWhisk you need to use the OpenWhisk CLI tool `wsk`, here there are two choices
  
* Use the one located in incubator-openwhisk-devtools/docker-compose/openwhisk-src/bin, e.g.,
  ```
  $ cd openwhisk-src
  $ bin/wsk [command]
  ```
  
or, if you're on Mac, you can install it using HomeBrew so that it is added to your PATH
  
* `$ brew install wsk`
  
---
  
*Note that you have to use the -i or --insecure flag with* wsk *, since the docker-compose OpenWhisk uses Self-Signed   Certificates*
    
---

### 3. Kafka Package

First, you need to set the `OPENWHISK_HOME` environment variable to the *openwhisk-src* directory. If you are inside the *docker-compose* directory, run:
```
$ export OPENWHISK_HOME=$PWD/openwhisk-src
```

then, set the following environment variables:
```
$ export AUTH_KEY=`cat $OPENWHISK_HOME/ansible/files/auth.whisk.system`
$ export API_HOST=`wsk -i property get --apihost | awk '{print $NF}' | sed -e 's/https:\/\///'`
$ export DB_URL=http://whisk_admin:some_passw0rd@${API_HOST}:5984
$ export DB_PREFIX=local_
```
 
You can then use the `Makefile` inside the docker-compose directory to set up the OpenWhisk kafkaprovider docker container
```
$ make create-provider-kafka
```
  
This will, however, not run the necessary `installKafka.sh` script, you will have to do that manually afterwards. If you are inside the docker-compose directory:
```
$ cd openwhisk-package-kafka
$ ./installKafka.sh $AUTH_KEY $API_HOST $DB_URL $DB_PREFIX $API_HOST
```
  
To confirm that kafkaFeed has been installed, run:
```
$ wsk -i package get --summary /whisk.system/messaging
```

You should get the following output:
```
package /whisk.system/messaging: Returns a result based on parameters endpoint, isBinaryKey, isBinaryValue, isJSONData, kafka_admin_url, kafka_brokers_sasl, password, topic and user
   (parameters: *endpoint, isBinaryKey, isBinaryValue, isJSONData, kafka_admin_url, kafka_brokers_sasl, password, topic, user)
 action /whisk.system/messaging/kafkaProduce: Deprecated - Produce a message to a Kafka cluster
   (parameters: base64DecodeKey, base64DecodeValue, brokers, key, topic, value)
 action /whisk.system/messaging/messageHubProduce: Deprecated - Produce a message to Message Hub
   (parameters: base64DecodeKey, base64DecodeValue, kafka_brokers_sasl, key, password, topic, user, value)
 feed   /whisk.system/messaging/kafkaFeed: Feed to listen to Kafka messages
   (parameters: brokers, endpoint, isBinaryKey, isBinaryValue, isJSONData, topic)
 feed   /whisk.system/messaging/messageHubFeed: Feed to list to Message Hub messages
   (parameters: endpoint, isBinaryKey, isBinaryValue, isJSONData, kafka_admin_url, kafka_brokers_sasl, password, topic, user)
```

### 4. Creating a trigger

To create a trigger that listens to a Kafka instance, run the following (assuming one Kafka broker running locally):
```
$ wsk -i trigger create MyKafkaTrigger -f /whisk.system/messaging/kafkaFeed -p brokers $API_HOST:9093 -p topic test -p isJSONData true
```

This should give you an output in JSON format, followed by:
```
ok: created trigger MyKafkaTrigger
```

### 5. Creating an action

The example below shows how to create an action that uses the custom python2-mantid runtime:
```
$ wsk -i action create reduce-dataset ./actions/reduce_dataset.py -P config.local.json --docker dacat/openwhisk-python2action-mantid:latest
```

You can create the *config.local.json* file from the *config.local.sample.json* file located in this repository

### 6. Checking logs

You can get a live feed of the logs for different activations by running:
```
wsk -i activation poll
```

To check the logs for a specific activation, run:
```
wsk -i activation logs <activationId>
```

## References

[OpenWhisk Documentation](https://openwhisk.apache.org/documentation.html#documentation)

[OpenWhisk Docker-Compose Documentation](https://github.com/apache/incubator-openwhisk-devtools/blob/master/docker-compose/README.md)

[OpenWhisk CLI Documentation](https://openwhisk.apache.org/documentation.html#wsk-cli)

[Kafka Package Documentation](https://github.com/apache/incubator-openwhisk-package-kafka/blob/master/README.md)

[Kafka Package Dev Guide](https://github.com/apache/incubator-openwhisk-package-kafka/blob/master/devGuide.md)

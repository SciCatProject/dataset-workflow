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

First, you need to set the `OPENWHISK_HOME` environment variable to the *openwhisk-src* directory, i.e.:
```
$ export OPENWHISK_HOME=/path/to/incubator-openwhisk-devtools/docker-compose/openwhisk-src
```
 
You can then use the `Makefile` inside the docker-compose directory to set up the OpenWhisk kafkaprovider docker container
```
$ make create-provider-kafka
```
  
This will, however, not run the necessary `installKafka.sh` script, you will have to do that manually afterwards. If you are inside the docker-compose directory:
```
$ cd openwhisk-package-kafka
$ ./installKafka.sh <authKey> <edgehost> <dburl> <dbprefix> <apihost>
```
  
* authKey
  
  This should be the authKey for the *guest* namespace, which you can get by typing:
  ```
  $ wsk -i property get --auth
  ```

* edgehost

  This the IP address located in your *.wskprops* APIHOST variable **without** the 'https://' prefix
  
* dburl

  The dburl should be of the following format:
  
  `http://whisk_admin:some_passw0rd@<YOUR IP FROM ABOVE>:5984`
  
* dbprefix

  This should be set to `local_`
  
* apihost

  The apihost variable should be the same as the edgehost variable
  
To confirm that kafkaFeed has been installed, run:
```
$ wsk -i package get --summary /[NAMESPACE]/messaging
```

(where NAMESPACE is either *guest* or *whisk.system*, depending on which auth key you chose when running *installKafka.sh*)

You should get the following output:
```
package /[NAMESPACE]/messaging: Returns a result based on parameter endpoint
   (parameters: *endpoint)
 action /[NAMESPACE]/messaging/kafkaProduce: Deprecated - Produce a message to a Kafka cluster
   (parameters: base64DecodeKey, base64DecodeValue, brokers, key, topic, value)
 feed   /[NAMESPACE]/messaging/kafkaFeed: Feed to listen to Kafka messages
   (parameters: brokers, endpoint, isBinaryKey, isBinaryValue, isJSONData, topic)
```

### 4. Creating a trigger

To create a trigger that listens to a Kafka instance, run the following (assuming one Kafka broker running locally):
```
$ wsk -i trigger create MyKafkaTrigger -f /[NAMESPACE]/messaging/kafkaFeed -p brokers "[\"[YOUR IP FROM ABOVE]:9092\"]" -p topic mytopic -p isJSONData true
```

### 5. Creating an action

The example below shows how to create an action that uses the custom python2-mantid runtime:
```
$ wsk -i action create reduce-dataset ./actions/reduce-dataset.py -P config.local.json --docker dacat/openwhisk-python2action-mantid:latest
```

## References

[OpenWhisk Documentation](https://openwhisk.apache.org/documentation.html#documentation)

[OpenWhisk Docker-Compose Documentation](https://github.com/apache/incubator-openwhisk-devtools/blob/master/docker-compose/README.md)

[OpenWhisk CLI Documentation](https://openwhisk.apache.org/documentation.html#wsk-cli)

[Kafka Package Documentation](https://github.com/apache/incubator-openwhisk-package-kafka/blob/master/README.md)

[Kafka Package Dev Guide](https://github.com/apache/incubator-openwhisk-package-kafka/blob/master/devGuide.md)

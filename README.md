# dataset-workflow

## Setup Guide

### OpenWhisk

* Clone the [Openwhisk repository](https://github.com/apache/incubator-openwhisk-devtools) and start the Docker containers
  ```
  git clone https://github.com/apache/incubator-openwhisk-devtools.git
  cd incubator-openwhisk-devtools/docker-compose
  make quick-start
  ```

* Copy the file *.wskprops*, located inside the current directory, to your home directory
  ```
  cp .wskprops $HOME/
  ```
  
### OpenWhisk CLI

To interact with OpenWhisk you need to use the OpenWhisk CLI tool `wsk`, here there are two choices
  
* Use the one located in incubator-openwhisk-devtools/docker-compose/openwhisk-src/bin, e.g.,
  ```
  cd openwhisk-src
  bin/wsk [command]
  ```
  
or, if you're on Mac, you can install it using HomeBrew so that it is added to your PATH
  
* `brew install wsk`
  
---
  
*Note that you have to use the -i or --insecure flag with* wsk *, since the docker-compose OpenWhisk uses Self-Signed Certificates*
  
---

### Kafka Package

* You can use the `Makefile` inside the docker-compose directory to set up the OpenWhisk kafkaprovider docker container
  ```
  make create-provider-kafka
  ```
  
This will, however, not run the necessary `installKafka.sh` script, you will have to do that manually afterwards. If you are inside the docker-compose directory:
```
cd openwhisk-package-kafka
./installKafka.sh <authKey> <edgehost> <dburl> <dbprefix> <apihost>
```
  
* autKey
  
  * To install the package under the *guest* namespace, use the key located in your *.wskprops* AUTH variable
  * To install the package under the *wisk.system* namespace, use the key located in 
  
    `incubator-openwhisk-devtools/docker-compose/openwhisk-src/ansible/files/auth.whisk.system`

* edgehost

  This the IP address located in your *.wskprops* APIHOST variable **without** the 'https://' prefix
  
* dburl

  The dburl should be of the following format:
  
  `https://whisk_admin:some_passw0rd@<YOUR IP FROM ABOVE>:5984`
  
* dbprefix

  This should be set to `ow_kafka_triggers`
  
* apihost

  The apihost variable should be the same as the edgehost variable
  
To confirm that kafkaFeed has been installed, run:
```
wsk -i package get --summary /[NAMESPACE]/messaging
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

### Creating a trigger

To create a trigger that listens to a Kafka instance, run the following (assuming one Kafka broker running locally):
```
$ wsk -i trigger create MyKafkaTrigger -f /[NAMESPACE]/messaging/kafkaFeed -p brokers "[\"[YOUR IP FROM ABOVE]:9092\"]" -p topic mytopic -p isJSONData true
```

## References

[OpenWhisk Documentation](https://openwhisk.apache.org/documentation.html#documentation)

[OpenWhisk Docker-Compose Documentation](https://github.com/apache/incubator-openwhisk-devtools/blob/master/docker-compose/README.md)

[OpenWhisk CLI Documentation](https://openwhisk.apache.org/documentation.html#wsk-cli)

[Kafka Package Documentation](https://github.com/apache/incubator-openwhisk-package-kafka/blob/master/README.md)

[Kafka Package Dev Guide](https://github.com/apache/incubator-openwhisk-package-kafka/blob/master/devGuide.md)

# CleaningRecordAPI
Cleaning Records API Source Code

docker network create KafkaNetwork
docker network connect KafkaNetwork cleaningrecordapi_app_1
docker network connect KafkaNetwork broker

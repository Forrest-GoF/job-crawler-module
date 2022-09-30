cd flask;
docker build -t rilac1/job-crawler-module_flask .;
docker push rilac1/job-crawler-module_flask;

docker buildx build --platform linux/amd64 --load -t rilac1/job-crawler-module_flask:amd64 .;
docker push rilac1/job-crawler-module_flask:amd64;
cd ..;
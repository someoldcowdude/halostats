docker stop halostats
docker rm halostats
docker build -t zgardler/halostats:test .
docker run -v $(pwd):/app -d --name halostats -p 80:5000 zgardler/halostats:test

sleep 2
curl localhost



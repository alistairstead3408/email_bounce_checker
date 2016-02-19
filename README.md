# email-bounce-checker
Tiny server for checking the email bounce email and making requests to isaac-api to update users.

## Installation / Setup instructions
-

Your server should be running on port `http://localhost:9090/check`

### Production
Deploy to dockerhub: `docker push ucamcldtg/email-bounce-checker`

The Docker container is available from [dockerhub](https://registry.hub.docker.com/u/ucamcldtg/email-bounce-checker/) by running: docker pull ucamcldtg/email-bounce-checker . This is useful for production use.

### isaac-dev

The following commands (as root) got it working. The `PYTHONUNBUFFERED` stuff is to make sure stdout is captured properly in logs.

```
docker pull ucamcldtg/email-bounce-checker
docker run -d -p 5000:5000 -e PYTHONUNBUFFERED=0 --name email-bounce-checker ucamcldtg/email-bounce-checker
```

To see live output:

```
docker logs -f email-bounce-checker
```

Before pulling new version:

```
docker rm email-bounce-checker
```
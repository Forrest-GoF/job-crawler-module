# job-crawler-module

### 1) Local Build (without nginx)
```sh 
git clone https://github.com/Forrest-GoF/job-crawler-module.git
```

```sh
pip install -r requirements.txt
```

```sh
cd flask; flask run
```

```sh
curl 127.0.0.1:5000
```


### 2) Docker (with Nginx)
1. download `docker-compose.yaml`
2. `docker-compose up -d`

#### Image versions
- _latest_ : for **arm**
- _amd64_ : for **x86**
  
> If your development environment is `x86`, use the image version of `amd64`.

#### Docker Hub
- [job-crawler-module_flask](https://hub.docker.com/repository/docker/rilac1/job-crawler-module_flask)
- [job-crawler-module_nginx](https://hub.docker.com/repository/docker/rilac1/job-crawler-module_nginx)

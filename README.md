#42-test-alexbazer


* GetBarista project - http://getbarista.com/project/2589/
* GetBarista link - http://fortytwotesttask-198.alexbazer.at.getbarista.com
* GitHab project - https://github.com/AlexBazer/FortyTwoTestTask

## Prepare virtual env
* Create virtual env and install pip requirements 
* install bower requirements
```
virtualenv --no-site-packages env
pip install -r requirements.txt
bower install
```

## Run Tests
```
make test
```

## Run local server
```
make run
``` 
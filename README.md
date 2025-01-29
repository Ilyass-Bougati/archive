# Archive
This application is a software that you can run on your old laptop or pc to turn it into an archive, I do not advise using it for anything serious.


# Running the project
## Directly
you only need to install the requirements the run the application

```bash
pip install -r requirements.txt
python app.py
```
for debugging

```bash
python app.py debug
```

## Docker
You can build and run the project using the following comands

```bash
docker build . -t archive:v1
docker run -p 80:5000 archive:v1
```

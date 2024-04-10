# meduzzen-internship

Welcome to my Meduzzen internship practice work.

### Installation & Setup
1. Clone this repository:

````angular2html
git clone https://github.com/nataliia-petrushak/meduzzen-intership.git
````
2. Install the required dependencies using pip:
````angular2html
pip install -r requirements.txt
````
3. In root directory build a Docker image:
````angular2html
docker build -t app .  
````
4. Start your Docker container:
````angular2html
docker run -d --name mycontainer -p 8000:8000 app
````

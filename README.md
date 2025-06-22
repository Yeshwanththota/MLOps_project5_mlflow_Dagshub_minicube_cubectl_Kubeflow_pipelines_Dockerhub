
## 🧰 Tech Stack

<p align="left">
  <img src="https://img.shields.io/badge/Mlflow-0175C2?style=for-the-badge&logo=mlflow&logoColor=white" alt="MLflow"/>
  <img src="https://img.shields.io/badge/Dagshub-000000?style=for-the-badge&logo=dagshub&logoColor=white" alt="Dagshub"/>
  <img src="https://img.shields.io/badge/Minikube-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" alt="Minikube"/>
  <img src="https://img.shields.io/badge/Kubectl-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" alt="Kubectl"/>
  <img src="https://img.shields.io/badge/Kubeflow_Pipelines-0098DB?style=for-the-badge&logo=kubeflow&logoColor=white" alt="Kubeflow Pipelines"/>
  <img src="https://img.shields.io/badge/DockerHub-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="DockerHub"/>
</p>

**Summary:** Integrated MLflow for experiment tracking, both locally and with Dagshub. Set up Kubeflow pipelines on a local Minikube cluster, containerized the project with Docker, and managed pipeline runs and deployments through the Kubeflow dashboard.

**Go to mlops_project5_outputs for artifacts**

Step 1
Project setup
1.	Creating virtual Environment in project folder.
2.	Creating required folders and files. (artifacts for outputs, Kubeflow pipeline folder, src where main project code lies, (static , templates for html,css,js and flask automatically finds them in project directory), utils for common functions, requirements and setup file. To make a folder a package we need to create a __init__.py file inside it so that the methods/files can be accessed from other places.
3.	Next, we code for setup, custom exceptions, logger, requirements files (basic things at first like numpy, pandas) .
4.	Then we run setup.py in venv in cmd using pip install -e . This will install all the required dependencies for the project make the project directory ready for next steps. This step automatically created a folder with project name given in the setup.py
Step 2
1.	After jupyter notebook testing we start with Data processing.
2.	Create data_processing.py, code it and test. You should see the artifacts in the project directory.
3.	Now model_training.py in src, code it and test. Should see the model.pkl in the artifacts.
Step 3
Experiment tracking using Mlflow, Dagahub
1.	Make code changes for mlflow in model_training.py
2.	And run the file. You will see mlruns in the root. Now run mlflow ui. You get the url. Go into it and you see there whatever you logged in model_training.py
3.	Now this is local. But to do it online we use Dagshub.
4.	Go to dagshub and sigin. Now create a repo.
5.	Now create a repo in github and push the code.
6.	Now from dagshub, connect with github .
7.	Now select the specific github repo to connect with dagshub.
8.	 After connecting, go to remote -Experiments-copy the MLflow tracking remote url. And now you set some variales
9.	Set MLFLOW_TRACKING_URI=paste url  here
10.	set MLFLOW_TRACKING_USERNAME=you can see in dagshub in profile
11.	Now for pwd, in dagshub go to top right – settings- token-generate token-give some name- generate- now this token is your pwd for below 
12.	set MLFLOW_TRACKING_PASSWORD=
13.	 Now run all the above 3 in venv.
14.	And run the model_training.py. should give you url for experiment tracking. Go to it and see the experiment and metrics.
15.	Push changes to github.
Step 4
App using Flask and ChatGPT
1.	Code index.html, style.css and application.py.
2.	Now Run the application.py. This will give you the url to test the app.
Step 5
Kubeflow and Minicube setup
You do this setup in pwsh not in project venv
1.	We are now doing local setup of Kubeflow pipelines.
2.	First, we need docker desktop on pc.
3.	Make sure it is running in background all time.
4.	And make sure Kubernetes engine is not running. You can check this in settings.
5.	Now install minikube (local kubernetes engine) for your machine and install. In power shell , minikube version for check if the installation is successful.
6.	Now start minikube in pwsh with minikube start
7.	Creates a docker container in the pc with some specification (like cpu’s, memory).
8.	Now check minikube status. Its should show running. You can also check in docker. You will see there too.
9.	Now kubectl(command line interface for Kubernetes) download and install.
10.	Install using chocolatey, so we first install this in pwsh using the command
11.	Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
12.	 Now follow the cmds in the Kubectl page to install kubectl.
13.	Src: https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
14.	choco install kubernetes-cli
15.	Now check with kubectl version 
16.	Now search for Kubernetes local deployment and go to official site and scroll down to docker desktop.
17.	Having installed Docker-Desktop, you create a Kubernetes cluster on Docker-Desktop.
18.	Src: https://www.kubeflow.org/docs/components/pipelines/legacy-v1/installation/localcluster-deployment/#k3s-on-windows-subsystem-for-linux-wsl
19.	We are doing all these because , we are configuring the infra by ourselves. In case of cloud deployment, it is already done for us by the cloud provider.
20.	Run the cmds given in there.
21.	Now our minikube cluster is running successfully.
22.	Now deploying the Kubeflow pipelines. In the same page , run the 4 cmds in pwsh one by one.
23.	After running cmds go to cmd and run Kubectl get pod -A (run this in cmd not pwsh).
24.	It should show all running. Note: Takes some time (30min depends on network and pc).
25.	Now go to the same page copy a cmd to run in pwsh to Verify that the Kubeflow Pipelines UI is accessible by port-forwarding.
26.	kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
27.	Now goto localhost:8080
28.	You will see now Kubeflow dashboard.
29.	Make sure don’t close the pwsh terminal.
Step 6
Building Kubeflow Pipeline
1.	So first we need to create docker file and training pipeline
2.	After coding the docker file. We push to dockerhub, because docker images can only be managed in dockerhub.
3.	Now in venv run docker build -t give_name .
4.	Now you run after building by running docker run name
5.	You will see the url. Go to it. If it’snt running don’t worry. Our main motto is to push to dockerhub and run there.
6.	Now we need to connect with dockerhub. So run docker login
7.	Login in the dialog box. Login
8.	In your vevn you see login succeded.
9.	Now go to dockerhub in web and login with same credentials.
10.	Now you tag the image to dockerhub by running docker tag name username/name:latest  The user name is from docker hub and name is your image name.
11.	Now you push the image by running docker push username/name:latest
12.	Wait until it gets pushed.
13.	Now go to dockerhub and refresh. You see the image pushed under repository. 
14.	Now we need to build the Kubeflow pipeline. So, create a .py file in Kubeflow pipeline folder and code it.
15.	After running this file, one .yaml file is created in root automatically.
16.	Now go to the pipelines in Kubeflow dashboard , make sure it is running in localhost:8080.
17.	There go to upload pipeline on top right – give name- description- upload the yaml file created just before- create.
18.	Now you see the pipeline there.
19.	Now go to create run on top right – leave the default values- Start.
20.	You can also create a experiment and select that in 19 step so that you can group the runs in to experiment.
21.	Now go to runs, you will see the project running there.
22.	Click on the data preprocessing , go to logs and details for further information about run.
23.	So finally, when you see green ticks on the steps. It’s done.
24.	In summary what we did in this project is we developed a project and dockerised and pushed image to Dockerhub. Then we setup a minikube and Kubeflow and created yaml file, then we uploaded this file in the Kubeflow dashboard and runned.  This run will execute the image. And this image is the main artifact we need to deploy in GKE/Cloud run/Vm etc.
25.	Done

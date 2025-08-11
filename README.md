# Social Media Analysis Tool (Predicto)

The **Social Media Analysis Tool** provides sentiment analysis, topic modeling, and trend prediction using social media data. This application is containerized with Docker to make it easy to run on any system without worrying about dependencies or environment setup.
> **⚠️ NOTE:**
> This project is currently **not runnable** because it was previously dependent on a university-hosted SQL server that is no longer accessible.  
> I’m currently **migrating it into Docker** and making **major improvements** to its architecture and features. Once complete, it will be runnable again on any system without special setup.



---

## Steps to Run the Application

### Prerequisites

Before running the application, ensure you have the following installed:

1. **Git**: [Download Git](https://git-scm.com/downloads)
2. **Docker**: [Download Docker](https://www.docker.com/products/docker-desktop)

---

### Instructions

Follow these steps to clone, build, and run the application:

1. **Clone the Repository**:
   Open a terminal and clone the repository to your local machine:
   ```
   git clone https://github.com/MohamedTababi-GitH/Social-Media-Analysis-Tool-Predicto.git
   cd Social-Media-Analysis-Tool-Predicto
   
   **add API keys in predicto_app.py line 33, 642. 

2. **Build the Docker Image: Use the Dockerfile to build the Docker image**:
   docker build -t social-media-analysis-tool .

3. **Run the Docker Container: Once the image is built, run the application inside a container**:
   docker run -it --rm -p 5000:5000 social-media-analysis-tool

4. **Access the Application**:
   Open a browser and navigate to http://localhost:5000 to access the app.

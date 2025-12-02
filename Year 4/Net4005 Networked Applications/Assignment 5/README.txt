# Assignment 5 NET4005

**Description**

Running docker containers using flask to generate a website that informs the user where they are connecting from

**Requirements**
- Python with Flask library installed
- Docker

**Getting Started**

***Executing program***

Running:

To run the docker container, a person must build the image first using the following command:
    -docker image build -t {assignment} .

After that to run the container, use the following command
    -docker run -p 8080:8080 {assignment}

Once all that is done, links should appear to the website

**NB**
**A html file is not generated as a for every instance,
"return f"<h1>You are connecting from {ip_addr}</h1>"" creates a new html file.**

## Contributors
Xindong Lin
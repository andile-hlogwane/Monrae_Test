Instructions

#clone the git repo:
git clone https://github.com/andile-hlogwane/Monrae_Test.git

#cd to the repo directory:
cd Monrae_Test

#build docker image:
docker build -t sentiment_analysis:1 .

#ochestrate and spin up docker containers:
docker-compose up

visit the following url:http://localhost:8000/api/schema/redoc/   
#wait until page loads, might take time (for the first time) due to the torch package

use any apidev and testing tool and send json request using the following format
{
    "user_input": ["good on you","get in there"]   #add more inputs if desired
}

or 

visit http://localhost:8000/api/schema/swagger-ui/ # to test api using swagger ui

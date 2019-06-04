# Headless-Chrome-Screenshots

Use Headless Chrome in AWS Lambda to take screenshots of webpages

### Binaries
There's two files here from other projects: 

chromedriver comes from http://chromedriver.chromium.org/

headless-chromium came from https://github.com/adieuadieu/serverless-chrome/releases

It's important to make sure you've got compatible versions of these two files. The versions currently in the repo are chromedriver 2.37 and headless-chromium 64 (from serverless-chrome release 37).

### Python Packages
This project requires the selenium package from PyPI. It's in the requirements.txt file. Install it like this:

`$ pip install -r requirements.txt -t .`

### Packaging for Lambda
`$ zip -r -9 lambda.zip lambda_function.py headless-chromium chromedriver selenium/ urllib3/`

Upload the lambda.zip file to your function.

### API Gateway
This Lambda function is meant to go along with an API Gateway endpoint. Once you've got the lambda function in place, add in an API Gateway trigger.

Because we're going to be returning images, be sure to allow binary media types. Enter `*/*` for this field.

### Url Parameters
The function implements these url parameters:
 
 url - Which page to load. Use the full url including the protocol (http or https) and urlencode any special characters.
  
  - Good: `https%3A%2F%2Fgoogle.com`
  
  - Bad: `https://google.com`
 
 res - The resolution of the screenshot. Defaults to 800 x 600.
 
 wait - Integer seconds to wait for the page to load before taking the screenshot. Defaults to 1.
 
 eg.
 `?url=https%3A%2F%2Fgoogle.com&res=1000x800&wait=2`
 
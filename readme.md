# Download From Github and Push To Amazon S3.

## The scripts in this repository are for a lambda function that downloads contents from S3 and moves them into S3. THe contents of this repository can be zipped and uploaded to a Lambda function. To see the use case of this Lambda and how to set up such a pipeline, view this [document](https://github.com/Pajkouisn/Website/blob/master/readme.md). 

## The code is well commented so is easy to understand.

## Usage
To prepare a package for Lambda deployment, run the following script.
```
	sh package.sh
```

This will create a zip that can be uploaded to S3 or sdeployed directly as a lambda function.
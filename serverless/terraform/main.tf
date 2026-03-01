provider "aws" {
  region = "eu-north-1"
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_lambda_function" "division_lambda" {
  function_name = "division-serverless"
  role          = aws_iam_role.lambda_role.arn
  handler       = "handler.handler"
  runtime       = "nodejs18.x"

  filename         = "${path.module}/function.zip"
  source_code_hash = filebase64sha256("${path.module}/function.zip")
}
FROM public.ecr.aws/lambda/python:3.8

COPY . .

# RUN pip install -r requirements.txt
# caching https://stackoverflow.com/a/57282479
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN python3 -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2');"
RUN pip cache purge

CMD [ "lambda_function.lambda_handler" ] 
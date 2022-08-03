FROM public.ecr.aws/lambda/python:3.8
COPY . .

# to make it faster to local image building I added the whl & model files, no need to download everytime
# RUN pip install -r requirements.txt
# caching https://stackoverflow.com/a/57282479
COPY torch-1.12.0-cp38-cp38-manylinux1_x86_64.whl . 
RUN pip install torch-1.12.0-cp38-cp38-manylinux1_x86_64.whl
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
# RUN python3 -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('model');"
RUN rm -rf torch-1.12.0-cp38-cp38-manylinux1_x86_64.whl
RUN pip cache purge

CMD [ "lambda_function.lambda_handler" ] 
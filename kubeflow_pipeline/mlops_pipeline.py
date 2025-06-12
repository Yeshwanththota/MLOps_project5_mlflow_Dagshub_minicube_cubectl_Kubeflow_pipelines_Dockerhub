import kfp
from kfp import dsl

def data_processing_op():
    return dsl.ContainerOp(
        name='Data Processing',
        image='yeshwanththota33/mlopsproject:latest',
        command=['python', 'src/data_processing.py'],)
def model_training_op():
    return dsl.ContainerOp(
        name='Model Training',
        image='yeshwanththota33/mlopsproject:latest',
        command=['python', 'src/model_training.py'],)

@dsl.pipeline(
    name='MLOps Pipeline',
    description='A MLOps pipeline for data processing and model training.'
)

def mlops_pipeline():
    data_processing = data_processing_op()
    model_training = model_training_op().after(data_processing)

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(mlops_pipeline, 'mlops_pipeline.yaml')
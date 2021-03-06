# Traffic

Write an AI to identify which traffic sign appears in a photograph.

    $ python traffic.py gtsrb
    Epoch 1/10
    500/500 [==============================] - 5s 9ms/step - loss: 3.7139 - accuracy: 0.1545
    Epoch 2/10
    500/500 [==============================] - 6s 11ms/step - loss: 2.0086 - accuracy: 0.4082
    Epoch 3/10
    500/500 [==============================] - 6s 12ms/step - loss: 1.3055 - accuracy: 0.5917
    Epoch 4/10
    500/500 [==============================] - 5s 11ms/step - loss: 0.9181 - accuracy: 0.7171
    Epoch 5/10
    500/500 [==============================] - 7s 13ms/step - loss: 0.6560 - accuracy: 0.7974
    Epoch 6/10
    500/500 [==============================] - 9s 18ms/step - loss: 0.5078 - accuracy: 0.8470
    Epoch 7/10
    500/500 [==============================] - 9s 18ms/step - loss: 0.4216 - accuracy: 0.8754
    Epoch 8/10
    500/500 [==============================] - 10s 20ms/step - loss: 0.3526 - accuracy: 0.8946
    Epoch 9/10
    500/500 [==============================] - 10s 21ms/step - loss: 0.3016 - accuracy: 0.9086
    Epoch 10/10
    500/500 [==============================] - 10s 20ms/step - loss: 0.2497 - accuracy: 0.9256
    333/333 - 5s - loss: 0.1616 - accuracy: 0.9535

### The problem solving approch:

The problem was solved using OpenCV to load images and Convolutional neural network for modelling the data.

A short video demonstrating my implementation of this project can be found [here](https://youtu.be/CsAt3N04TYk)

### Specification

Specification for this project can be found [here](https://cs50.harvard.edu/ai/2020/projects/5/traffic/#specification)


## Installation processes:

    step 1 - pip install tensorflow 
    -------> Not worked! DLL load failed, ....
    step 2 - conda install tensorflow 
    -------> Not worked! tensorflow was not compatible with python 3.8
    step 3 - conda create --name py37 python=3.7
            source activate py37
            conda install tensorflow
    -------> Finally worked
    step 4 - conda install opencv
    -------> Not worked! not available from conda standard packages
    step 5 - conda install -c conda-forge opencv
    -------> Worked
    step 6 - conda install scikit-learn
    -------> Worked

## Not working Experimentation processes:

    Convolutional layers : one, with 32 3x3 filters
    Pooling layers : one, Max pooling, 2x2
    Hidden layers : one, 128
    Dropout : 50%
    ----> Not Worked!
    ----> Accuracy was very low 0.06, epoch time was high 30s

    
    -> Replace Hidden layers : one, 128 with two, 43
    -> Replace Convolutional Filters : 10 3x3 filters in place of 32
    Convolutional layers : one, with 10 3x3 filters
    Pooling layers : one, Max pooling, 2x2
    Hidden layers : two, 43
    Dropout : 50%
    ----> Not Worked!
    ----> Accuracy was very low 0.06, epoch time was high 14s


    -> Replace Hidden layers : two, 20 in place of two, 43
    Convolutional layers : one, with 10 3x3 filters
    Pooling layers : one, Max pooling, 2x2
    Hidden layers : two, 20
    Dropout : 50%
    ----> Not Worked!
    ----> Accuracy was very low 0.06, epoch time was high 27s


    -> Replace Convolutional Filters : 100 10x10 filters in place of 10 3x3
    Convolutional layers : one, with 100 10x10 filters
    Pooling layers : one, Max pooling, 2x2
    Hidden layers : two, 20
    Dropout : 50%
    ----> Not Worked!
    ----> Accuracy was very low 0.06, epoch time was high 2:27s


    -> Replace Convolutional Filters : 5 10x10 filters in place of 100 10x10
    Convolutional layers : one, with 5 10x10 filters
    Pooling layers : one, Max pooling, 2x2
    Hidden layers : two, 20
    Dropout : 50%
    ----> Not Worked!
    ----> Accuracy was very low 0.06, epoch time was high 27s


    -> Replace Hidden layers : one, 10 in place of two, 20
    Convolutional layers : one, with 5 10x10 filters
    Pooling layers : one, Max pooling, 2x2
    Hidden layers : one, 10
    Dropout : 50%
    ----> Not Worked!
    ----> Accuracy was very low 0.06, epoch time was high 31s

    

## Working Experimentation processes:

    -> Replace Hidden layers : one, 128 in place of one, 10
    -> Replace Convolutional Filters : 20 3x3 filters in place of 5 10x10
    -> Replace Pooling layers : one, Max pooling, 10x10 in place of one, Max pooling, 2x2
    Convolutional layers : one, with 5 10x10 filters
    Pooling layers : one, Max pooling, 10x10
    Hidden layers : one, 128
    Dropout : 50%
    ----> Worked!
    ----> Accuracy increased significantly after 10 epoch! from 0.1149 to 0.4422 , epoch time was 14s


    -> Replace Convolutional Filters : 40 3x3 filters in place of 20 10x10
    Convolutional layers : one, with 40 3x3 filters
    Pooling layers : one, Max pooling, 10x10
    Hidden layers : one, 128
    Dropout : 50%
    ----> Worked!
    ----> Accuracy slightly increased after 10 epoch! from 0.0999 to 0.4785 , epoch time was higher 25s


    -> Replace Convolutional Filters : 10 3x3 filters in place of 40 10x10
    -> add Pooling layers : one, Max pooling, 2x2 in place of one, Max pooling, 10x10
    -> add Convolutional Filters : 10 3x3 filters
    -> add Pooling layers : one, Max pooling, 10x10
    Convolutional layers : one, with 10 3x3 filters
    Pooling layers : one, Max pooling, 2x2
    Convolutional layers : one, with 10 3x3 filters
    Pooling layers : one, Max pooling, 10x10
    Hidden layers : one, 128
    Dropout : 50%
    ----> Not Worked!
    ----> Accuracy decreased after 10 epoch! from 0.079 to 0.2495 , epoch time was 18s


    -> Replace Convolutional Filters : 20 3x3 filters in place of 10 10x10
    -> Replace Pooling layers : one, Max pooling, 10x10 in place of one, Max pooling, 2x2
    -> delete Convolutional Filters : 10 3x3 filters
    -> delete Pooling layers : one, Max pooling, 10x10
    -> decrease dropout to 10%
    Convolutional layers : one, with 20 3x3 filters
    Pooling layers : one, Max pooling, 10x10
    Hidden layers : one, 128
    Dropout : 10%
    ----> Worked!
    ----> Accuracy significantly increased after 10 epoch! from 0.16 to 0.73 , epoch time was 13s
    ----> since accuracy in validation was 0.7495, 10% dropout was not a bad idae and the model generalization was good.


    -> Replace Pooling layers : one, Max pooling, 2x2 in place of one, Max pooling, 10x10
    -> decrease dropout to 5%
    Convolutional layers : one, with 20 3x3 filters
    Pooling layers : one, Max pooling, 2x2
    Hidden layers : one, 128
    Dropout : 5%
    ----> Worked!
    ----> Accuracy significantly increased after 10 epoch! from 0.1436 to 0.9190 , epoch time was 28s
    ----> since accuracy in validation was 0.9284, low dropout was not a bad idae, in fact sice the sample size is large (16000), the model generalization is good without dropout


    -> decrease dropout to 1%
    Convolutional layers : one, with 20 3x3 filters
    Pooling layers : one, Max pooling, 2x2
    Hidden layers : one, 128
    Dropout : 1%
    ----> Not Worked!
    ----> Accuracy increased after 10 epoch! from 0.3861 to 0.9715 , epoch time was 28s
    ----> since accuracy in validation was 0.9450; lower than the training accuracy, 1% dropout was not a good idea. the relatively large accuracy in the first epoch is in line with this observation. these observations suqqest overfitting.


#!/usr/bin/env python
"""
:module: Multilayer Perceptron using Theano to calculate tournament win probabilities.
Built on example code from http://deeplearning.net/tutorial/mlp.html.


A multilayer perceptron is a logistic regressor where
instead of feeding the input to the logistic regression you insert a
intermediate layer, called the hidden layer, that has a nonlinear
activation function (usually tanh or sigmoid) . One can use many such
hidden layers making the architecture deep. The tutorial will also tackle
the problem of MNIST digit classification.

.. math::

    f(x) = G( b^{(2)} + W^{(2)}( s( b^{(1)} + W^{(1)} x))),

References:
    - http://deeplearning.net/tutorial/mlp.html
    - textbooks: "Pattern Recognition and Machine Learning" - Christopher M. Bishop, section 5

Theano license:
    Copyright (c) 2009-2013, Theano Development Team All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
    following conditions are met:

    Redistributions of source code must retain the above copyright notice, this list of conditions and the following
    disclaimer.
    Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
    disclaimer in the documentation and/or other materials provided with the distribution.
    Neither the name of Theano nor the names of its contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ''AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT
    NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN
    NO EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
    STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
    EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import os
import sys
import time

import cPickle
import gzip
import numpy
import theano
import theano.tensor as T

import Analysis
import Constants
import Misc

__docformat__ = 'restructedtext en'


class Perceptron(Analysis.BaseClass):
    def __init__(self):
        self.name = "Perceptron"

    def data_available(self, season_id):
        pass

    def train(self, team, season_id):
        pass

    def win_probability(self, team_1, team_2, season_id, daynum=None):
        pass









    ################################################################################
    # MatLab example code below
    # TODO use as reference implementation
    ################################################################################
    """
    %--------------------
    %-----Data Mining Competition
    %-----David Casterton
    %--------------------

    %dataIn=load('Workarea/ClassifyTrain.txt');
    function [u,v,epoch,alpha] = dataMine12(data,u,v,M,alpha,startEpoch,inEpoch,a,b);

    %--------------------
    %-----loading data sets
    %--------------------
    start=clock; tic;
    fprintf(strcat('loading...\n'));
    Y=data(:,1)-1;
    data=data(:,2:702);
    fprintf(strcat('loaded:\tall data\t\t\t\t\t',num2str(toc),'secs\n')); tic;

    train=data(1:(0+a),:);
    trainClass=Y(1:(0+a),1);
    t2=toc;
    fprintf(strcat('loaded:\ttraining set:\t',num2str(a),'\t\t',num2str(toc),'secs\n')); tic;

    test=data(29001:(29000+b),:);
    testClass=Y(29001:(29000+b),1);
    t3=toc;
    fprintf(strcat('loaded:\ttest set:\t\t',num2str(b),'\t\t',num2str(toc),'secs\n')); tic;

    clear data

    %------------------------------
    %-----training
    %------------------------------

    %-----initializations
    tic;
    epoch=startEpoch;
    endEpoch=startEpoch+inEpoch;
    %M; %-----# of neurons
    m=1;%-----# output neurons
    n=701; %-----# of inputs
    if u==0 & v==0
        u=randn(M,n);
        v=randn((M+1),m);
    end
    if (size(u,1)~=M) & (M>size(u,1))
        uOld=u; vOld=v;
        u=randn(M,n);
        v=randn((M+1),m);
        u(1:size(uOld,1),1:size(uOld,2))=uOld;
        v(1:size(vOld,1),1:size(vOld,2))=vOld;
    end
    if (size(u,1)~=M) & (M<size(u,1))
        uOld=u; vOld=v;
        clear u; clear v;
        u=[uOld(1:M,:)];
        v=[vOld(1:M+1,:)];
    end
    MSEtot=0;
    MSEave(inEpoch,1)=0;
    correct=ones(a,1)-1;
    trainClassConv(a,m)=0;
    fprintf(strcat('initializations done:\t\t\t\t',num2str(toc),'secs\n'));

    %-----training loop
    while epoch<endEpoch,
        if mod(epoch,round(1/M*800))==0 & epoch>1
            alpha=alpha*.98;
            fprintf(strcat('\t\t--alpha:',num2str(alpha,3),'--\n'));
        end
        tic
        for k=1:a
            Z=[1,tanh(train(k,:)*u')];
            Yprime=(Z*v);

            %-----update weights
            v=v+2*alpha*(Y(k,1)-Yprime(1,m))*Z(1,:)';
            u=u+2*alpha*(Y(k,1)-Yprime(1,m))*v(2:M+1,1).*((1-(Z(1,2:M+1)).^2)')*train(k,:);
        end
        epoch=epoch+1;

        %-----calc % correct
        if mod(epoch,round(1/M*150))==0
            for k=1:a
                Z=[1,tanh(train(k,:)*u')];
                Yprime=(Z*v);
                    if Yprime>=.5
                        ans=1;
                    else
                        ans=0;
                    end
                    if ans==trainClass(k,1)
                        correct(k,1)=1; %marked 1 whenever correct
                    end
            end
            correctAveTrain(1,epoch)=sum(correct(:,1))/size(correct(:,1),1)*100;
            fprintf(strcat('\t-----train correct:',num2str(correctAveTrain(1,size(correctAveTrain,2)),3),'%%-----\n'));
        elseif epoch<(startEpoch+(mod(startEpoch, round(1/M*150))))
            correctAveTrain(1,epoch)=0;
        else
            correctAveTrain(1,epoch)=correctAveTrain(1,epoch-1);
        end

        if (mod(epoch,round(1/M*800))==0)
            eval(strcat('save saveFile', num2str(correctAveTrain(1,size(correctAveTrain,2)),3),'a-',num2str(M),'n-',num2str(epoch),'e',' epoch alpha u v'));
            fprintf(strcat('\t\t--file saved--\n'));
        end
        %-----terminal printout
        fprintf(strcat('Epoch:',num2str(epoch),'.\t',num2str(endEpoch-epoch),'remaining.\tepoch time:',num2str(toc,2),'secs.\t',num2str((toc/60)*(endEpoch-epoch),2),'mins remaining\n'))
    end

    %------------------------------
    %-----TEST set calc's
    %------------------------------
        correct(b,1)=0;
        clear Yprime;
        for k=1:b
            Z=[1,tanh(u*test(k,:)')'];
            Yprime(k,:)=(Z*v);
            if Yprime>=.5
                ans=1;
            else
                ans=0;
            end
            if ans==testClass(k,1)
                correct(k,1)=1; %marked 1 whenever correct
            end
        end
        correctAve=sum(correct(:,1))/size(correct(:,1),1)*100;

    %------------------------------
    %-----text output
    %------------------------------

    %-----final terminal printout
    fprintf(strcat('\ntotal epochs: ',num2str(endEpoch),'\tneurons: ',num2str(M),'\talpha:',num2str(alpha)));
    total=clock-start;
    finish=clock;
    if total(1,5)
        fprintf(strcat('\ntotal time:\t',num2str(total(1,5)),':',num2str(finish(1,6)+(60-start(1,6)),2),'mins.\ttrain %%:',num2str(correctAveTrain(1,size(correctAveTrain,2)),3),'\ttest %%:',num2str(correctAve,3),'\n'));
    else
        fprintf(strcat('\ntotal time:\t',num2str(total(1,6),2),'secs.\ttrain %%:',num2str(correctAveTrain(1,size(correctAveTrain,2)),3),'\ttest %%:',num2str(correctAve,3),'\n'));
    end

    %------------------------------
    %-----graphical output
    %------------------------------

    %-----%ave correct plot
    figure
    plot(startEpoch+1:(startEpoch+inEpoch),correctAveTrain(1,startEpoch+1:(startEpoch+inEpoch)))
    title(strcat('test set correct: ',num2str(correctAve,3),'%   train set correct:',num2str(correctAveTrain(1,size(correctAveTrain,2)),3),'%'));
    legend('train set')
    """


    ################################################################################
    # Theano example code below
    # TODO adapt into framework
    ################################################################################

    class HiddenLayer(object):
        def __init__(self, rng, input, n_in, n_out, W=None, b=None,
                     activation=T.tanh):
            """
            Typical hidden layer of a MLP: units are fully-connected and have
            sigmoidal activation function. Weight matrix W is of shape (n_in,n_out)
            and the bias vector b is of shape (n_out,).

            NOTE : The nonlinearity used here is tanh

            Hidden unit activation is given by: tanh(dot(input,W) + b)

            :type rng: numpy.random.RandomState
            :param rng: a random number generator used to initialize weights

            :type input: theano.tensor.dmatrix
            :param input: a symbolic tensor of shape (n_examples, n_in)

            :type n_in: int
            :param n_in: dimensionality of input

            :type n_out: int
            :param n_out: number of hidden units

            :type activation: theano.Op or function
            :param activation: Non linearity to be applied in the hidden
                               layer
            """
            self.input = input

            # `W` is initialized with `W_values` which is uniformely sampled
            # from sqrt(-6./(n_in+n_hidden)) and sqrt(6./(n_in+n_hidden))
            # for tanh activation function
            # the output of uniform if converted using asarray to dtype
            # theano.config.floatX so that the code is runable on GPU
            # Note : optimal initialization of weights is dependent on the
            #        activation function used (among other things).
            #        For example, results presented in [Xavier10] suggest that you
            #        should use 4 times larger initial weights for sigmoid
            #        compared to tanh
            #        We have no info for other function, so we use the same as
            #        tanh.
            if W is None:
                W_values = numpy.asarray(rng.uniform(
                        low=-numpy.sqrt(6. / (n_in + n_out)),
                        high=numpy.sqrt(6. / (n_in + n_out)),
                        size=(n_in, n_out)), dtype=theano.config.floatX)
                if activation == theano.tensor.nnet.sigmoid:
                    W_values *= 4

                W = theano.shared(value=W_values, name='W', borrow=True)

            if b is None:
                b_values = numpy.zeros((n_out,), dtype=theano.config.floatX)
                b = theano.shared(value=b_values, name='b', borrow=True)

            self.W = W
            self.b = b

            lin_output = T.dot(input, self.W) + self.b
            self.output = (lin_output if activation is None
                           else activation(lin_output))
            # parameters of the model
            self.params = [self.W, self.b]


    class MLP(object):
        """Multi-Layer Perceptron Class

        A multilayer perceptron is a feedforward artificial neural network model
        that has one layer or more of hidden units and nonlinear activations.
        Intermediate layers usually have as activation function tanh or the
        sigmoid function (defined here by a ``HiddenLayer`` class)  while the
        top layer is a softamx layer (defined here by a ``LogisticRegression``
        class).
        """

        def __init__(self, rng, input, n_in, n_hidden, n_out):
            """Initialize the parameters for the multilayer perceptron

            :type rng: numpy.random.RandomState
            :param rng: a random number generator used to initialize weights

            :type input: theano.tensor.TensorType
            :param input: symbolic variable that describes the input of the
            architecture (one minibatch)

            :type n_in: int
            :param n_in: number of input units, the dimension of the space in
            which the datapoints lie

            :type n_hidden: int
            :param n_hidden: number of hidden units

            :type n_out: int
            :param n_out: number of output units, the dimension of the space in
            which the labels lie

            """

            # Since we are dealing with a one hidden layer MLP, this will translate
            # into a HiddenLayer with a tanh activation function connected to the
            # LogisticRegression layer; the activation function can be replaced by
            # sigmoid or any other nonlinear function
            self.hiddenLayer = HiddenLayer(rng=rng, input=input,
                                           n_in=n_in, n_out=n_hidden,
                                           activation=T.tanh)

            # The logistic regression layer gets as input the hidden units
            # of the hidden layer
            self.logRegressionLayer = LogisticRegression(
                input=self.hiddenLayer.output,
                n_in=n_hidden,
                n_out=n_out)

            # L1 norm ; one regularization option is to enforce L1 norm to
            # be small
            self.L1 = abs(self.hiddenLayer.W).sum() \
                    + abs(self.logRegressionLayer.W).sum()

            # square of L2 norm ; one regularization option is to enforce
            # square of L2 norm to be small
            self.L2_sqr = (self.hiddenLayer.W ** 2).sum() \
                        + (self.logRegressionLayer.W ** 2).sum()

            # negative log likelihood of the MLP is given by the negative
            # log likelihood of the output of the model, computed in the
            # logistic regression layer
            self.negative_log_likelihood = self.logRegressionLayer.negative_log_likelihood
            # same holds for the function computing the number of errors
            self.errors = self.logRegressionLayer.errors

            # the parameters of the model are the parameters of the two layer it is
            # made out of
            self.params = self.hiddenLayer.params + self.logRegressionLayer.params


    def test_mlp(learning_rate=0.01, L1_reg=0.00, L2_reg=0.0001, n_epochs=1000,
                 dataset='mnist.pkl.gz', batch_size=20, n_hidden=500):
        """
        Demonstrate stochastic gradient descent optimization for a multilayer
        perceptron

        This is demonstrated on MNIST.

        :type learning_rate: float
        :param learning_rate: learning rate used (factor for the stochastic
        gradient

        :type L1_reg: float
        :param L1_reg: L1-norm's weight when added to the cost (see
        regularization)

        :type L2_reg: float
        :param L2_reg: L2-norm's weight when added to the cost (see
        regularization)

        :type n_epochs: int
        :param n_epochs: maximal number of epochs to run the optimizer

        :type dataset: string
        :param dataset: the path of the MNIST dataset file from
                     http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz


       """
        datasets = load_data(dataset)

        train_set_x, train_set_y = datasets[0]
        valid_set_x, valid_set_y = datasets[1]
        test_set_x, test_set_y = datasets[2]

        # compute number of minibatches for training, validation and testing
        n_train_batches = train_set_x.get_value(borrow=True).shape[0] / batch_size
        n_valid_batches = valid_set_x.get_value(borrow=True).shape[0] / batch_size
        n_test_batches = test_set_x.get_value(borrow=True).shape[0] / batch_size

        ######################
        # BUILD ACTUAL MODEL #
        ######################
        print '... building the model'

        # allocate symbolic variables for the data
        index = T.lscalar()  # index to a [mini]batch
        x = T.matrix('x')  # the data is presented as rasterized images
        y = T.ivector('y')  # the labels are presented as 1D vector of
                            # [int] labels

        rng = numpy.random.RandomState(1234)

        # construct the MLP class
        classifier = MLP(rng=rng, input=x, n_in=28 * 28,
                         n_hidden=n_hidden, n_out=10)

        # the cost we minimize during training is the negative log likelihood of
        # the model plus the regularization terms (L1 and L2); cost is expressed
        # here symbolically
        cost = classifier.negative_log_likelihood(y) \
             + L1_reg * classifier.L1 \
             + L2_reg * classifier.L2_sqr

        # compiling a Theano function that computes the mistakes that are made
        # by the model on a minibatch
        test_model = theano.function(inputs=[index],
                outputs=classifier.errors(y),
                givens={
                    x: test_set_x[index * batch_size:(index + 1) * batch_size],
                    y: test_set_y[index * batch_size:(index + 1) * batch_size]})

        validate_model = theano.function(inputs=[index],
                outputs=classifier.errors(y),
                givens={
                    x: valid_set_x[index * batch_size:(index + 1) * batch_size],
                    y: valid_set_y[index * batch_size:(index + 1) * batch_size]})

        # compute the gradient of cost with respect to theta (sotred in params)
        # the resulting gradients will be stored in a list gparams
        gparams = []
        for param in classifier.params:
            gparam = T.grad(cost, param)
            gparams.append(gparam)

        # specify how to update the parameters of the model as a list of
        # (variable, update expression) pairs
        updates = []
        # given two list the zip A = [a1, a2, a3, a4] and B = [b1, b2, b3, b4] of
        # same length, zip generates a list C of same size, where each element
        # is a pair formed from the two lists :
        #    C = [(a1, b1), (a2, b2), (a3, b3), (a4, b4)]
        for param, gparam in zip(classifier.params, gparams):
            updates.append((param, param - learning_rate * gparam))

        # compiling a Theano function `train_model` that returns the cost, but
        # in the same time updates the parameter of the model based on the rules
        # defined in `updates`
        train_model = theano.function(inputs=[index], outputs=cost,
                updates=updates,
                givens={
                    x: train_set_x[index * batch_size:(index + 1) * batch_size],
                    y: train_set_y[index * batch_size:(index + 1) * batch_size]})

        ###############
        # TRAIN MODEL #
        ###############
        print '... training'

        # early-stopping parameters
        patience = 10000  # look as this many examples regardless
        patience_increase = 2  # wait this much longer when a new best is
                               # found
        improvement_threshold = 0.995  # a relative improvement of this much is
                                       # considered significant
        validation_frequency = min(n_train_batches, patience / 2)
                                      # go through this many
                                      # minibatche before checking the network
                                      # on the validation set; in this case we
                                      # check every epoch

        best_params = None
        best_validation_loss = numpy.inf
        best_iter = 0
        test_score = 0.
        start_time = time.clock()

        epoch = 0
        done_looping = False

        while (epoch < n_epochs) and (not done_looping):
            epoch = epoch + 1
            for minibatch_index in xrange(n_train_batches):

                minibatch_avg_cost = train_model(minibatch_index)
                # iteration number
                iter = (epoch - 1) * n_train_batches + minibatch_index

                if (iter + 1) % validation_frequency == 0:
                    # compute zero-one loss on validation set
                    validation_losses = [validate_model(i) for i
                                         in xrange(n_valid_batches)]
                    this_validation_loss = numpy.mean(validation_losses)

                    print('epoch %i, minibatch %i/%i, validation error %f %%' %
                         (epoch, minibatch_index + 1, n_train_batches,
                          this_validation_loss * 100.))

                    # if we got the best validation score until now
                    if this_validation_loss < best_validation_loss:
                        #improve patience if loss improvement is good enough
                        if this_validation_loss < best_validation_loss *  \
                               improvement_threshold:
                            patience = max(patience, iter * patience_increase)

                        best_validation_loss = this_validation_loss
                        best_iter = iter

                        # test it on the test set
                        test_losses = [test_model(i) for i
                                       in xrange(n_test_batches)]
                        test_score = numpy.mean(test_losses)

                        print(('     epoch %i, minibatch %i/%i, test error of '
                               'best model %f %%') %
                              (epoch, minibatch_index + 1, n_train_batches,
                               test_score * 100.))

                if patience <= iter:
                        done_looping = True
                        break

        end_time = time.clock()
        print(('Optimization complete. Best validation score of %f %% '
               'obtained at iteration %i, with test performance %f %%') %
              (best_validation_loss * 100., best_iter + 1, test_score * 100.))
        print >> sys.stderr, ('The code for file ' +
                              os.path.split(__file__)[1] +
                              ' ran for %.2fm' % ((end_time - start_time) / 60.))


    class LogisticRegression(object):
        """Multi-class Logistic Regression Class

        The logistic regression is fully described by a weight matrix :math:`W`
        and bias vector :math:`b`. Classification is done by projecting data
        points onto a set of hyperplanes, the distance to which is used to
        determine a class membership probability.
        """

        def __init__(self, input, n_in, n_out):
            """ Initialize the parameters of the logistic regression

            :type input: theano.tensor.TensorType
            :param input: symbolic variable that describes the input of the
                          architecture (one minibatch)

            :type n_in: int
            :param n_in: number of input units, the dimension of the space in
                         which the datapoints lie

            :type n_out: int
            :param n_out: number of output units, the dimension of the space in
                          which the labels lie

            """

            # initialize with 0 the weights W as a matrix of shape (n_in, n_out)
            self.W = theano.shared(value=numpy.zeros((n_in, n_out),
                                                     dtype=theano.config.floatX),
                                    name='W', borrow=True)
            # initialize the baises b as a vector of n_out 0s
            self.b = theano.shared(value=numpy.zeros((n_out,),
                                                     dtype=theano.config.floatX),
                                   name='b', borrow=True)

            # compute vector of class-membership probabilities in symbolic form
            self.p_y_given_x = T.nnet.softmax(T.dot(input, self.W) + self.b)

            # compute prediction as class whose probability is maximal in
            # symbolic form
            self.y_pred = T.argmax(self.p_y_given_x, axis=1)

            # parameters of the model
            self.params = [self.W, self.b]

        def negative_log_likelihood(self, y):
            """Return the mean of the negative log-likelihood of the prediction
            of this model under a given target distribution.

            .. math::

                \frac{1}{|\mathcal{D}|} \mathcal{L} (\theta=\{W,b\}, \mathcal{D}) =
                \frac{1}{|\mathcal{D}|} \sum_{i=0}^{|\mathcal{D}|} \log(P(Y=y^{(i)}|x^{(i)}, W,b)) \\
                    \ell (\theta=\{W,b\}, \mathcal{D})

            :type y: theano.tensor.TensorType
            :param y: corresponds to a vector that gives for each example the
                      correct label

            Note: we use the mean instead of the sum so that
                  the learning rate is less dependent on the batch size
            """
            # y.shape[0] is (symbolically) the number of rows in y, i.e.,
            # number of examples (call it n) in the minibatch
            # T.arange(y.shape[0]) is a symbolic vector which will contain
            # [0,1,2,... n-1] T.log(self.p_y_given_x) is a matrix of
            # Log-Probabilities (call it LP) with one row per example and
            # one column per class LP[T.arange(y.shape[0]),y] is a vector
            # v containing [LP[0,y[0]], LP[1,y[1]], LP[2,y[2]], ...,
            # LP[n-1,y[n-1]]] and T.mean(LP[T.arange(y.shape[0]),y]) is
            # the mean (across minibatch examples) of the elements in v,
            # i.e., the mean log-likelihood across the minibatch.
            return -T.mean(T.log(self.p_y_given_x)[T.arange(y.shape[0]), y])

        def errors(self, y):
            """Return a float representing the number of errors in the minibatch
            over the total number of examples of the minibatch ; zero one
            loss over the size of the minibatch

            :type y: theano.tensor.TensorType
            :param y: corresponds to a vector that gives for each example the
                      correct label
            """

            # check if y has same dimension of y_pred
            if y.ndim != self.y_pred.ndim:
                raise TypeError('y should have the same shape as self.y_pred',
                    ('y', target.type, 'y_pred', self.y_pred.type))
            # check if y is of the correct datatype
            if y.dtype.startswith('int'):
                # the T.neq operator returns a vector of 0s and 1s, where 1
                # represents a mistake in prediction
                return T.mean(T.neq(self.y_pred, y))
            else:
                raise NotImplementedError()


    def load_data(dataset):
        ''' Loads the dataset

        :type dataset: string
        :param dataset: the path to the dataset (here MNIST)
        '''

        #############
        # LOAD DATA #
        #############

        # Download the MNIST dataset if it is not present
        data_dir, data_file = os.path.split(dataset)
        if data_dir == "" and not os.path.isfile(dataset):
            # Check if dataset is in the data directory.
            new_path = os.path.join(os.path.split(__file__)[0], "..", "data", dataset)
            if os.path.isfile(new_path) or data_file == 'mnist.pkl.gz':
                dataset = new_path

        if (not os.path.isfile(dataset)) and data_file == 'mnist.pkl.gz':
            import urllib
            origin = 'http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz'
            print 'Downloading data from %s' % origin
            urllib.urlretrieve(origin, dataset)

        print '... loading data'

        # Load the dataset
        f = gzip.open(dataset, 'rb')
        train_set, valid_set, test_set = cPickle.load(f)
        f.close()
        #train_set, valid_set, test_set format: tuple(input, target)
        #input is an numpy.ndarray of 2 dimensions (a matrix)
        #witch row's correspond to an example. target is a
        #numpy.ndarray of 1 dimensions (vector)) that have the same length as
        #the number of rows in the input. It should give the target
        #target to the example with the same index in the input.

        def shared_dataset(data_xy, borrow=True):
            """ Function that loads the dataset into shared variables

            The reason we store our dataset in shared variables is to allow
            Theano to copy it into the GPU memory (when code is run on GPU).
            Since copying data into the GPU is slow, copying a minibatch everytime
            is needed (the default behaviour if the data is not in a shared
            variable) would lead to a large decrease in performance.
            """
            data_x, data_y = data_xy
            shared_x = theano.shared(numpy.asarray(data_x,
                                                   dtype=theano.config.floatX),
                                     borrow=borrow)
            shared_y = theano.shared(numpy.asarray(data_y,
                                                   dtype=theano.config.floatX),
                                     borrow=borrow)
            # When storing data on the GPU it has to be stored as floats
            # therefore we will store the labels as ``floatX`` as well
            # (``shared_y`` does exactly that). But during our computations
            # we need them as ints (we use labels as index, and if they are
            # floats it doesn't make sense) therefore instead of returning
            # ``shared_y`` we will have to cast it to int. This little hack
            # lets ous get around this issue
            return shared_x, T.cast(shared_y, 'int32')

        test_set_x, test_set_y = shared_dataset(test_set)
        valid_set_x, valid_set_y = shared_dataset(valid_set)
        train_set_x, train_set_y = shared_dataset(train_set)

        rval = [(train_set_x, train_set_y), (valid_set_x, valid_set_y),
                (test_set_x, test_set_y)]
        return rval
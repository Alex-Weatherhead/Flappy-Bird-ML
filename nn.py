import numpy


activation_function = lambda x: 1/(1 + numpy.exp(-x)) #Sigmoid.

def query (inputs, weights_ih, weights_ho):
    
    input_outs = numpy.array(inputs, ndmin = 2).T
                
    hidden_ins = numpy.dot(weights_ih, input_outs)
    hidden_outs = activation_function(hidden_ins)
                
    output_ins = numpy.dot(weights_ho, hidden_outs)
    output_outs = activation_function(output_ins)

    return output_outs.argmax()
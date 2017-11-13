import numpy
from random import random, randint

input_neurons = 2
hidden_neurons = 5
output_neurons = 2

def initialize (population):
    
    ih_weights = [None] * population
    ho_weights = [None] * population

    for j in range(population):

        ih_weights[j] = (numpy.random.rand(hidden_neurons, input_neurons) - 0.5)
        ho_weights[j] = (numpy.random.rand(output_neurons, hidden_neurons) - 0.5)

    return (ih_weights, ho_weights)

def train (population, weights, scores):

    ih_weights, ho_weights = weights

    rankings = scores.argsort()

    x = int(population * 0.30)                      # 30% of the population (i.e. x = 3 if population = 10).
    y = int(population * 0.20)                      # 20% of the population (i.e. x = 2 if population = 10).

    unfit = rankings[:population - x]               # Unfit population initially includes all but the top 30% of the population.
    numpy.random.shuffle(unfit)             # The unfit population is then shuffled.
   
    fit = numpy.append(rankings[population - x:], unfit[:y])     # Fit population includes top 30% of the population + 20% of the unfit population (random because of the shuffling).
    unfit = unfit[y:]                               # Unfit population now includes the other 80% of the initial unfit population.
    
    d = numpy.array([scores[f] for f in fit])       # distribution of scores across fit population.
    p = d / numpy.sum(d)                            # probability distribution across fit population.
 
 
    for u in unfit:
        
        i, j = numpy.random.choice(fit, 2, replace=False, p=p)          # select two members of the fit population on which to perform crossover.
        
        parents = zip(
            numpy.append(ih_weights[i].reshape(hidden_neurons * input_neurons), ho_weights[i].reshape(output_neurons * hidden_neurons)),
            numpy.append(ih_weights[j].reshape(hidden_neurons * input_neurons), ho_weights[j].reshape(output_neurons * hidden_neurons))
        )

        child = crossover(parents)
        
        if random() < 0.80:     # Arbitrary percentage threshold.
            mutate(child)

        ih_weights[u] = child[:hidden_neurons * input_neurons].reshape(hidden_neurons, input_neurons)
        ho_weights[u] = child[output_neurons * hidden_neurons:].reshape(output_neurons, hidden_neurons)

def crossover (parents):

    child = numpy.array([numpy.random.choice(gene) for gene in parents])

    return child

def mutate (child):

    gene = randint(0, len(child) - 1)
    
    child[gene] += round((random() - 0.50), 2)

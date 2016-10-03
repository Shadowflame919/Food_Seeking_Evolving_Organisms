"""

    Brain layers:
      Input - Only holds input values and outputs with weights for next layer
      Hidden - Recieves, Processes and outputs data with weight for next layer
      Output - Revieves, Processes and outputs data with NO weights

      Layers contain neurons
      Neurons contains a weight for each neuron in the next layer


    [
      [ [0,0,0] , [0,0,0] ],
      [ [0] , [0] , [0] ],
      [ [] ],
    ]
    
    
"""

import math
import random


class Neural_Network:
    def __init__(self, structure=None):
        #print("Initiating Network with structure of " + str(structure))
        self.layers = []
        
        if structure != None:
            for layer in range(len(structure)):
                #print("Creating layer " + str(layer))
                self.layers.append([])
                for neuron in range(structure[layer]):  # add the amount of neurons given by structure
                    self.layers[layer].append([])
                #print("Added " + str(len(self.layers[layer])) + " neurons to layer")
                if layer != len(structure)-1:   # if not an output layer, add bias and give neurons weights
                    self.layers[layer].append([])
                    #print("Layer " + str(layer) + " is not output, bias was added")
                    for neuron in self.layers[layer]:
                        for lengthOfNextLayer in range(structure[layer+1]):
                            neuron.append((random.random()-0.5)*2)

    def giveOutput(self, brainInput):
        layerOutput = brainInput    # layer outputs for input layer
        layerOutput.append(1)  # add bias neurons input to the inputs layers output
        #print("\nInputs for input layer was set to " + str(layerOutput))

        for layer in range(1, len(self.layers)): # for each layer
            #print("\n\nGetting outputs for Layer " + str(layer))
            newOutput = []  # what the current outputs for this layer will be
            neuronAmount = len(self.layers[layer])    # amount of neurons that must produce an output value
            if layer != len(self.layers)-1:
                neuronAmount -= 1
            for neuron in range(neuronAmount): # for each neuron in this layer
                #print("\nGetting output for neuron " + str(neuron))
                inputSum = 0
                for feedNeuron in range(len(self.layers[layer-1])): # for each neuron in the previous layer
                    #print("Adding input from neuron " + str(feedNeuron) + ", layer " + str(layer-1) + "...")
                    #print("The input from this neuron was " + str(round(layerOutput[feedNeuron],2)) + " x " + str(round(self.layers[layer-1][feedNeuron][neuron],2)) + " = " + str(round(layerOutput[feedNeuron] * self.layers[layer-1][feedNeuron][neuron],2)))
                    inputSum += layerOutput[feedNeuron] * self.layers[layer-1][feedNeuron][neuron]  # add up the input the neuron is giving
                #print("The sum of all inputs from this neuron is " + str(round(inputSum,2)))
                inputSum = math.tanh(inputSum)  # Apply Activation Function
                #print("After tanh(), the neuron was given an output value of " + str(round(inputSum,2)))
                newOutput.append(inputSum)  # add this neurons output to the output list for this layer
                
            if layer != len(self.layers)-1: # add next layers bias neuron output which will be 1
                newOutput.append(1)
            layerOutput = newOutput
            #print("\nLayer " + str(layer) + "'s outputs were set to " + str(layerOutput))
            
        return layerOutput

    def childBrain(self):
        #print("Creating child brain")
        mutateRate = 0.2
        childNetwork = Neural_Network()
        childLayers = childNetwork.layers
        for layer in self.layers:
            childLayers.append([])
            for neuron in layer:
                childLayers[-1].append([])
                for weight in neuron:
                    newWeight = 0
                    if random.random() > 0.1:
                        newWeight = weight + (random.random()-0.5) * mutateRate
                        if newWeight > 2:
                            newWeight = 2
                        elif newWeight < -2:
                            newWeight = -2
                    else:
                        newWeight = (random.random()-0.5) * 4
                    childLayers[-1][-1].append(newWeight)

        # Add/Remove extra neurons to hidden layers
        for i in range(1, len(self.layers)-1):
            if random.random() < 0.2:   # Add neuron to layer
                #print("Adding neuron to layer " + str(i))
                #print("Layer was " + str(self.layers[i]))
                self.layers[i].insert(-1, [])
                #print("Layer is now " + str(self.layers[i]))
                #print("Previous layer was " + str(self.layers[i-1]))
                for prevNeuron in self.layers[i-1]:
                    prevNeuron.append((random.random()-0.5))
                #print("Previous layer now is " + str(self.layers[i-1]))
                #print("Neuron needs " + str(len(self.layers[i+1])-1) + " weights connecting to next layer")
                for nextNum in range(len(self.layers[i+1])-1):
                    self.layers[i][-2].append((random.random()-0.5))
                if i+1 == len(self.layers)-1: # If next layer is the last layer
                    self.layers[i][-2].append((random.random()-0.5))
                    
            if len(self.layers[i]) > 2 and random.random() < 0.2:   # Remove neuron from layer
                neuronNum = random.randrange(len(self.layers[i])-1)
                self.layers[i].pop(neuronNum)
                for prevNeuron in self.layers[i-1]:
                    prevNeuron.pop(neuronNum)
                
        return childNetwork
        
































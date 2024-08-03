package main

import (
	"fmt"
	"math/rand"
	"time"
)

type Network struct {
	sizes   []int
	layers  int
	biases  [][]float64
	weights [][][]float64
}

func newNetwork(sizes []int) *Network {
	n := Network{sizes, len(sizes), generateBiases(sizes), generateWeights(sizes)}
	return &n
}

func generateBiases(sizes []int) [][]float64 {
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	sizeSplice := sizes[1:]

	arrSize := len(sizeSplice)
	biases := make([][]float64, arrSize)

	for i := 0; i < arrSize; i++ {
		biases[i] = make([]float64, sizeSplice[i])
		for j := 0; j < sizeSplice[i]; j++ {
			biases[i][j] = r.NormFloat64()
		}
	}

	return biases
}

func generateWeights(sizes []int) [][][]float64 {
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	arrSize := len(sizes) - 1

	inputNodes := sizes[:arrSize]
	outputNodes := sizes[1:]

	weights := make([][][]float64, arrSize)

	for i := 0; i < arrSize; i++ {
		weights[i] = make([][]float64, outputNodes[i])
		for j := 0; j < outputNodes[i]; j++ {
			weights[i][j] = make([]float64, inputNodes[i])
			for k := 0; k < inputNodes[i]; k++ {
				weights[i][j][k] = r.NormFloat64()
			}
		}
	}

	return weights
}

func (network Network) printWeights() {
	fmt.Println("Printing Weights...")

	weights := network.weights
	for i := 0; i < len(weights); i++ {
		fmt.Println(weights[i])
		fmt.Println()
	}
	fmt.Println()
}

func (network Network) printBiases() {
	fmt.Println("Printing Biases...")

	biases := network.biases
	for i := 0; i < len(biases); i++ {
		fmt.Println(biases[i])
	}
	fmt.Println()
}

func feedForward(inputVector, biases []float64, weights [][]float64) (zs []float64, outputActivation []float64) {
	if len(inputVector) != len(weights) && len(inputVector) != len(biases) {
		return make([]float64, len(biases)), make([]float64, len(biases))
	}

	for i := 0; i < len(biases); i++ {
		zs[i] = 0
		for j := 0; j < len(biases); j++ {
			zs[i] += weights[i][j] * inputVector[j]
		}
		zs[i] += biases[i]
		outputActivation[i] = SigmoidElementwise(zs[i])
	}

	return zs, outputActivation
}

func backprop(inputVector []float64, numLayers int, biases [][]float64, weights [][][]float64) []float64 {
	output := make([]float64, len(inputVector))

	// 1. Feedforward

	inputVectors := make([][]float64, numLayers)
	zs := make([][]float64, numLayers)
	for i := 0; i < numLayers; i++ {
		zs[i], inputVectors[i] = feedForward(inputVector, biases[i], weights[i])
	}

	// 2. Compute error of last layer

	// 3. Backpropogate the error of the previous layers

	// 4. Output the gradient

	return output
}

//func SGD()

func main() {
	sizes := []int{3, 1, 3}
	network := newNetwork(sizes)

	network.printWeights()
	network.printBiases()

	//fmt.Print(feedForward([]float64{1, 2, 3}, network.biases, network.weights))
}

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

type VectorArray struct {
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

	nodes := sizes[1:]
	paths := sizes[:arrSize]

	weights := make([][][]float64, arrSize)

	for i := 0; i < arrSize; i++ {
		weights[i] = make([][]float64, nodes[i])
		for j := 0; j < nodes[i]; j++ {
			weights[i][j] = make([]float64, paths[i])
			for k := 0; k < paths[i]; k++ {
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

func feedForward(inputVector []float64, biases [][]float64, weights [][][]float64) []float64 {
	for i := 0; i < len(biases); i++ {
		addVector := MatrixVectorMult(weights[i], inputVector)
		inputVector = Sigmoid(VectorAdd(addVector, biases[i]))
	}

	return inputVector
}

//func SGD()

func main() {
	sizes := []int{2, 3, 1}
	network := newNetwork(sizes)

	network.printWeights()
	network.printBiases()
}

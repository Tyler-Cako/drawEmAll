package main

import (
	"math"
)

func Sigmoid(inputVector []float64) []float64 {
	outputVector := make([]float64, len(inputVector))

	for i := 0; i <= len(inputVector); i++ {
		outputVector[i] = (1 / (1 + math.Exp(inputVector[i])))
	}

	return outputVector
}

func SigmoidElementwise(inputValue float64) float64 {
	return (1 / (1 + math.Exp(inputValue)))
}

func SigmoidPrime(inputVector []float64) []float64 {
	outputVector := make([]float64, len(inputVector))

	for i := 0; i <= len(inputVector); i++ {
		zi := (1 / (1 + math.Exp(inputVector[i])))
		outputVector[i] = zi * (1 - zi)
	}

	return outputVector
}

func CostDerivative(outputActivations, desiredOutput []float64) []float64 {
	outputVector := make([]float64, len(outputActivations))

	for i := 0; i < len(outputActivations); i++ {
		outputVector[i] = outputActivations[i] - desiredOutput[i]
	}

	return outputVector
}

func ArrMax(arr []int) int {
	temp := 0

	for i := 0; i < len(arr); i++ {
		if arr[i] > temp {
			temp = arr[i]
		}
	}

	return temp
}

func MaxInt(num1, num2 int) int {
	if num1 >= num2 {
		return num1
	} else {
		return num2
	}
}

func DotProduct(v1, v2 []float64) float64 {
	if len(v1) != len(v2) {
		return -1
	}

	output := float64(0)
	for i := 0; i < len(v1); i++ {
		output += v1[i] * v2[i]
	}

	return output
}

func VectorAdd(v1, v2 []float64) []float64 {
	if len(v1) != len(v2) {
		return make([]float64, len(v1))
	}

	output := make([]float64, len(v1))

	if len(v1) != len(v2) {
		return output
	}

	for i := 0; i < len(v1); i++ {
		output[i] = v1[i] + v2[i]
	}

	return output
}

func MatrixVectorMult(m [][]float64, v []float64) []float64 {
	if len(v) != len(m) {
		return make([]float64, len(v))
	}

	output := make([]float64, len(v))

	for i := 0; i < len(v); i++ {
		for j := 0; j < len(m[i]); j++ {
			output[i] += m[i][j] * v[j]
		}
	}

	return output
}

func HadamardProduct(v1, v2 []float64) []float64 {
	output := make([]float64, len(v1))
	for i := 0; i < len(v1); i++ {
		output[i] = v1[i] * v2[i]
	}
	return output
}

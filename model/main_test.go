package main

import "testing"

func TestGenerateBiases(t *testing.T) {
	sizes := []int{3, 1, 3}
	expectedVectorLengths := []int{1, 3}

	output := generateBiases(sizes)

	for i := 0; i < len(output); i++ {
		vector := output[i]

		if len(vector) != expectedVectorLengths[i] {
			t.Errorf("len(output) = %d. Output vector: %f not equal to expected length: %d", len(output), vector, expectedVectorLengths[i])
		}

		for j := 0; j < len(vector); j++ {
			if vector[j] == 0 {
				t.Errorf("Output vector[%d] doesn't contain a random value", j)
			}
		}
	}
}

func TestGenerateWeights(t *testing.T) {
	sizes := []int{3, 1, 3}
	expectedMatrixSizes := [3][2]int{
		{1, 3},
		{3, 1},
	}

	output := generateWeights(sizes)

	for i := 0; i < len(sizes)-1; i++ {
		matrix := output[i]
		if len(matrix) != expectedMatrixSizes[i][0] {
			t.Errorf("Output # of cols of output matrix: %d different than expected: %d", len(matrix), expectedMatrixSizes[i][1])
		}
		if len(matrix[0]) != expectedMatrixSizes[i][1] {
			t.Errorf("Output # of rows of output matrix: %d different than expected: %d", len(matrix[0]), expectedMatrixSizes[i][0])
		}
	}

}

// func TestFeedForward(t *testing.T) {
// 	input := []float64{1, 2, 3}
// 	biases := []float64{1, 1, 1}
// 	weights := [][][]float64{
// 		{
// 			{0.6, -0.5, 1.1},
// 		},
// 		{
// 			{.4}, {.9}, {1.1},
// 		},
// 	}

// 	output := feedForward(input, biases, weights)

// 	for i := 0; i < len(output); i++ {

// 	}
// }

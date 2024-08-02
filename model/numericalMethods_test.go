package main

import "testing"

type sizesArr struct {
	sizes    []int
	expected int
}

var arrTests = []sizesArr{
	sizesArr{[]int{1, 2, 4, 3, 2}, 4},
	sizesArr{[]int{9, 2, 4, 3, 2}, 9},
	sizesArr{[]int{1, 2, 4, 3, 8}, 8},
}

func TestArrMax(t *testing.T) {
	for _, test := range arrTests {
		output := ArrMax(test.sizes)
		if output != test.expected {
			t.Errorf("Output max %q not equal to expected max %q", output, test.expected)
		}
	}
}

func TestDotProduct(t *testing.T) {
	v1 := []float64{1, 2, 3, 4}
	v2 := []float64{4, 3, 2, 1}

	output := DotProduct(v1, v2)

	if output != float64(20) {
		t.Errorf("Output dot product %f not equal to expected dot product %f", output, float64(20))
	}
}

func TestVectorAdd(t *testing.T) {
	v1 := []float64{2, 3, 3, 2}
	v2 := []float64{9, 5, 2, 7}

	output := VectorAdd(v1, v2)

	expected := []float64{11, 8, 5, 9}

	for i := 0; i < len(expected); i++ {
		if output[i] != expected[i] {
			t.Errorf("Output[%d] = %f not equal to Expected[%d] = %f", i, output[i], i, expected[i])
		}
	}
}

func TestMatrixVectorMult(t *testing.T) {
	m := [][]float64{
		{1, 2, 3, 4},
		{4, 3, 2, 1},
		{3, 2, 2, 3},
		{2, 3, 3, 2},
	}
	v := []float64{1, 2, 3, 4}
	expected := []float64{30, 20, 25, 25}
	output := MatrixVectorMult(m, v)

	for i := 0; i < len(expected); i++ {
		if output[i] != expected[i] {
			t.Errorf("Output[%d] = %f not equal to Expected[%d] = %f", i, output[i], i, expected[i])
		}
	}
}

func TestSigmoid(t *testing.T) {

}

package main

import ("fmt"
"strconv"
"time")


func sum(a int, b int) string{
	return strconv.Itoa(a + b)
}

func checkBenchMark(n int){
	start := time.Now()
	var s[]int
	for i := 0; i < n; i++{
		s = append(s, i)
	}
	fmt.Println("Total time was taken  ", time.Since(start))
}

func checkBenchMark2(n int){
	start := time.Now()
	// Create the array using the the make function
	s := make([]int, 0, 10)
	for i := 0; i < n; i++{
		s = append(s, i)
	}
	fmt.Println("Total time was taken  ", time.Since(start))
}


func main(){
	var a = 10
	var b = 121212
	fmt.Println(sum(a,b))
	// For loop 
	for i :=0 ; i < 10; i++{
		fmt.Printf("Hello word %d is\n",i)
	}

	// Switch Statement
	var i = 2
	switch i{
	case 1:
		fmt.Printf("Hi this is one")
	case 2:
		fmt.Printf("This is two")
	default:
		fmt.Printf("Here this is three")
	}

	// array
	c := []int{}
	fmt.Println("This is array", c)
	c = append(c,1)
	fmt.Println("This is array", c)

	// Loop in array
	for index, value := range c{
		fmt.Printf("value %d is %d \n", index, value)
	}
	// Loop in array another way
	for i :=0 ; i < len(c) ; i++{
		fmt.Printf("hi this is %d \n", c[i])
	}
	// check the make and empty bench mark
	checkBenchMark(100000000)
	checkBenchMark2(100000000)

	// map in go
	data_map := make(map[string]int)
	data_map["j"] = 1
	data_map["i"] = 1
	fmt.Println("data value", data_map)
	fmt.Println("data value", data_map["i"])
	fmt.Println("data value", data_map["L"])

	//

}


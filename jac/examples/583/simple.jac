"""
A simple Jac program to calculate the sum and product of two numbers.
"""

glob NUM1 = 10, NUM2 = 20;

can calculate_sum(a: int, b: int) -> int {
    return a + b;
}

# Function to calculate the product of two numbers
can calculate_product(a: int, b: int) -> int {
    #* This function multiplies two integers.
       The result is returned as an integer. *#
    return a * b;
}

# Main entry point
with entry {

    sum_result = calculate_sum(NUM1, NUM2);
    product_result = calculate_product(NUM1, NUM2);

    print(f"The sum of {NUM1} and {NUM2} is: {sum_result}");
    print(f"The product of {NUM1} and {NUM2} is: {product_result}");
}


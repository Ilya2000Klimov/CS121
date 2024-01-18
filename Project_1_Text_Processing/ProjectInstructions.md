Here's the converted Markdown version of your HTML code:

---

This assignment is to be done individually. You cannot use code written by your classmates. Use code found over the Internet at your own peril -- it may not do exactly what the assignment requests. If you do end up using code you find on the Internet, you must disclose the origin of the code. **Concealing the origin of a piece of code is plagiarism**. Use Ed Discussion for general questions whose answers can benefit you and everyone.

**General Specifications**

1. You are required to use python (preferable python 3.8.x or newer) The next homework will use crawlers written in Python, so you may want to use this homework to brush up your knowledge of Python.
2. Make sure to break down your program into classes/methods/functions corresponding to the parts in this specification. They will be tested separately.
3. The function signatures in this specification are informal; their purpose is to explain the inputs and outputs of the methods.
4. At points, the assignment may be under-specified. In those cases, make your own assumptions and be prepared to defend them.
5. The input files for both parts will be UTF-8 encoded.
6. Do not print any extra lines (e.g. debug lines, headers, names of the input files, etc) other than what you can see in the examples in the output as it will result in the tests failing and you losing credit.
7. External libraries are not to be used for this part (Also you can't use regex for this assignment)
8. The TA will use their own text files. Note that some of the text files may be VERY LARGE
9. Commands for running will be as follows:
   - python PartA.py [filename] for Part A
   - python PartB.py [filename 1] [filename 2] for Part B

**Part A: Word Frequencies (4 points)**

Write a program that takes a file name as a command line argument, read this text file, tokenize it, count the tokens, and print out the token (word) frequencies. You can use the following methods as an example (you are not required to use these specific methods):

- **Method/Function:** List<Token> tokenize(TextFilePath)  
  Write a method/function that reads in a text file and returns a list of the tokens in that file. For the purposes of this project, a token is a sequence of alphanumeric characters, independent of capitalization (so *Apple*, *applE* and *aPPle* are the same token "apple").

- **Method:** Map<Token,Count> computeWordFrequencies(List<Token>)  
  Write another method/function that counts the number of occurrences of each token in the token list.

- **Method:** void print(Frequencies<Token, Count>)  
  Finally, write a method that prints out the word frequency counts onto the screen. The print out should be ordered by decreasing frequency. (so, highest frequency words first). Resolve ties alphabetically and in ascending order.

Here is an example if input/output:

**Input :**

Here's a fun-fact! White tigers live mostly in "India".

Wild lions mostly live in "Africa".

**Output:**

| Token   | Frequency |
|---------|-----------|
| in      | 2         |
| live    | 2         |
| mostly  | 2         |
| a       | 1         |
| africa  | 1         |
| fact    | 1         |
| fun     | 1         |
| here    | 1         |
| india   | 1         |
| lions   | 1         |
| s       | 1         |
| tigers  | 1         |
| white   | 1         |
| wild    | 1         |

Each line of the output should use "[token]\t[frequency]" formatting where you need to replace [token] with the token name and [frequency] with the token frequency. For example, if you have two tokens: hello with frequency 1 and world with frequency 2, the output should be:

world\t2  
hello\t1

Note that "\t" will be changed to a tab (couple of spaces) when printed on the console.

**Part B: Intersection of two files (6 points)**

Write a program that takes two text files as command line arguments and outputs the number of tokens they have in common. Here is an example of input/output:

**Input file 1:**

We reviewed **the trip** and credited **the cancellation fee**. **The driver has** been notified.

**Input file 2:**

If a **trip** is cancelled more than 5 times after **the driver**-partner **has** confirmed **the** request, a **cancellation fee** will apply.

**Output:**

6

You can reuse code you wrote for part A.

**Common Tasks**

For both part A and part B, please add a brief runtime complexity explanation for your code as a comment on top of each method or function (does it run in linear time relative to the size of the input? Polynomial time? Exponential time? ). **This explanation and your code's actual conformance with this explanation will be the basis for evaluating the performance of your program.**

**You should get the file names from command line arguments.** Do not hard code the input file names in your code or read them from system standard input (stdin). As the assignment will be graded using an automatic grader, not doing this will result in losing the whole credit for the assignment.

**Exception handling is required for bad inputs.** An example of bad input would be a character in a non-english language. Your code should be able to tokenize the whole input file even though there may be some bad inputs in it. You should be able to skip the bad input and continue with the rest. If your code throws an exception in the middle of tokenizing a TA's input test case, you will lose the whole credit for that test case.

**Submitting Your Assignment**

Your submission should be a single zip file containing two programs, one for part A, the other for part B. Something like this:

Assignment1.zip  
------------ PartA.py  
------------ PartB.py

Submit it to Canvas.

You can replace Assignment1 with whatever name you think is appropriate. You don't need to add your UCInetID or student number to the zip file name. Canvas will do that automatically when we are downloading your assignments. Do not zip the directory containing these two files! So the following examples are **not** a correct structure:

Assignment1.zip  
------------ Assignment 1  
------------------------ PartA.py  
------------------------ PartB.py

Assignment1.zip  
------------ PartA  
------------------------ PartA.py  
------------ PartB  
------------------------ PartB.py

This is necessary as the automatic grader can only work with this structure. Again, please pay attention that you only need to upload **ONE** zip file containing two python files at shown above and not one zip file for each part.

**Grading Process**

The correctness of your programs will be evaluated against a set of test cases using an automated grader. If necessary the results will be reviewed by a TA or Reader as well. Then, your source code will be evaluated by a TA or Reader for Understand-ability and Performance.

**Evaluation Criteria**

Your assignment will be graded on the following four criteria.

1

. Correctness (40%)
   - How well does the behavior of the program match the specification?
   - How does your program handle bad input?

2. Understanding (30%)
   - Do you demonstrate understanding of the code?

3. Efficiency (30%)
   - How quickly does the program work on large inputs? Besides the sorting part in Part A, only linear time complexity for both parts gets the full credit.

---
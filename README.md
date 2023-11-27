# URL Summarization Project

URL Summarization Project is an application designed to fetch text content from web pages and provide a concise summarization using Evadb and AI models. The tool is perfect for users seeking to quickly grasp the essence of lengthy web documents.

**Application Link**: [GitHub - URL Summarization Project](https://github.com/Pb314314/EvaDB_project)

## Implementation Details

This project leverages Evadb for web content summarization. Users input a URL, and the software generates a concise summary of the content found on that web page.

### Steps:

1. **User URL Input**: Users enter the URL of the webpage they wish to summarize. The application utilizes ReportLab and Beautiful Soup (bs4) to fetch and parse the web page text and subsequently creates a PDF.
2. **Merge Paragraphs and Create PDF**: The paragraphs are merged to ensure each contains more than 300 words. This approach reduces the total number of paragraphs while ensuring each has sufficient content for effective summarization.
3. **Load PDF to Evadb, Load Model, and Summarize**: The generated PDF is loaded into Evadb. A summarization model (`facebook/bart-large-cnn`) is then used to create concise summaries of the content.
4. **Merge and Output the Obtained Summarization**: The summarization results are merged into a single string, and both the length and content are outputted.

## Sample Input

**URL**: "https://buzzdb-docs.readthedocs.io/part1/lab1.html"

This webpage is part of a CS6422 lab and contains a substantial amount of text, making it ideal for testing the summarization capabilities of the project.

## Sample Output

**Evadb Output**:

```text
This assignment is to help you brush up your C++programming skills, and exercise your skills in Data Structure and Algorithm Design. In this assignment,you are to develop a word locator program written in C++, which will allow a user to check if a specified(re)occurrence of a specified query word appears in the input text file. The locate command is case insensitive, i.e. to match the word in the locate command with a word in a load file you should use a case-insensitive string comparison method. The syntax of the locatecommand is "locate". The parameter will have a whitespace before and after it, and should be an integer greater than 0. If an incorrectload command is entered, such as "load" then your data structure should not be reset. For example ra#s and rats! are invalid word parameters. All the command keywords are case insensitive, so "LoCATe sing 2" is a valid command,and should be treated as "locate sing 2". The following is a sample run: Sample Run > load data/sample.txt >locate song 1 3 > locate Song 1 3. locate pie 1 18 > locate pie 2. locate SoNg 1 3 and locate pie 18. locate bird 1 18 and bird 2 18. Find the bird and the pie. Your main design task is to pick atree-based data structure that allows efficient execution of the locate command. The memory footprint of your program should not exceed fourtimes the size of the input load file, when measured in bytes. You can usethe command ps -l to check the program size. The handout contains the skeleton code and the test files. Your program must be written only in C++. Each file should start with a header describing the purpose of the file and should alsocontain your name, GT UserID, and GT email address. The large data file wrnpc.txt is hidden and is evaluated only when submitted to the Gradescope. You will be submitting your assignment on Gradescope. You are expected to run submit.sh and submit the generated zip to theautograder. Report.md to describe the following design and program criteria (optional) Incase you don't complete all the testcases, we will award you partial points based on the report. What is the complexity of your implementation of the locate command in terms of the number of words in the file that you are querying? For the complexity, we are only interested in the big-O analysis. The maximum score on this assignment is 100. If you get 100 on the autograder thatis your score. If a report has a. score less than 100 we will award partial points based on the report. If a report. score more than 100, we will give partial points to the team that scored the most points. If the report has. a score of 100 or less we will offer partial points for the team with the highest score.
```

**Total Word Count**: 478 words

## References

- [EvaDB Documentation](https://evadb.readthedocs.io/en/latest/source/usecases/text-summarization.html#ai-query-using-registered-functions)
- [Hugging Face Summarization](https://huggingface.co/docs/transformers/tasks/summarization)


# EECS E6893 Big Data Analytics HW0

> Lijie Huang, UNI: lh3158
Sep 14, 2022
> 

## 1. Warm-up Exercises

### (1) Provide screenshots to prove you’ve completed the exercises

Exercise 3 Pi Calculation:

![截屏2022-09-13 18.49.49.png](EECS%20E6893%20Big%20Data%20Analytics%20HW0%201f71be9019a649599a91a12aedf9c024/%25E6%2588%25AA%25E5%25B1%258F2022-09-13_18.49.49.png)

Exercise 4 Word Count Job:

![截屏2022-09-13 20.54.16.png](EECS%20E6893%20Big%20Data%20Analytics%20HW0%201f71be9019a649599a91a12aedf9c024/%25E6%2588%25AA%25E5%25B1%258F2022-09-13_20.54.16.png)

### (2) List the Spark transformations and actions involved in each exercise. Identify the RDD operation that triggers the program to execute.

- Pi Calculation Job:
    
    ![Untitled](EECS%20E6893%20Big%20Data%20Analytics%20HW0%201f71be9019a649599a91a12aedf9c024/Untitled.png)
    
    On line 32, a RDD is created by parallelizing the data randomly generated. From line 32 to line 36, a transformation “map” and an action “reduce” are processed to count how many points are inside the circle, whose radius is 1. Finally, Pi can be estimated by calculating the probability.
    
- Word Count Job:
    
    ![Untitled](EECS%20E6893%20Big%20Data%20Analytics%20HW0%201f71be9019a649599a91a12aedf9c024/Untitled%201.png)
    
    On line 13, a RDD is created from the text file by function “textFile”. on line 14 and 15, 3 transformations “flatMap”, “map” and “reduceByKey” are processed to count the frequency of each word. On line 16, an action (”saveAsTextFile”) is used to save the count result.
    

## 2. NYC Bike Expert

### (1) How many stations with longitude between -73.94 and -74.04?

698

![Untitled](EECS%20E6893%20Big%20Data%20Analytics%20HW0%201f71be9019a649599a91a12aedf9c024/Untitled%202.png)

### (2) What’s the total number of bikes available in region_id 71?

11885

![HW0-2-2.png](EECS%20E6893%20Big%20Data%20Analytics%20HW0%201f71be9019a649599a91a12aedf9c024/HW0-2-2.png)

### (3) What’s the largest capacity for a station? List all the station_id of the stations that have the largest capacity.

largest capacity: 79

![HW0-2-3-1.png](EECS%20E6893%20Big%20Data%20Analytics%20HW0%201f71be9019a649599a91a12aedf9c024/HW0-2-3-1.png)

stations with the largest capacity:

![HW0-2-3-2.png](EECS%20E6893%20Big%20Data%20Analytics%20HW0%201f71be9019a649599a91a12aedf9c024/HW0-2-3-2.png)

## 3. Understanding William Shakespeare

### (1) Find top-10 frequent words without any text preprocessing.

```bash
[(the,620),(and,427),(of,396),(to,367),(I,326),(a,256),(you,193),(in,190),(is,185),(my,170)]
```

![截屏2022-09-14 22.43.38.png](EECS%20E6893%20Big%20Data%20Analytics%20HW0%201f71be9019a649599a91a12aedf9c024/%25E6%2588%25AA%25E5%25B1%258F2022-09-14_22.43.38.png)

### (2) Find top-10 frequent words by first filtering out stop words provides by NLTK packages.

```bash
[(Macb.,137),(haue,114),(Enter,73),(thou,61),(Macd.,58),(shall,47),(vpon,47),(thy,46),(yet,45),(thee,43)]
```

![截屏2022-09-14 22.44.31.png](EECS%20E6893%20Big%20Data%20Analytics%20HW0%201f71be9019a649599a91a12aedf9c024/%25E6%2588%25AA%25E5%25B1%258F2022-09-14_22.44.31.png)
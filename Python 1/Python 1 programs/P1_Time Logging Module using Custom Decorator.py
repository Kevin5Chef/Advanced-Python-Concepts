import time
print("SY-5, Kevin Victor, Roll No.-30")
def log_exec(func):
    def wrapper(*args,**kwargs):
        start=time.perf_counter()
        result=func(*args,**kwargs)
        end=time.perf_counter()

        elapsed_us=(end-start)*1_000_000

        print(f"The function named - '{func.__name__}' took {elapsed_us:.2f} microseconds to execute.")
        return result
    return wrapper

@log_exec
def add():
    a=2
    b=3
    print("\nSum = ",a+b)

#Function call
add()
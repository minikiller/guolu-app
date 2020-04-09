
import multiprocessing
import mqtt_client
def add_employee(emp, emp_list=None):
    if emp_list is None:
        emp_list = []
    emp_list.append(emp)

# def main():
    # multiprocessing.freeze_support()
p = multiprocessing.Process(target=mqtt_client.main)
p.start()
p.join()
# if __name__ == "__main__":
#     main()
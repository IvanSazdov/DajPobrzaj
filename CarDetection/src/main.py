from StreamProcessing import StreamProcessing
from multiprocessing import Process
from Areas import AREAS
import SendingService
from CarsDto import Car
from datetime import datetime

def process_stream(area, name, file):
    stream_process = StreamProcessing(name, area, file)
    stream_process.Process()


def main():
    # processes = [
    #     Process(target=process_stream, args=(details["coordinates"], name, details["file"]))
    #     for name, details in AREAS.items()
    # ]
    # for process in processes:
    #     process.start()
    while True:
        car = Car(datetime.now(),"Bogorodica",6)
        SendingService.SendCarsData(car)

    # cars = SendingService.GetCarsData()



if __name__ == "__main__":
    main()

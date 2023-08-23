from StreamProcessing import StreamProcessing
from multiprocessing import Process

AREAS = {
    "Bogorodica": {
        "coordinates": [(581, 298), (345, 448), (1618, 456), (1581, 303)],
        "file": "media/premin_bogorodica.mp4"
    },
    "Blace": {
        "coordinates": [(499, 341), (241, 539), (1446, 557), (1240, 325)],
        "file": "media/premin_blace.mp4"
    },
    "Tabanovce": {
        "coordinates": [(510, 392), (350, 436), (565, 479), (660, 431)],
        "file": "media/premin_tabanovce.mp4"
    }
}


def process_stream(area, name, file):
    stream_process = StreamProcessing(name, area, file)
    stream_process.Process()


def main():
    processes = [
        Process(target=process_stream, args=(details["coordinates"], name, details["file"]))
        for name, details in AREAS.items()
    ]

    for process in processes:
        process.start()


if __name__ == "__main__":
    main()

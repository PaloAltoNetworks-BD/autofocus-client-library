import multiprocessing
import time
from autofocus import AFSample


def search_hash(hash):

    print("Searching for {}".format(hash))

    query = {
        "operator": "all",
        "children": [
            {
                "field": "sample.sha256",
                "operator": "is",
                "value": None  # Will be filled with a hash
            }
        ]
    }

    query['children'][0]['value'] = hash

    for sample in AFSample.search(query):
        print(f"sha256:{sample.sha256} md5:{sample.md5} m:{sample.malware} b:{sample.benign} g:{sample.grayware}")
        break

    return None


if __name__ == "__main__":

    hashes_to_find = [
        "bfbba86bca5bd25e7f9a561f91466a305d7c2429657f0bad9ab488cae8bb8765",
        "3d9509e0d2c25446e65d256d4a753796f171fa66c0f37d679e1d01dd50c1e63b",
        "333eedb63e1725c22294db6cf906e19eb2099fdb12efcfba8906975fe3701cc5",
        "aae06d9ebd13f628b3f8487fda7228f742ac3b4e8aad37c996f2430e65285922",
        "d3adc13e9cd761d679841753b7c1b70910bfff963a9e886b24a48b573d62d37b",
        "0724db773abebce839d47ced3abb808dedf342c079799b00c8def9bcf759e704",
        "20ece7473ad124a59f9d908acd2cb7c13d44b0fee018d14e0fe3803fad9a20fc",
        "95ff746c61ad95c03853aa517e73feb102c35217743047c6ba5d97f471a992a4",
        "c9ff55a317efe202985c68fc76e7941a6a9c2a097662b71b53e285974e765acb",
        "09a00975673d2f59ab8ac44c47f2d1fa7bae1cf5153a503ee9b6a63a2345bcae"
    ]
    workers = []
    max_workers = 4

    while True:

        new_workers = []

        # Clean up workers
        for worker in workers:
            if worker.is_alive():
                new_workers.append(worker)

        workers = new_workers

        # Is there work to be done? If not, we're done
        if not hashes_to_find:
            break

        # Start workers
        while True:

            # Start the work if there is work and we have free workers
            if hashes_to_find and len(workers) < max_workers:
                v = hashes_to_find.pop()
                workers.append(multiprocessing.Process(target=search_hash, args=(v,)))
                workers[-1].start()
            else:
                break

        # Rest
        print("Sleeping, to be nice")
        time.sleep(.5)

    print("Already done!")

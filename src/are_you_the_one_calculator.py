import os
import ayto_server
import ayto_client
if __name__ == "__main__":
    cache_folder = "./cache"
    logs_folder = "./logs"

    try:
        os.mkdir(cache_folder)
    except OSError:
        print ("Creation of the directory %s failed" % cache_folder)
        
    try:
        os.mkdir(logs_folder)
    except OSError:
        print ("Creation of the directory %s failed" % logs_folder)

    input_value = None
    while True:
        input_value = input("Start as server[s] or client[c]    exit[e]: ")
        if input_value == "s":
            s = ayto_server.ayto_server()
            
        elif input_value == "c":
            c = ayto_client.ayto_client()

        elif input_value == "e":
            break
            


            
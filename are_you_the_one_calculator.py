import ayto_server
import ayto_client
if __name__ == "__main__":
    input_value = None
    while True:
        input_value = input("Start as server[s] or client[c]    exit[e]: ")
        if input_value == "s":
            s = ayto_server.ayto_server()
            
        elif input_value == "c":
            c = ayto_client.ayto_client()

        elif input_value == "e":
            break
            


            
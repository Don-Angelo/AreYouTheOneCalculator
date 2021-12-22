import ayto_server
import ayto_client
import matching_night_simulation
if __name__ == "__main__":
    input_value = None
    while True:
        input_value = input("Start as server[s], client[c] or matching night simulation[m]: ")
        if input_value == "s":
            s = ayto_server.ayto_server()
            
        elif input_value == "c":
            c = ayto_client.ayto_client()
            
        elif input_value == "m":
            m = matching_night_simulation


            
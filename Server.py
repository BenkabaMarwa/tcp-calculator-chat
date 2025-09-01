import socket
import pyttsx3
from colorama import Fore, Style

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if "english" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    server_socket.settimeout(30)

    print("Server is listening on port 12345...")
    speak("Server is listening on port 12345")

    try:
        conn, addr = server_socket.accept()
        print(Fore.GREEN + f"Connection established with {addr}" + Style.RESET_ALL)
        speak("Connection established with client")
    except socket.timeout:
        print(Fore.RED + "No client connected within the timeout period." + Style.RESET_ALL)
        speak("No client connected, server shutting down.")
        server_socket.close()
        return

    try:
    # TCP Handshake Simulation
        syn = conn.recv(1024).decode()
        if not syn:
            raise ConnectionResetError

        print(Fore.YELLOW + f"Client: {syn}" + Style.RESET_ALL)
        if syn == "SYN":
            speak("Received SYN from client")
            conn.send("SYN-ACK".encode())
            print(Fore.BLUE + "Server: SYN-ACK" + Style.RESET_ALL)

    
        ack = conn.recv(1024).decode()

        if not ack:
            raise ConnectionResetError

        print(Fore.YELLOW + f"Client: {ack}" + Style.RESET_ALL)
        if ack == "ACK":
            print(Fore.GREEN + "Received ACK from client. Handshake complete." + Style.RESET_ALL)
            speak("Received ACK from client. Handshake complete")

        while True:
            Operation = conn.recv(1024).decode()
            print(Fore.YELLOW + f"Client: the operation is {Operation}" + Style.RESET_ALL) 
            speak(f"Received the operation from client, the operation is {Operation}")

            conn.send("Send two numbers".encode())
            print(Fore.BLUE + "Server: Send Two numbers" + Style.RESET_ALL)
        
            frNumber = conn.recv(1024).decode()
            if frNumber.lower() == "exit":
                print(Fore.RED + "Client exited the communication."+ Style.RESET_ALL)
                speak("Client exited the communication.")
                break
            print(Fore.YELLOW + f"Client: the first number is {frNumber}" + Style.RESET_ALL) 
            speak(f"Received the first number from client, the number is {frNumber}")

            scNumber = conn.recv(1024).decode()

            if scNumber.lower() == "exit":
                print(Fore.RED + "Client exited the communication."+ Style.RESET_ALL)
                speak("Client exited the communication.")
                break
        
            print(Fore.YELLOW + f"Client: the second number is {scNumber}" + Style.RESET_ALL)
            speak(f"Received the second number from client, the number is {scNumber}")
        
            try:
                if Operation.lower()=="addition":
                    result = int(frNumber) + int(scNumber)
                elif Operation.lower()=="subtraction":
                    result = int(frNumber) - int(scNumber)
                elif Operation.lower()=="multiplication":
                    result = int(frNumber) * int(scNumber)
                else:
                    result = int(frNumber) / int(scNumber)
                conn.send(str(result).encode())
                print(Fore.BLUE + f"Server: The result is {result}" + Style.RESET_ALL)
            except:
                print(Fore.RED + "Invalid input received." + Style.RESET_ALL)
                speak("Invalid input received")
                conn.send("Error: Invalid input".encode())
    
    except (ConnectionResetError, BrokenPipeError):
        print(Fore.RED + "Client disconnected unexpectedly." + Style.RESET_ALL)
        speak("Client disconnected unexpectedly")

    except socket.error as e:
        print(Fore.RED + f"Socket error: {e}" + Style.RESET_ALL)
        speak("A socket error occurred")

    finally:
        try:
            conn.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        conn.close()
        server_socket.close()
        print(Fore.RED + "Server shut down." + Style.RESET_ALL)
        speak("Server shut down")
    

if __name__ == "__main__":
    server()
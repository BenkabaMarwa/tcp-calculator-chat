import socket
import time
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

def getValidNumber(prompt):
    while True:
        try:
            num = input(prompt)
            if num.lower() == "exit":
                return "exit"
            return str(int(num))
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter an integer." + Style.RESET_ALL)
            speak("Invalid input. Please enter an integer.")


def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(30)

    try:
        client_socket.connect(('localhost', 12345))
    except socket.timeout:
        print(Fore.RED + "Server is not responding. Connection timed out." + Style.RESET_ALL)
        speak("Server is not responding")
        return
    except socket.error as e:
        print(Fore.RED + f"Failed to connect to server: {e}" + Style.RESET_ALL)
        speak("Failed to connect to server")
        return
    
    print(Fore.GREEN + "Connected to server." + Style.RESET_ALL)
    speak("Connected to server")

    try:
        # TCP Handshake Simulation
        client_socket.send("SYN".encode())
        print(Fore.YELLOW + "Client: SYN" + Style.RESET_ALL)
        Ack = client_socket.recv(1024).decode()

        if not Ack:
            raise ConnectionResetError

        print(Fore.BLUE + f"Server: {Ack}" + Style.RESET_ALL)
        if Ack == "SYN-ACK":
            speak("Received SYN-ACK from server")
            client_socket.send("ACK".encode())
            print(Fore.YELLOW + "Client: ACK" + Style.RESET_ALL)
            time.sleep(1)
    
        while True:
            speak("Enter the operation (addition, subtraction, multiplication, or division..)")
            while True:
                Operation= input("Enter the opperation (addition, subtraction, multiplication, or division)..")
                valid_operations = ["addition", "subtraction", "multiplication", "division"]
                if Operation in valid_operations:
                    break
                else:
                    print(Fore.RED + f"Please enter correct operation (addition, subtraction, multiplication, or division..)"+ Style.RESET_ALL)
                    speak(f"Please enter correct operation (addition, subtraction, multiplication, or division..)")

            client_socket.send(Operation.encode())
            print(Fore.YELLOW + f"Client: The operation is {Operation}"+ Style.RESET_ALL)
         
            message = client_socket.recv(1024).decode()

            if not message:
                raise ConnectionResetError

            print(Fore.BLUE + f"Server: {message}"+ Style.RESET_ALL)
            speak(f"Received message from server {message}")
        
            speak("Enter the first number or type exit to quit")

            num1 = getValidNumber("Enter the first number (or type 'exit' to quit)..")

            client_socket.send(num1.encode())
            if num1.lower() == "exit":
                speak("exit")
                print(Fore.RED + "exit" + Style.RESET_ALL)
                break

            print(Fore.YELLOW + f"Client: the first number is {num1}" + Style.RESET_ALL)
            time.sleep(1)

            speak("Enter the second number or type exit to quit")
        
            num2 = getValidNumber("Enter the second number (or type 'exit' to quit)..")

            while True:
                if Operation.lower()=="division" and num2=="0":
                    print(Fore.RED + "We can't divide by zero" + Style.RESET_ALL)
                    speak("We can't divide by zero")
                    speak("Enter the second number different from zero (or type 'exit' to quit)")
                    num2 = getValidNumber("Enter the second number different from zero '0'(or type 'exit' to quit)..")               
                else:
                    break

            client_socket.send(num2.encode())
            if num2.lower() == "exit":
                speak("exit")
                print(Fore.RED + "exit" + Style.RESET_ALL)
                break
        
            print(Fore.YELLOW + f"Client: the second number is {num2}" + Style.RESET_ALL)
        
            result = client_socket.recv(1024).decode()
        
            if not result:
                raise ConnectionResetError

            print(Fore.BLUE + "Server: The result is ", result + Style.RESET_ALL)
            speak(f"Recieved the result from server {result}")
    
    except (ConnectionResetError, BrokenPipeError):
        print(Fore.RED + "Server disconnected unexpectedly." + Style.RESET_ALL)
        speak("Server disconnected unexpectedly")

    except socket.error as e:
        print(Fore.RED + f"Socket error: {e}" + Style.RESET_ALL)
        speak("A socket error occurred")

    finally:
        try:
            client_socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        client_socket.close()
        print(Fore.RED + "Client disconnected." + Style.RESET_ALL)
        speak("Client disconnected")  

if __name__ == "__main__":
    client()

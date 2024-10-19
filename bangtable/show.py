import socket
SERVER_IP = '192.168.11.5'
SERVER_PORT = 53087

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
  server_socket.bind((SERVER_IP,SERVER_PORT))
  
  server_socket.listen()
  print("connecting....")
  
  conn,addr = server_socket.accept()
  
  with conn:
    print(f"接続されました:{addr}")
    while True:
      data = conn.recv(1024)
      if not data:
        break
      print(f"受信したデータ:{data.decode('utf-8')}")
      
      response = "Hello from server"
      conn.sendall(response.encode('utf-8'))
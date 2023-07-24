import java.net.*;
import java.io.*;
import java.util.ArrayList;

public class ClientAccepter extends Thread {
    Socket socket;
    DataInputStream leInput;
    DataOutputStream leOutput;
    ArrayList<Socket> sockets;

    public ClientAccepter(Socket socket, ArrayList<Socket> sockets) throws Exception {
        this.socket = socket;
        this.leInput = new DataInputStream(socket.getInputStream());
        this.leOutput = new DataOutputStream(socket.getOutputStream());
        this.sockets = sockets;
    }

    @Override
    public void run() {
        while (!socket.isClosed()) {
            try {
                String input = leInput.readUTF();
                System.out.println(input);
            } catch (IOException e) {
                System.out.println(e.getLocalizedMessage());
                // handle the IOException by closing the socket and removing it from the list of sockets
                try {
                    socket.close();
                    sockets.remove(socket);
                } catch (IOException ex) {
                    System.out.println(ex.getLocalizedMessage());
                }
            }
        }
    }
}

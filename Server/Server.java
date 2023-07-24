import java.net.*;
import java.util.ArrayList;

public class Server {
    public static void main (String [] args) throws Exception {
        ServerSocket serverSocket;
        int nCtr = 0;
        serverSocket = new ServerSocket(12345);
        serverSocket.setSoTimeout(0);

        ArrayList<ClientAccepter> clientAccepter = new ArrayList<ClientAccepter>();
        ArrayList<Socket> clients = new ArrayList<Socket>();

        while (!serverSocket.isClosed()) {
            clients.add(serverSocket.accept());
            clientAccepter.add(new ClientAccepter( clients.get(nCtr), clients) );
            clientAccepter.get(nCtr).start();
            nCtr++;
            System.out.println("---------- Message Board Server ----------");
            System.out.println("A client has entered the Message Board Server!");
            System.out.println("Number of clients connected: " + clients.size());

        }
    }
}

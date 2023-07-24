import java.io.*;
import java.net.*;
import java.util.*;

public class ClientHandler extends Thread {
    private String handle;
    private Socket socket;
    private ArrayList<Socket> clients;
    private BufferedReader reader;
    private PrintWriter writer;

    public ClientHandler(Socket socket, ArrayList<Socket> clients) throws IOException {
        this.socket = socket;
        this.clients = clients;
        reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        writer = new PrintWriter(socket.getOutputStream(), true);
    }

    public void run() {
        try {
            // Get the handle from the client
            handle = reader.readLine();
            System.out.println(handle + " has joined the chat!");

            while (true) {
                // Read a message from the client
                String message = reader.readLine();

                // Check if the message is a direct message to a specific client
                if (message.startsWith("@")) {
                    String[] tokens = message.split(" ", 2);
                    String recipient = tokens[0].substring(1);
                    message = tokens[1];

                    // Loop through all connected clients and send the message to the recipient only
                    for (Socket client : clients) {
                        PrintWriter clientWriter = new PrintWriter(client.getOutputStream(), true);
                        BufferedReader clientReader = new BufferedReader(new InputStreamReader(client.getInputStream()));
                        String clientHandle = clientReader.readLine();
                        if (clientHandle.equals(recipient)) {
                            System.out.println(message);
                            clientWriter.println(handle + " (DM): " + message);
                            break;
                        }
                    }
                } else {
                    // Broadcast the message to all connected clients
                    for (Socket client : clients) {
                        PrintWriter clientWriter = new PrintWriter(client.getOutputStream(), true);
                        System.out.println(message);
                        clientWriter.println(handle + ": " + message);
                    }
                }
            }
        } catch (IOException e) {
            System.out.println(handle + " has left the chat!");
        }
    }
}

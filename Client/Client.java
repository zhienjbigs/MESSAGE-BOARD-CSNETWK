import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.*;
import java.util.HashMap;
import java.util.Scanner;
import org.json.simple.*;

public class Client {
    public static void main (String [] args) throws Exception {
        Socket socket = new Socket();
        Commands cmd = new Commands();

        System.out.println("Hello! Please input a command to start: ");

        while (true) {
            cmd.commandFuncs(socket);
        }

    }
}

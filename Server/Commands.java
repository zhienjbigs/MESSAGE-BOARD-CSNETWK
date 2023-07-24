import org.json.simple.JSONObject;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.util.HashMap;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;

public class Commands {
    DataOutputStream leOutput;
    HashMap<String, String> hmc;
    Scanner sc = new Scanner (System.in);
    JSONObject throwJson;
    boolean isConnected;

    public Commands() {
        hmc = new HashMap<String, String>();
        hmc.put("command", null);
        hmc.put("handle", null);
        hmc.put("message", null);
        hmc.put("error", null);
        this.throwJson = null;
        isConnected = false;
    }

    private static HashMap<String, DataOutputStream> clients = new HashMap<>();
    public boolean commandFuncs(Socket socket) throws IOException, InterruptedException {
        String scannerInput = sc.nextLine();
        String splitter; //scannerInput.substring(0, scannerInput.indexOf(" "));
        String splitterVal;
        boolean validCommandEntered = false;

        if ( scannerInput.compareTo("/?") == 0 || scannerInput.compareTo("/leave") == 0) {
            splitter = scannerInput;
        }
        else {
            splitter = scannerInput.substring(0, scannerInput.indexOf(" "));
        }

        while (!validCommandEntered) {
            if (splitter.compareTo("/join") == 0) {
                splitterVal = scannerInput.substring(scannerInput.indexOf(" ") + 1);
                String addr = splitterVal.substring(0, splitterVal.indexOf(" "));
                int nPort = Integer.valueOf(splitterVal.substring(splitterVal.indexOf(" ") + 1));
                boolean isValidPort = false;
                while (!isValidPort) {
                    try {
                        socket.connect(new InetSocketAddress(addr, nPort));
                        leOutput = new DataOutputStream(socket.getOutputStream());
                        System.out.println("Connection to the Message Board Server is successful!");
                        isConnected = true;
                        isValidPort = true;
                        validCommandEntered = true;
                    } catch (Exception e) {
                        System.out.println("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.");
                        Scanner sc = new Scanner(System.in);
                        scannerInput = sc.nextLine();
                        splitterVal = scannerInput.substring(scannerInput.indexOf(" ") + 1);
                        addr = splitterVal.substring(0, splitterVal.indexOf(" "));
                        nPort = Integer.valueOf(splitterVal.substring(splitterVal.indexOf(" ") + 1));
                        socket = new Socket();
                        socket.connect(new InetSocketAddress(addr, nPort));
                        leOutput = new DataOutputStream(socket.getOutputStream());
                        System.out.println("Connection to the Message Board Server is successful!");
                        isConnected = true;
                        isValidPort = true;
                        validCommandEntered = true;
                    }
                }
            } else if (splitter.compareTo("/leave") == 0) {
                if (!isConnected) {
                    System.out.println("Disconnection failed, please connect to a server first.");
                    return false;
                }
                System.out.println("Connection closed. Thank you!");
                TimeUnit.SECONDS.sleep(3);
                socket.close();
                validCommandEntered = true;
            } else if (splitter.compareTo("/register") == 0) {
                splitterVal = scannerInput.substring(scannerInput.indexOf(" ") + 1);
                String handle = splitterVal.trim(); // Extract handle from input and remove leading/trailing whitespace
                if (hmc.containsValue(handle)) {
                    hmc.put("error", "Error: Registration failed. Handle or alias already exists");
                    System.out.println("Error: Registration failed. Handle or alias already exists");
                    validCommandEntered = true;
                } else {
                    hmc.put("command", splitter);
                    hmc.put("handle", handle);
                    System.out.println("Welcome " + handle + "!");
                    validCommandEntered = true;
                }
            } else if (splitter.compareTo("/all") == 0) {
                try {
                    splitterVal = scannerInput.substring(scannerInput.indexOf(" ") + 1);
                    hmc.put("message", splitterVal);
                    hmc.put("command", splitter);
                    validCommandEntered = true;

                } catch (Exception e) {
                    hmc.put("error", "Error unknown.");
                    validCommandEntered = true;
                }
            } else if (splitter.compareTo("/msg") == 0) {
                try {
                    splitterVal = scannerInput.substring(scannerInput.indexOf(" ") + 1);
                    String handle = splitterVal.substring(0, splitterVal.indexOf(" "));
                    String message = splitterVal.substring(splitterVal.indexOf(" ") + 1);

                    // Check if handle or alias exists
                    if (!hmc.containsValue(handle)) {
                        hmc.put("error", "Error: Handle or alias not found.");
                        System.out.println("Error: Handle or alias not found.");
                        validCommandEntered = true;
                        continue; // Return to main loop without sending message
                    }

                    hmc.put("command", splitter);
                    hmc.put("handle", handle);
                    hmc.put("message", message);
                    System.out.println("[To" + " " + handle + "]:" + message);
                    validCommandEntered = true;
                } catch (Exception e) {
                    hmc.put("error", "Error unknown.");
                    validCommandEntered = true;
                }
            }
            else if (splitter.compareTo("/?") == 0) {
                System.out.println("Need help? List of available commands: \n");
                System.out.println("/join <address> <port>: Connect to the message board server at the specified address and port.");
                System.out.println("/register <handle>: Register a unique handle with the message board server.");
                System.out.println("/msg <handle> <message>: Send a private message to the specified handle.");
                System.out.println("/all <message>: Send a message to all connected users.");
                System.out.println("/leave: Disconnect from the message board server.");
                System.out.println("/?: List all the available commands for the program.");
                validCommandEntered = true;
                continue;
            } else {
                hmc.put("error", "Error: Command not found.");
                System.out.println("Error: Command not found.");
                scannerInput = new Scanner(System.in).nextLine();
                splitter = scannerInput.substring(0, scannerInput.indexOf(" "));
                continue;
            }
        }

        throwJson = new JSONObject(hmc);

        if (isConnected) {
            leOutput.writeUTF(throwJson.toJSONString());
        }

        return false;
    }

    public boolean handleExists(String handle) {
        String[] registeredHandles = new String[0];
        for (String registeredHandle : registeredHandles) {
            if (registeredHandle.equals(handle)) {
                return false;
            }
        }
        return true;
    }
}

import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class rsvclient {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage:");
            System.out.println("  java rsvclient list <server>");
            System.out.println("  java rsvclient reserve <server> <class> [passenger] [seatNumber]");
            System.out.println("  java rsvclient passengerlist <server>");
            return;
        }

        try {
            String command = args[0].toLowerCase();
            String serverName = args[1];

            Registry registry = LocateRegistry.getRegistry(serverName, 1099);
            reservationInterface stub = (reservationInterface) registry.lookup("ReservationService");

            switch (command) {
                case "list":
                    System.out.println(stub.listAvailability());
                    break;

                case "reserve":
                    if (args.length == 3) {
                        // auto seat
                        String seatClass = args[2];
                        System.out.println(stub.reserveSeat(seatClass));
                    } else if (args.length >= 5) {
                        // specific seat and passenger
                        String seatClass = args[2];
                        String passenger = args[3];
                        int seatNumber = Integer.parseInt(args[4]);
                        System.out.println(stub.reserveSeat(seatClass, passenger, seatNumber));
                    } else {
                        System.out.println("Usage: java rsvclient reserve <server> <class> [passenger] [seatNumber]");
                    }
                    break;

                case "passengerlist":
                    System.out.println(stub.passengerList());
                    break;

                default:
                    System.out.println("Unknown command: " + command);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

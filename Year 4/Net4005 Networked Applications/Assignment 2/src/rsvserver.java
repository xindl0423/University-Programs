import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;
import java.util.*;

public class rsvserver extends UnicastRemoteObject implements reservationInterface {
    private static final int totalbusiness = 5;
    private static final int totaleconomy = 25;
    private static final int totalseats = 30;

    private final List<Integer> businessSeats = new ArrayList<>();
    private final List<Integer> economySeats = new ArrayList<>();

    private final Map<Integer, String> reservations = new HashMap<>();

    public rsvserver() throws RemoteException {
        for (int i = 1; i <= totalbusiness; i++) businessSeats.add(i);
        for (int i = 6; i <= totalseats; i++) economySeats.add(i);
    }


    @Override
    public synchronized String listAvailability() throws RemoteException {
        StringBuilder sb = new StringBuilder();

        sb.append("Business class:\n");
        sb.append(describeSeats(businessSeats, "business"));
        sb.append("\nEconomy class:\n");
        sb.append(describeSeats(economySeats, "economy"));

        return sb.toString();
    }

    private String describeSeats(List<Integer> seats, String seatClass) {
        if (seats.isEmpty()) return "No seats available.\n";

        Map<Integer, List<Integer>> priceBuckets = new LinkedHashMap<>();

        for (int seat : seats) {
            int price = getPrice(seatClass, seat);
            priceBuckets.computeIfAbsent(price, k -> new ArrayList<>()).add(seat);
        }

        StringBuilder sb = new StringBuilder();
        for (Map.Entry<Integer, List<Integer>> e : priceBuckets.entrySet()) {
            sb.append(e.getValue().size())
              .append(" seats at $").append(e.getKey())
              .append(" each\nSeat numbers: ")
              .append(e.getValue()).append("\n");
        }
        return sb.toString();
    }


    @Override
    public synchronized String reserveSeat(String seatClass) throws RemoteException {
        List<Integer> targetList = seatClass.equalsIgnoreCase("business") ? businessSeats : economySeats;

        if (targetList.isEmpty()) return "No seats left in " + seatClass + " class.";

        int seatNumber = targetList.remove(0);
        int price = getPrice(seatClass, seatNumber);
        reservations.put(seatNumber, "Anonymous");

        return "Seat " + seatNumber + " in " + seatClass + " class reserved for $" + price + ".";
    }

    @Override
    public synchronized String reserveSeat(String seatClass, String passenger, int seatNumber) throws RemoteException {
        if (reservations.containsKey(seatNumber))
            return "Seat " + seatNumber + " is already reserved by " + reservations.get(seatNumber) + ".";

        if (seatClass.equalsIgnoreCase("business") && (seatNumber < 1 || seatNumber > 5))
            return "Invalid seat number for business class.";
        if (seatClass.equalsIgnoreCase("economy") && (seatNumber < 6 || seatNumber > 30))
            return "Invalid seat number for economy class.";

        List<Integer> targetList = seatClass.equalsIgnoreCase("business") ? businessSeats : economySeats;
        if (!targetList.contains(seatNumber))
            return "Seat " + seatNumber + " not available.";

        targetList.remove(Integer.valueOf(seatNumber));
        reservations.put(seatNumber, passenger);
        int price = getPrice(seatClass, seatNumber);

        return "Seat " + seatNumber + " in " + seatClass + " class reserved for " + passenger + " at $" + price + ".";
    }

    @Override
    public synchronized String passengerList() throws RemoteException {
        if (reservations.isEmpty()) return "No passengers yet.";

        StringBuilder sb = new StringBuilder("Passenger List:\n");
        reservations.forEach((seat, name) -> sb.append("Seat ").append(seat)
                                              .append(": ").append(name).append("\n"));
        return sb.toString();
    }

    private int getPrice(String seatClass, int seatNumber) {
        if (seatClass.equalsIgnoreCase("business")) {
            int sold = totalbusiness - businessSeats.size();
            return (sold < 3) ? 500 : 800;
        } else {
            int sold = totaleconomy - economySeats.size();
            if (sold < 10) return 200;
            else if (sold < 20) return 300;
            else return 450;
        }
    }

    public static void main(String[] args) {
        try {
            reservationInterface server = new rsvserver();
            Registry registry = LocateRegistry.createRegistry(1099);
            registry.rebind("ReservationService", server);
            System.out.println("Reservation server is running...");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

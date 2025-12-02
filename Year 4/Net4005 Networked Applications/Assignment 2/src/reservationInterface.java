import java.rmi.Remote;
import java.rmi.RemoteException;

public interface reservationInterface extends Remote {
    // List current seat availability
    String listAvailability() throws RemoteException;

    // Reserve the next available seat in a class (automatic seat assignment)
    String reserveSeat(String seatClass) throws RemoteException;

    // Reserve a specific seat for a passenger
    String reserveSeat(String seatClass, String passenger, int seatNumber) throws RemoteException;

    // View all passengers and their seats
    String passengerList() throws RemoteException;
}

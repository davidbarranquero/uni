// Java Train Ticketing System using Java Swing Components

import javax.swing.*;
import java.awt.*;
import java.io.FileNotFoundException;
import java.io.Serializable;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Formatter;
import java.util.NoSuchElementException;


interface PriceModifier {  // Our interface which Passenger and Ticket will implement
    double getPriceModifier();
}

abstract class Passenger implements PriceModifier, Serializable { // Our abstract Passenger Superclass
    private String fullName, firstName, lastName, passengerType; // Local Variables for Passengers
    private LocalDateTime dob;
    private Ticket ticket;

    private DateTimeFormatter dateFormat = DateTimeFormatter.ofPattern("dd/MM/yyyy");

    public Passenger() {
    }  // Default Constructor

    // Our Constructor to make the Passenger Object
    public Passenger(String firstName, String lastName, LocalDateTime dob, String passengerType) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.dob = dob;
        this.passengerType = passengerType;

        fullName = getFirstName() + " " + getLastName();
    }

    @Override // Our toString method to display the object
    public String toString() {
        return String.format("Name: %s\nDOB: %s", getFullName(), getDob());
    }

    // Our interface method
    public abstract double getPriceModifier();

    // A series of getter methods to return the Passenger attributes
    public String getFullName() {
        return fullName;
    }

    public String getFirstName() {
        return firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public String getDob() {
        return dob.format(dateFormat);
    }

    public String getPassengerType() {
        return passengerType;
    }

    public Ticket getTicket() {
        return ticket;
    }

    // A series of setter methods to set the Passenger attributes
    public void setFullName(String first, String last) {
        this.fullName = first + " " + last;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public void setDob(LocalDateTime dob) {
        this.dob = dob;
    }

    public void setPassengerType(String passengerType) {
        this.passengerType = passengerType;
    }

    public void setTicket(Ticket ticket) {
        this.ticket = ticket;
    }

    // Our method for calculating the base passenger cost
    public double calculatePassengerCost(int origin, int destination) {
        if (origin != 9 && destination != 9) {
            return 1.2 * Math.abs(origin - destination);
        } else {
            return (1.2 * Math.abs(origin - destination)) + 15;
        }
    }
}

class AdultPassenger extends Passenger { // Our AdultPassenger sub-class that extends Passenger

    // Default constructor
    public AdultPassenger() {
    }

    // Our constructor for the sub class
    public AdultPassenger(String firstName, String lastName, LocalDateTime dob, String passengerType) {
        super(firstName, lastName, dob, passengerType);
    }

    @Override // We override the interface/abstract method and return the AdultPassenger price modifier
    public double getPriceModifier() {
        return 1;
    }
}

class ChildPassenger extends Passenger { // Our ChildPassenger sub-class that extends Passenger

    // Default constructor
    public ChildPassenger() {
    }

    // Our constructor for the sub class
    public ChildPassenger(String firstName, String lastName, LocalDateTime dob, String passengerType) {
        super(firstName, lastName, dob, passengerType);
    }

    @Override // We override the interface/abstract method and return the ChildPassenger price modifier
    public double getPriceModifier() {
        return 0.5;
    }
}

class SeniorPassenger extends Passenger { // Our SeniorPassenger sub-class that extends Passenger

    // Default constructor
    public SeniorPassenger() {
    }

    // Our constructor for the sub class
    public SeniorPassenger(String firstName, String lastName, LocalDateTime dob, String passengerType) {
        super(firstName, lastName, dob, passengerType);
    }

    @Override // We override the interface/abstract method and return the ChildPassenger price modifier
    public double getPriceModifier() {
        return 0.1;
    }
}


abstract class Ticket implements PriceModifier, Serializable { // Our abstract Ticket super class
    private Passenger passenger;
    private int start, end, ticketID;
    private double cost;
    private String passengerType, ticketType;
    private static int ticketCount = 1;  //For setting a unique id

    // We store all the station names in an array
    String[] stationNames = {"Kiama", "Shellharbour", "Dapto", "Wollongong", "North Wollongong", "Thirroul",
            "Sutherland", "Hurstville", "Wolli Creek", "Central"};

    // Default Constructor
    public Ticket() {
    }

    // Our constructor for the superclass
    public Ticket(Passenger passenger, int start, int end, String passengerType, String ticketType) {
        this.passenger = passenger;
        this.start = start;
        this.end = end;
        this.passengerType = passengerType;
        this.ticketType = ticketType;

        setID();
    }

    @Override // Our toString method to display the tickets
    public String toString() {
        return String.format("Ticket ID: JE-%s\nTicket Type: %s\nOrigin: %s\nDestination: %s\nCost: $%s\nPassenger Info: \n%s\nPassenger Type: %s\n",
                getID(), getTicketType(), getStart(), getEnd(), getCost(), getPassenger(), getPassengerType());
    }

    // Our interface method
    public abstract double getPriceModifier();

    // A series of getter methods to return the Ticket attributes
    public Passenger getPassenger() {
        return passenger;
    }

    public String getStart() {
        return stationNames[start - 1];
    }

    public String getEnd() {
        return stationNames[end - 1];
    }

    public double getCost() {
        return cost;
    }

    public String getPassengerType() {
        return passengerType;
    }

    public String getTicketType() {
        return ticketType;
    }

    public int getID() { //Returns the task ID
        return ticketID;
    }

    // A series of setter methods to set the Ticket attributes
    public void setID() { //Sets a unique ID for each new task
        ticketID = ticketCount++;
    }

    public void setTicketType(String ticketType) {
        this.ticketType = ticketType;
    }

    public void setPassengerType(String passengerType) {
        this.passengerType = passengerType;
    }

    public void setPassenger(Passenger passenger) {
        this.passenger = passenger;
    }

    public void setStart(int start) {
        this.start = start;
    }

    public void setEnd(int end) {
        this.end = end;
    }

    public void setCost(double cost) {
        this.cost = cost;
    }

}

class OneWayTicket extends Ticket { // Our OneWayTicket sub-class that extends Ticket

    // Default Constructor
    public OneWayTicket() {
    }

    // Our constructor for the subclass
    public OneWayTicket(Passenger passenger, int start, int end, String passengerType, String ticketType) {
        super(passenger, start, end, passengerType, ticketType);
    }

    @Override // We override the interface/abstract method to return the ticket's price modifier
    public double getPriceModifier() {
        return 1;
    }
}

class ReturnTicket extends Ticket { // Our ReturnTicket sub-class that extends Ticket

    // Default Constructor
    public ReturnTicket() {
    }

    // Our constructor for the subclass
    public ReturnTicket(Passenger passenger, int start, int end, String passengerType, String ticketType) {
        super(passenger, start, end, passengerType, ticketType);
    }

    @Override // We override the interface/abstract method to return the ticket's price modifier
    public double getPriceModifier() {
        return 1.8;
    }

}

class WeeklyTicket extends Ticket { // Our WeeklyTicket sub-class that extends Ticket

    // Default Constructor
    public WeeklyTicket() {
    }

    // Our constructor for the subclass
    public WeeklyTicket(Passenger passenger, int start, int end, String passengerType, String ticketType) {
        super(passenger, start, end, passengerType, ticketType);
    }

    @Override // We override the interface/abstract method to return the ticket's price modifier
    public double getPriceModifier() {
        return 6 * 1.8;
    }

}


class Journey implements Serializable { // Our journey class to store the created tickets

    ArrayList<Ticket> ticketList;

    double totalCost = 0;

    String[] stationNames = {"Kiama", "Shellharbour", "Dapto", "Wollongong", "North Wollongong", "Thirroul",
            "Sutherland", "Hurstville", "Wolli Creek", "Central"};

    // Our constructor for the Journey class
    public Journey() {
        ticketList = new ArrayList<>();
    }

    @Override
    public String toString() { // Our toString method to display the Journey Summary
        StringBuilder journeyString = new StringBuilder();
        journeyString.append("\nTicket Order Summary:\n");
        journeyString.append("\nNumber of Tickets: ").append(getNumberOfTickets()).append("\n");
        journeyString.append("\nTotal Order Cost: $").append(roundFiveCents(getTotalCost())).append("\n\n");

        for (Ticket ticket : ticketList) {
            journeyString.append(ticket).append("\n\n");
        }

        return journeyString.toString();
    }

    // Getter methods to return journey attributes
    public int getNumberOfTickets() {
        return ticketList.size();
    }

    public double getTotalCost() {
        calculateTotalCost();
        return totalCost;
    }

    public String[] getStationNames() {
        return stationNames;
    }

    public ArrayList<Ticket> getTicketList() {
        return ticketList;
    }

    // Setter methods for class attributes
    public void setStationNames(String[] stationNames) {
        this.stationNames = stationNames;
    }

    public void setTicketList(ArrayList<Ticket> ticketList) {
        this.ticketList = ticketList;
    }

    // A method to calculate the cumulative cost of all the tickets for the journey
    public void calculateTotalCost() {
        totalCost = 0;
        for (Ticket ticket : ticketList) {
            totalCost += ticket.getCost();
        }
    }

    // A method to round the price to the nearest 5 cents
    public double roundFiveCents(double value) {
        double unrounded, fiveCents = 0;
        int rounded, remainder;
        unrounded = value * 1000; // Brings three decimal places above the decimal point
        if (unrounded % 10 >= 5) {
            unrounded /= 10;
            unrounded += 1;
            rounded = (int) unrounded;
        } else {
            unrounded /= 10;
            rounded = (int) unrounded;
        }
        remainder = rounded % 10;
        switch (remainder) {
            case 0:
            case 5:
                fiveCents = (double) rounded / 100;
                break;
            case 1:
            case 6:
                fiveCents = (double) (rounded - 1) / 100;
                break;
            case 2:
            case 7:
                fiveCents = (double) (rounded - 2) / 100;
                break;
            case 3:
            case 8:
                fiveCents = (double) (rounded + 2) / 100;
                break;
            case 4:
            case 9:
                fiveCents = (double) (rounded + 1) / 100;
                break;
        }
        return fiveCents;
    }

    // Methods to add and removeTickets
    public void addTicket(Ticket ticket) {
        ticketList.add(ticket);
    }

    public void removeTicket(int index) {
        ticketList.remove(index);
    }
}


public class TicketingSystem extends JFrame implements Serializable, ActionListener {

    public static Formatter ticketOutput;

    private final JPanel buttonPanel;
    private final JPanel titlePanel; // Panels to hold our JComponents
    private final JPanel leftPanel;
    private final JPanel rightPanel;
    private final JPanel mainMenu;
    private final JPanel editTicketPanel;
    private final JPanel removeTicketPanel;

    private JPanel addTicket; // Main panel for creating ticket

    private JTextArea displayTicketInformation; // Text Areas to hold the text

    private JList<String> ticketsToChangeList; // JList to hold the tickets we want to edit

    private final JLabel mainMenuTitle; // And a Main menu title

    private JButton addTicketButton;

    private final JButton[] buttons; // An array to hold our main menu buttons, and another for their names
    private static final String[] buttonNames = {"Add New Ticket", "Edit Ticket", "Remove Ticket(s)", "Buy Tickets", "Exit Ticket System"};
    private static final String[] days = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
            "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"};
    private static final String[] months = {"January", "February", "March", "April", "May", "June", "July", "August",
            "September", "October", "November", "December"};
    private static String[] unsortedYears = new String[122];
    private static String[] years = new String[122];

    private final GridLayout gridLayout;
    private final CardLayout cardLayout; // We will primarily use a CardLayout design for our project
    private final Container cards;

    // Ticket and Passenger attributes
    private String ticketType = "", firstName = "", lastName = "", passengerType = "",
            dayString = "", yearString = "";

    private int dayInt, monthInt, yearInt, monthDayMax, origin, destination, ticketToEdit;

    private double displayCost, ticketCost;

    private boolean edit = false;

    private LocalDateTime passengerDOB;

    // We create variables to store the created objects
    Passenger passenger = null;
    Ticket ticket = null;
    Journey journey = new Journey();


    public static void main(String[] args) { // Our main method

        // Create the JFrame and display it
        TicketingSystem ticketingSystem = new TicketingSystem();
        ticketingSystem.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        ticketingSystem.setSize(900, 600);
        ticketingSystem.setVisible(true);
    }

    public TicketingSystem() { // Our constructor for the TicketingSystem
        super("CSIT121 Final Project 2021 David Barranquero");
        cardLayout = new CardLayout(); // Set the layout dimensions for our main menu with our buttons
        gridLayout = new GridLayout(1, 3, 10, 10);

        // We fill our years array with the appropriate values from
        for (int i = 1900; i < 2022; i++) {
            String year = String.valueOf(i);
            unsortedYears[i - 1900] = year;
        }

        // We reverse the order so that our drop down list will display current years first
        for (int j = 0; j < 122; j++) {
            years[j] = unsortedYears[121 - j];
        }

        // We set the title for our Main Menu in the Panel
        mainMenuTitle = new JLabel("Welcome to the Java Express Train Ticketing System.");
        titlePanel = new JPanel();
        titlePanel.add(mainMenuTitle);

        // We set the button panel for our buttons
        buttonPanel = new JPanel();
        buttonPanel.setLayout(gridLayout);
        buttonPanel.setMaximumSize(new Dimension(100, 50));
        buttons = new JButton[buttonNames.length];

        // And create our Main menu Panel with a border layout
        mainMenu = new JPanel();
        mainMenu.setLayout(new BorderLayout(5, 5));

        // We create the Panels to add, edit and remove the tickets
        addTicket = new JPanel(new BorderLayout(10, 10));

        editTicketPanel = new JPanel(new BorderLayout());
        updateLists('s');
        editTicketPanel.add(ticketsToChangeList, BorderLayout.CENTER);
        editTicketPanel.add(new JScrollPane(ticketsToChangeList));

        removeTicketPanel = new JPanel(new BorderLayout());
        updateLists('m');
        removeTicketPanel.add(ticketsToChangeList, BorderLayout.CENTER);
        removeTicketPanel.add(new JScrollPane(ticketsToChangeList));

        // And a text area to display the order summaries
        displayTicketInformation = new JTextArea(50, 50); // Create text areas
        displayTicketInformation.setText(journey.toString());
        displayTicketInformation.setEditable(false);

        // Use a for loop to iterate through the buttons and add a new button to the button array
        for (int count = 0; count < buttonNames.length; count++) {
            buttons[count] = new JButton(buttonNames[count]);
            buttons[count].setPreferredSize(new Dimension(100, 50));
            buttons[count].addActionListener(this);
            buttonPanel.add(buttons[count]);
        }

        // Create our buffer panels
        leftPanel = new JPanel();
        rightPanel = new JPanel();

        // Call the method to create our panel
        new CreateTicketPanel();

        // And we add these to the main menu panel
        mainMenu.add(buttonPanel, BorderLayout.SOUTH);
        mainMenu.add(titlePanel, BorderLayout.NORTH);
        mainMenu.add(new JScrollPane(displayTicketInformation), BorderLayout.CENTER);
        mainMenu.add(leftPanel, BorderLayout.WEST);
        mainMenu.add(rightPanel, BorderLayout.EAST);

        // We set the cards Container, give it a CardLayout and add the 4 different menu screens to the container
        cards = getContentPane();
        cards.setLayout(cardLayout);
        cards.add("mainMenu", mainMenu);
        cards.add("addTicket", addTicket);

        cardLayout.show(cards, "mainMenu"); // Finally display the main menu
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == buttons[0]) { // If they click addStaff, we update all Multi-option lists and show the page
            addTicketButton.setText("Add Ticket");
            cardLayout.show(cards, "addTicket");
        } else if (e.getSource() == buttons[1]) { // If they wish to edit
            if (journey.ticketList.isEmpty()) { // First check if there are tickets
                JOptionPane.showMessageDialog(null, "No Tickets to Edit.");
            } else {
                updateLists('s'); // Create a single selection summary list of tickets
                editTicketPanel.removeAll();
                editTicketPanel.add(ticketsToChangeList, BorderLayout.CENTER);
                editTicketPanel.add(new JScrollPane(ticketsToChangeList));
                int option = JOptionPane.showOptionDialog(null, editTicketPanel,
                        "Select Ticket to Edit", // Get the user's selection
                        JOptionPane.OK_CANCEL_OPTION,
                        JOptionPane.INFORMATION_MESSAGE,
                        null, null, null);
                if (option == JOptionPane.OK_OPTION) { // Process the ticket to be edited
                    ticketToEdit = ticketsToChangeList.getSelectedIndex();
                    edit = true;
                    addTicketButton.setText("Edit Ticket");
                    cardLayout.show(cards, "addTicket");
                }
            }
        } else if (e.getSource() == buttons[2]) { // If they want to remove
            if (journey.ticketList.isEmpty()) { // First check that there are tickets to remove
                JOptionPane.showMessageDialog(null, "No Tickets to Remove.");
            } else {
                updateLists('m'); // Allow multiple selection
                removeTicketPanel.removeAll(); // Create a single selection summary list of tickets
                removeTicketPanel.add(ticketsToChangeList, BorderLayout.CENTER);
                removeTicketPanel.add(new JScrollPane(ticketsToChangeList));
                int option = JOptionPane.showOptionDialog(null, removeTicketPanel,
                        "Select Tickets to Remove", // Get the user's selection
                        JOptionPane.OK_CANCEL_OPTION,
                        JOptionPane.INFORMATION_MESSAGE,
                        null, null, null);

                if (option == JOptionPane.OK_OPTION) { // Create arrays
                    int[] unsortedIndices = ticketsToChangeList.getSelectedIndices();
                    int[] sortedIndices = new int[unsortedIndices.length];

                    Arrays.sort(unsortedIndices);

                    for (int i = 0; i < unsortedIndices.length; i++) { // Get indices in descending order
                        sortedIndices[i] = unsortedIndices[unsortedIndices.length - 1 - i];
                    }

                    for (int sortedIndex : sortedIndices) { // remove tickets
                        journey.removeTicket(sortedIndex);
                    }
                    updateSummary(); // update summary
                }
            }
        } else if (e.getSource() == buttons[3]) { // If they wish to purchase
            if (journey.ticketList.isEmpty()) {
                JOptionPane.showMessageDialog(null, "No Tickets to Purchase.");
            } else {
                int option = JOptionPane.showOptionDialog(null, "Confirm Purchase?",
                        "Buy Tickets", // Get confirmation from user
                        JOptionPane.OK_CANCEL_OPTION,
                        JOptionPane.INFORMATION_MESSAGE,
                        null, null, null);
                if (option == JOptionPane.OK_OPTION) {
                    String  textFileName = journey.ticketList.get(0).getPassenger().getLastName().toLowerCase() + ".txt";
                    try { // Try to create/access the file
                        System.out.println("Creating New Text File...");
                        ticketOutput = new Formatter(textFileName);
                    } catch (SecurityException | FileNotFoundException error) { // Check if failed
                        System.out.println("Error. Access denied. Program will exit.");
                    }
                    try { // Try to write the school objects to a text file
                        System.out.println("Writing Objects to Text File...");
                        ticketOutput.format("%s", journey);
                        System.out.println("Ticket Exporting Complete.");
                        JOptionPane.showMessageDialog(null, "Tickets saved under '" + textFileName + "'.\nEnjoy your Journey!");
                    } catch (NoSuchElementException error) { // Check if failed
                        System.out.println("Error. Tickets DNE.");
                    } finally { // Irrespective, we close the file when finished.
                        System.out.println("Closing File.");
                        ticketOutput.close();
                    }
                    journey.ticketList.clear();
                    updateSummary();
                }
            }

        } else if (e.getSource() == buttons[4]) { // We update all lists to ensure consistency of the program
            JOptionPane.showMessageDialog(null, "Thank you for choosing Java Express. Enjoy your journey!");
            System.exit(0);
        }
    }

    public void updateLists(char selection) { // updates the summary lists for the tickets for altering tickets
        String[] ticketsToAlter = new String[journey.getNumberOfTickets()];
        for (int i = 0; i < journey.ticketList.size(); i++) {
            ticketsToAlter[i] = String.format("Ticket ID: JE-%s, Type: %s, Passenger: %s, Trip: %s -> %s\n",
                    journey.ticketList.get(i).getID(),
                    journey.ticketList.get(i).getTicketType(),
                    journey.ticketList.get(i).getPassenger().getFullName(),
                    journey.ticketList.get(i).getStart(),
                    journey.ticketList.get(i).getEnd());
        }

        ticketsToChangeList = new JList(ticketsToAlter);
        ticketsToChangeList.setPreferredSize(new Dimension(600, 500));
        ticketsToChangeList.setVisibleRowCount(5);
        if (selection == 's') {
            ticketsToChangeList.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        } else if (selection == 'm') {
            ticketsToChangeList.setSelectionMode(ListSelectionModel.MULTIPLE_INTERVAL_SELECTION); // Allow multiple interval selection
        }
    }

    public class CreateTicketPanel implements ActionListener {

        private JPanel addTicketButtonPanel; // A collection of JPanels for different components
        private JPanel informationPanel;
        private JPanel dobPanel;
        private JPanel ticketTypePanel;
        private JPanel passengerTypePanel;
        private JPanel invisiblePanel;
        private JPanel leftPanel;
        private JPanel rightPanel;

        private JLabel addTicketLabel; // A series of JLabels to instruct the user to enter information
        private JLabel passengerFirstNameLabel;
        private JLabel passengerLastNameLabel;
        private JLabel passengerDOBLabel;
        private JLabel passengerTypeLabel;
        private JLabel ticketTypeLabel;
        private JLabel originLabel;
        private JLabel destinationLabel;
        private JLabel costLabel;

        private JButton clearTicketButton;// All our menus will have a return, clear and add button
        private JButton addTicketMenuButton;

        private JTextField passengerFirstNameText; // Several JTextFields where the user can enter the Passenger's name
        private JTextField passengerLastNameText;

        private JRadioButton adultButton; // Some radio buttons for mutually exclusive options like passenger and ticket type
        private JRadioButton childButton;
        private JRadioButton seniorButton;
        private ButtonGroup passengerTypeButtons;

        private JRadioButton oneWayTicketButton; // Some radio buttons for mutually exclusive options like passenger and ticket type
        private JRadioButton returnTicketButton;
        private JRadioButton weeklyTicketButton;
        private ButtonGroup ticketTypeButtons;

        private JComboBox<String> dayList; // ComboBoxes for our immutable lists
        private JComboBox<String> monthList;
        private JComboBox<String> yearList;
        private JComboBox<String> originList;
        private JComboBox<String> destinationList;

        public CreateTicketPanel() { // Our constructor for the page

            // First we create all the panels and set the appropriate layouts
            addTicketButtonPanel = new JPanel(new GridLayout(1, 3));
            informationPanel = new JPanel(new GridLayout(10, 2, 20, 20));
            dobPanel = new JPanel(new GridLayout(1, 3));
            passengerTypePanel = new JPanel();
            ticketTypePanel = new JPanel();
            invisiblePanel = new JPanel();
            leftPanel = new JPanel();
            rightPanel = new JPanel();

            // Then we create the three buttons, and attach action listeners to them
            addTicketButton = new JButton("Add Ticket");
            addTicketButton.setPreferredSize(new Dimension(40, 40));
            addTicketButton.addActionListener(this);

            clearTicketButton = new JButton("Clear and Reset");
            clearTicketButton.setPreferredSize(new Dimension(40, 40));
            clearTicketButton.addActionListener(this);

            addTicketMenuButton = new JButton("Return to Main Menu");
            addTicketMenuButton.setPreferredSize(new Dimension(40, 40));
            addTicketMenuButton.addActionListener(this);

            // Next we create the JRadioButtons for the ticket type
            oneWayTicketButton = new JRadioButton("One-Way", true);
            returnTicketButton = new JRadioButton("Return", false);
            weeklyTicketButton = new JRadioButton("Weekly", false);
            ticketTypeButtons = new ButtonGroup(); // Add them to a button group
            ticketTypeButtons.add(oneWayTicketButton);
            ticketTypeButtons.add(returnTicketButton);
            ticketTypeButtons.add(weeklyTicketButton);
            oneWayTicketButton.addItemListener(new TicketRBHandler("One-way"));
            returnTicketButton.addItemListener(new TicketRBHandler("Return"));
            weeklyTicketButton.addItemListener(new TicketRBHandler("Weekly"));
            ticketType = "One-way"; // We set the default value

            // We also create the passenger type radio buttons
            adultButton = new JRadioButton("Adult", true);
            childButton = new JRadioButton("Child", false);
            seniorButton = new JRadioButton("Senior", false);
            passengerTypeButtons = new ButtonGroup(); // Add them to a button group
            passengerTypeButtons.add(adultButton);
            passengerTypeButtons.add(childButton);
            passengerTypeButtons.add(seniorButton);
            adultButton.addItemListener(new PassengerRBHandler("Adult"));
            childButton.addItemListener(new PassengerRBHandler("Child"));
            seniorButton.addItemListener(new PassengerRBHandler("Senior"));
            passengerType = "Adult"; // We set the default value

            // We create all the JLabels, listing all the information for the user to enter to create the Ticket
            addTicketLabel = new JLabel("Please insert the Passenger and Ticket Information below, then click the 'Add Staff Member' button.", SwingConstants.CENTER);
            passengerFirstNameLabel = new JLabel("Enter Passenger First Name:", SwingConstants.LEFT);
            passengerLastNameLabel = new JLabel("Enter Passenger Last Name:", SwingConstants.LEFT);
            passengerDOBLabel = new JLabel("Enter Passenger DOB:", SwingConstants.LEFT);
            passengerTypeLabel = new JLabel("Passenger Type:", SwingConstants.LEFT);
            ticketTypeLabel = new JLabel("Select Ticket Type (Note: Weekly unavailable for Seniors):", SwingConstants.LEFT);
            originLabel = new JLabel("Select Origin:", SwingConstants.LEFT); // Everything is set to the LHS
            destinationLabel = new JLabel("Select Destination:", SwingConstants.LEFT);
            costLabel = new JLabel("Total Ticket Cost: $" + journey.roundFiveCents(displayCost), SwingConstants.LEFT);

            // We create the Text fields for the responses and make them empty
            passengerFirstNameText = new JTextField("", 30);
            passengerLastNameText = new JTextField("", 30);

            // We create a text field handler for our text fields
            PassengerTextFieldHandler textHandler = new PassengerTextFieldHandler();
            passengerFirstNameText.addFocusListener(textHandler);
            passengerLastNameText.addFocusListener(textHandler);

            dayList = new JComboBox<>(days); // We make our ComboBoxes for the days
            dayList.setMaximumRowCount(10);
            dayList.addItemListener(e -> {
                if (dayList.getSelectedIndex() != -1) { // Filters out when the list selection is cleared returning -1
                    dayString = days[dayList.getSelectedIndex()];
                    dayInt = Integer.parseInt(dayString);
                }
            });

            monthList = new JComboBox<>(months);  // We make our ComboBoxes for the months
            monthList.setMaximumRowCount(10);
            monthList.addItemListener(e -> {
                if (monthList.getSelectedIndex() != -1) { // Filters out when the list selection is cleared returning -1
                    monthInt = monthList.getSelectedIndex()+1;
                }
            });

            yearList = new JComboBox<>(years);  // We make our ComboBoxes for the years
            yearList.setMaximumRowCount(10);
            yearList.addItemListener(e -> {
                if (yearList.getSelectedIndex() != -1) { // Filters out when the list selection is cleared returning -1
                    yearString = years[yearList.getSelectedIndex()];
                    yearInt = Integer.parseInt(yearString);
                }
            });

            // Set the values to the values present in the default list
            dayInt = 1;
            monthInt = 1;
            yearInt = 2021;
            origin = 1;
            destination = 10;

            originList = new JComboBox<>(journey.getStationNames());  // We make our ComboBoxes for the origin station
            originList.setPreferredSize(new Dimension(200, 500));
            originList.setMaximumRowCount(10);
            originList.addItemListener(e -> {
                if (originList.getSelectedIndex() != -1) { // Filters out when the list selection is cleared returning -1
                    origin = originList.getSelectedIndex() + 1;
                    updateCost();
                }
            });

            // We need to assign two different objects to the two different combo boxes, so we make a duplicate list of the stations for the second combobox
            String[] duplicateNames = journey.getStationNames();

            destinationList = new JComboBox<>(duplicateNames);  // We make our ComboBoxes for the destination station
            destinationList.setPreferredSize(new Dimension(200, 500));
            destinationList.setMaximumRowCount(10);
            destinationList.addItemListener(e -> {
                if (destinationList.getSelectedIndex() != -1) { // Filters out when the list selection is cleared returning -1
                    destination = destinationList.getSelectedIndex() + 1;
                    updateCost();
                }
            });

            // Set the selected index to the last one
            destinationList.setSelectedIndex(9);

            addTicketButtonPanel.add(addTicketMenuButton);
            addTicketButtonPanel.add(clearTicketButton);  // We add our three buttons to the student button panel
            addTicketButtonPanel.add(addTicketButton);

            // We attach each pair of label and text to the main panel
            informationPanel.add(passengerFirstNameLabel);
            informationPanel.add(passengerFirstNameText);

            informationPanel.add(passengerLastNameLabel);
            informationPanel.add(passengerLastNameText);

            informationPanel.add(passengerTypeLabel);
            passengerTypePanel.add(adultButton);
            passengerTypePanel.add(childButton);
            passengerTypePanel.add(seniorButton);
            informationPanel.add(passengerTypePanel);

            informationPanel.add(passengerDOBLabel);
            dobPanel.add(dayList);
            dobPanel.add(monthList);
            dobPanel.add(yearList);
            informationPanel.add(dobPanel);

            informationPanel.add(ticketTypeLabel);
            ticketTypePanel.add(oneWayTicketButton);
            ticketTypePanel.add(returnTicketButton);
            ticketTypePanel.add(weeklyTicketButton);
            informationPanel.add(ticketTypePanel);

            informationPanel.add(originLabel);
            informationPanel.add(originList); // Attaching the list panel and scroll pane to their own panel

            informationPanel.add(destinationLabel);
            informationPanel.add(destinationList); // Attaching the list panel and scroll pane to their own panel

            informationPanel.add(invisiblePanel);
            informationPanel.add(costLabel);

            addTicket.add(addTicketLabel, BorderLayout.NORTH);
            addTicket.add(informationPanel, BorderLayout.CENTER); // Finally, we add all this to the main addStudent panel
            addTicket.add(addTicketButtonPanel, BorderLayout.SOUTH);
            addTicket.add(leftPanel, BorderLayout.WEST);
            addTicket.add(rightPanel, BorderLayout.EAST);
        }

        @Override // For the buttons pressed
        public void actionPerformed(ActionEvent e) {
            if (e.getSource() == addTicketButton) { // If they want to make a new Ticket
                try {
                    if (validInput()) { // First we check all the information is valid
                        if (edit) {
                            editTicket(); // Next we check if they're actually editing a ticket (as we reuse the same panel)
                        } else {
                            switch (passengerType) { // We use a switch-case for the passenger type, to create a passenger
                                case "Adult":
                                    passenger = new AdultPassenger(firstName, lastName, passengerDOB, passengerType);
                                    break;
                                case "Child":
                                    passenger = new ChildPassenger(firstName, lastName, passengerDOB, passengerType);
                                    break;
                                case "Senior":
                                    passenger = new SeniorPassenger(firstName, lastName, passengerDOB, passengerType);
                                    break;
                            }
                            switch (ticketType) { // We use a switch-case for the ticket type, to create a ticket
                                case "One-way":
                                    ticket = new OneWayTicket(passenger, origin, destination, passengerType, ticketType);
                                    break;
                                case "Return":
                                    ticket = new ReturnTicket(passenger, origin, destination, passengerType, ticketType);
                                    break;
                                case "Weekly":
                                    ticket = new WeeklyTicket(passenger, origin, destination, passengerType, ticketType);
                                    break;
                            }

                            // We calculate the appropriate ticket cost using the object passenger modifiers
                            ticketCost = passenger.calculatePassengerCost(origin, destination) * passenger.getPriceModifier() * ticket.getPriceModifier();

                            // Then we round to nearest five cents
                            ticketCost = journey.roundFiveCents(ticketCost);

                            // Set the cost to the ticket, add the ticket to the passenger and add the ticket to the journey
                            ticket.setCost(ticketCost);

                            passenger.setTicket(ticket);

                            journey.addTicket(ticket);

                            JOptionPane.showMessageDialog(null, "Ticket Added.");


                        }
                    }
                } catch (InvalidPassengerTypeException ex) { // For invalid passenger types with the date of births
                    JOptionPane.showMessageDialog(null, ex.getMessage());
                }
            } else if (e.getSource() == clearTicketButton) { // If they want to clear, then reset the values
                resetValues();
            } else if (e.getSource() == addTicketMenuButton) { // If the user wishes to return to the main menu, we return
                updateSummary();
                cardLayout.show(cards, "mainMenu");
            }
        }

        public void resetValues() { // Our method to reset the values

            passengerFirstNameText.setText(""); // First we reset all the components
            passengerLastNameText.setText("");
            dayList.setSelectedIndex(0);
            monthList.setSelectedIndex(0);
            yearList.setSelectedIndex(0);
            originList.setSelectedIndex(0);
            destinationList.setSelectedIndex(9);
            adultButton.setSelected(true);
            oneWayTicketButton.setSelected(true);

            firstName = ""; // Then we set all of the variables to whatever the GUI displays when reset
            lastName = "";
            dayInt = 1;
            monthInt = 1;
            yearInt = 2021;
            origin = 1;
            destination = 10;
            passengerType = "Adult";
            ticketType = "One-way";
        }

        public void editTicket() {

            // If this panel is being used to edit a ticket, we edit all the attributes of the ticket with whatever the user has entered.
            journey.ticketList.get(ticketToEdit).getPassenger().setFirstName(firstName);
            journey.ticketList.get(ticketToEdit).getPassenger().setLastName(lastName);
            journey.ticketList.get(ticketToEdit).getPassenger().setFullName(firstName, lastName);
            journey.ticketList.get(ticketToEdit).getPassenger().setDob(passengerDOB);
            journey.ticketList.get(ticketToEdit).getPassenger().setPassengerType(passengerType);
            journey.ticketList.get(ticketToEdit).setStart(origin);
            journey.ticketList.get(ticketToEdit).setEnd(destination);
            journey.ticketList.get(ticketToEdit).setPassengerType(passengerType);
            journey.ticketList.get(ticketToEdit).setTicketType(ticketType);

            // Calculate the new ticket cost
            ticketCost = passenger.calculatePassengerCost(origin, destination) * passenger.getPriceModifier() * ticket.getPriceModifier();
            ticketCost = journey.roundFiveCents(ticketCost);
            journey.ticketList.get(ticketToEdit).setCost(ticketCost);

            // Display a message to the user and reset the appropriate values for testing, error checking and information, then display the main menu
            JOptionPane.showMessageDialog(null, "Ticket has been altered.");
            updateSummary();
            cardLayout.show(cards, "mainMenu");

        }

        public boolean validInput() throws InvalidPassengerTypeException {
            try {
                if (origin == destination) { // First check that the two stations are not the same
                    JOptionPane.showMessageDialog(null, "The Origin and Destination Stations cannot be the same.");
                } else if (!dateValid()) { // Then check that the user hasn't entered an invalid date (E.g. 31 February)
                    throw new IllegalArgumentException();
                } else if ((weeklyTicketButton.isSelected() && seniorButton.isSelected())) {  // Then check that they are not trying to create a weekly senior ticket
                    throw new IllegalStateException();
                } else if (firstName.equals("") || lastName.equals("")) { // Check that the first name and last name have been inputted
                    JOptionPane.showMessageDialog(null, "You must enter a first name and last name for the Passenger.");
                } else {
                    LocalDateTime currentDate = LocalDateTime.now(); // Set current date
                    passengerDOB = LocalDateTime.of(yearInt, monthInt, dayInt, 0, 0); // Get passengers dob from their info
                    int age = (currentDate.getYear() - passengerDOB.getYear()); // Calculate their age
                    if (age < 18 && !childButton.isSelected()) { // Less than 18 is a child
                        throw new InvalidPassengerTypeException("Child");
                    } else if (age >= 65 && !seniorButton.isSelected()) { // 65+ is a senior
                        throw new InvalidPassengerTypeException("Senior");
                    } else if (age >= 18 && age < 65 && !adultButton.isSelected()) { // 18-64 is an adult
                        throw new InvalidPassengerTypeException("Adult");
                    } else {
                        return true; // If all these checks are passed, the user has entered valid input
                    }
                }
            } catch (IllegalArgumentException e) { // Our two exceptions catch blocks
                JOptionPane.showMessageDialog(null, "Date doesn't exist. Please enter a valid Date of Birth");
            } catch (IllegalStateException e) {
                JOptionPane.showMessageDialog(null, "Weekly Ticket option unavailable for Seniors");
            }
            return false;
        }

        public void updateCost() { // Our method to continuously update the display cost of the tickets when the user adjusts the settings

            // We calculate the cost and round, given the ticket they've selected
            if (origin != 9 && destination != 9) {
                displayCost = 1.2 * Math.abs(origin - destination);
            } else {
                displayCost = (1.2 * Math.abs(origin - destination)) + 15;
            }
            displayCost *= getPriceModifiers(passengerType);
            displayCost *= getPriceModifiers(ticketType);
            costLabel.setText("Total Ticket Cost: $" + journey.roundFiveCents(displayCost));
        }

        private class PassengerTextFieldHandler implements FocusListener { // Inner inner class for handling text field events

            @Override
            public void focusGained(FocusEvent e) {
            }

            @Override
            public void focusLost(FocusEvent e) { // When the user clicks away, we take the entered text and save it n the variables
                if (e.getSource() == passengerFirstNameText) {
                    firstName = passengerFirstNameText.getText();
                } else if (e.getSource() == passengerLastNameText) {
                    lastName = passengerLastNameText.getText();
                }

            }
        }

        private class PassengerRBHandler implements ItemListener { // Inner inner class for handling Passenger Type RadioButtons

            private String type;

            public PassengerRBHandler(String type) {
                this.type = type;
            }

            @Override
            public void itemStateChanged(ItemEvent e) { // We set the passenger type and update the cost accordingly
                passengerType = type;
                updateCost();
            }
        }

        private class TicketRBHandler implements ItemListener { // Inner inner class for handling Ticket Type RadioButtons

            private String type;

            public TicketRBHandler(String type) {
                this.type = type;
            }

            @Override
            public void itemStateChanged(ItemEvent e) { // We set the ticket type and update the cost accordingly
                ticketType = type;
                updateCost();
            }
        }
    }

    public double getPriceModifiers(String modifier) { // Our method to provide the price modifiers for the continuously changing displayCost
        switch (modifier) {
            case "Adult":
            case "One-way":
                return 1;
            case "Child":
                return 0.5;
            case "Senior":
                return 0.1;
            case "Return":
                return 1.8;
            case "Weekly":
                return 10.8;
        }
        return 0;
    }


    public void updateSummary() {
        displayTicketInformation.setText(journey.toString());
        displayTicketInformation.setCaretPosition(0);
    }

    public boolean dateValid() { // Tests validity of user's date
        setMonthDayMax();
        return dayInt <= getMonthDayMax();
    }

    public void setMonthDayMax() { // Sets the maximum amount of days in the given month

        int[] daysInMonth = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}; // We create an array of the maximum days in each, 0 being a null variable for our indexing

        monthDayMax = daysInMonth[monthInt]; //Sets the month day max

        if (monthInt == 1) { //Tests for a leap year and if so, adds 1 to the monthDayMax
            if (yearInt % 4 == 0) {
                monthDayMax += 1;
            }
        }
    }

    public int getMonthDayMax() { //Retrieves the maximum amount of days in the given month
        return monthDayMax;
    }

}


class InvalidPassengerTypeException extends Exception { // Custom Exception for matching ID's and subject codes
    private String type;

    public InvalidPassengerTypeException(String type) {
        this.type = type;
    }

    public String getMessage() {
        return "Date of Birth indicates '" + type + "' ticket. Please select that option, or set the correct Date of Birth.";
    }
}


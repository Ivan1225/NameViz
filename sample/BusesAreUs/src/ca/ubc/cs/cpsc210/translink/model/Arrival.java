package ca.ubc.cs.cpsc210.translink.model;

/**
 * Represents an estimated arrival with time to arrival in minutes,
 * the route, the name of destination, and the status (early/late).
 */

public class Arrival implements Comparable<Arrival>{

    private int timeToStop;
    private String destination;
    private Route route;
    private String status;

    public Arrival(int timeToStop, String destination, Route route) {
        this.timeToStop = timeToStop;
        this.destination = destination;
        this.route = route;
        status = "on schedule";
    }

    /**
     * Get time until bus arrives at stop in minutes.
     */
    public int getTimeToStopInMins() {
        return timeToStop;
    }

    public String getDestination() {
        return destination;
    }

    public Route getRoute() {
        return route;
    }

    /**
     * Order bus arrivals by time until bus arrives at stop
     * (shorter times ordered before longer times)
     */
    @Override
    public int compareTo(Arrival arrival) {
        // Do not modify the implementation of this method!
        return this.getTimeToStopInMins() - arrival.getTimeToStopInMins();
    }

    /**
     * Get the status, an indicator of whether the arrival is on schedule, early, or late
     */
    public String getStatus() {
        return status;
    }

    /**
     * Set the status, an indicator of whether the arrival is on schedule, early, or late
     */
    public void setStatus(String status) {
        this.status = status;
    }
}

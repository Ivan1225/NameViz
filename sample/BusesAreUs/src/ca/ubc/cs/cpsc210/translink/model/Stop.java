package ca.ubc.cs.cpsc210.translink.model;

import ca.ubc.cs.cpsc210.translink.util.LatLon;

import java.util.*;

/**
 * Represents a bus stop with an number, name, location (lat/lon)
 * set of routes which stop at this stop and a list of arrivals.
 */

public class Stop implements Iterable<Arrival> {
    private List<Arrival> arrivals;
    private int number;
    private String name;
    private LatLon locn;
    private Set<Route> routes;

    /**
     * Constructs a stop with given number, name and location.
     * Set of routes and list of arrivals are empty.
     */
    public Stop(int number, String name, LatLon locn) {
        arrivals = new ArrayList<>();
        this.number = number;
        this.name = name;
        this.locn = locn;
        routes = new HashSet<>();
    }

    /**
     * getter for name
     */
    public String getName() {
        return name;
    }

    /**
     * getter for locn
     */
    public LatLon getLocn() {
        return locn;
    }

    /**
     * getter for number
     */
    public int getNumber() {
        return number;
    }

    /**
     * getter for set of routes
     */
    public Set<Route> getRoutes() {
        return Collections.unmodifiableSet(routes);
    }

    /**
     * Add route to set of routes with stops at this stop.
     */
    public void addRoute(Route route) {
        routes.add(route);
        route.addStop(this);
    }

    /**
     * Remove route from set of routes with stops at this stop
     */
    public void removeRoute(Route route) {
        routes.remove(route);
        route.removeStop(this);
    }

    /**
     * Determine if this stop is on a given route
     */
    public boolean onRoute(Route route) {
        return route.hasStop(this);
    }

    /**
     * Add bus arrival travelling on a particular route at this stop.
     * Arrivals are to be sorted in order by arrival time
     */
    public void addArrival(Arrival arrival) {
        int index = 0;
        boolean added = false;

        if(arrivals.size() == 0)
        {
            arrivals.add(arrival);
            added = true;
        }
        else
        {
            for(Arrival next : arrivals)
            {
                if(next.compareTo(arrival) >= 0)
                {
                    shift(index, arrival);
                    added = true;
                    break;
                }
                index++;
            }
        }

        if(!added)
            arrivals.add(arrival);
    }

    private void shift(int index, Arrival arrival)
    {
        int i;
        for(i = arrivals.size(); i > index; i--)
        {
            arrivals.add(i, arrivals.get(i-1));
            arrivals.remove(i-1);
        }

        arrivals.add(i, arrival);
    }

    /**
     * Remove all arrivals from this stop
     */
    public void clearArrivals() {
        arrivals.clear();
    }

    /**
     * Two stops are equal if their ids are equal
     */
    @Override
    public boolean equals(Object o) {
        if(this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        Stop stop = (Stop) o;

        return stop.getNumber() == (this.number);
    }

    /**
     * Two stops are equal if their ids are equal.
     * Therefore hashCode only pays attention to number.
     */
    @Override
    public int hashCode() {
        return number;
    }

    @Override
    public Iterator<Arrival> iterator() {
        // Do not modify the implementation of this method!
        return arrivals.iterator();
    }

    /**
     * setter for name
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * setter for location
     */
    public void setLocn(LatLon locn) {
        this.locn = locn;
    }

    /**
     * getter for arrivals
     */
    public List<Arrival> getArrivals()
    {
        return Collections.unmodifiableList(arrivals);
    }
}

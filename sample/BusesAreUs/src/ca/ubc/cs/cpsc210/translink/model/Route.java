package ca.ubc.cs.cpsc210.translink.model;

import java.util.*;
import java.util.List;

/**
 * Represents a bus route with a route number, name, list of stops, and list of RoutePatterns.
 * <p/>
 * Invariants:
 * - no duplicates in list of stops
 * - iterator iterates over stops in the order in which they were added to the route
 */

public class Route implements Iterable<Stop> {
    private List<Stop> stops;
    private String number;
    private String name;
    private List<RoutePattern> routes;

    /**
     * Constructs a route with given number.
     * List of stops is empty.
     */
    public Route(String number) {
        this.number = number;
        name = "";
        stops = new ArrayList<>();
        routes = new ArrayList<>();
    }

    /**
     * Return the number of the route
     */
    public String getNumber() {
        return number;
    }

    /**
     * Set the name of the route
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * Add the pattern to the route if it is not already there
     */
    public void addPattern(RoutePattern pattern) {
        if(!routes.contains(pattern))
        {
            routes.add(pattern);
            pattern.setRoute(this);
        }
    }

    /**
     * Add stop to route.  Stops must not be duplicated in a route.
     */
    public void addStop(Stop stop) {
        if(!stops.contains(stop))
        {
            stops.add(stop);
            stop.addRoute(this);
        }
    }

    /**
     * Remove stop from route
     */
    public void removeStop(Stop stop) {
        if(stops.contains(stop))
        {
            stops.remove(stop);
            stop.removeRoute(this);
        }
    }

    /**
     * Return all the stops in this route, in the order in which they were added
     */
    public List<Stop> getStops() {
        return Collections.unmodifiableList(stops);
    }

    /**
     * Determines if this route has a stop at a given stop
     */
    public boolean hasStop(Stop stop) {
        return stops.contains(stop);
    }

    /**
     * Two routes are equal if their numbers are equal
     */
    @Override
    public boolean equals(Object o) {
        if(this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        Route route = (Route) o;

        return route.getNumber().equals(this.number);
    }

    /**
     * Two routes are equal if their numbers are equal.
     * Therefore hashCode only pays attention to number.
     */
    @Override
    public int hashCode() {
        return number.hashCode();
    }

    @Override
    public Iterator<Stop> iterator() {
        // Do not modify the implementation of this method!
        return stops.iterator();
    }

    /**
     * Return the name of this route
     */
    public String getName() {
        return name;
    }

    @Override
    public String toString() {
        return "Route " + getNumber();
    }

    /**
     * Return the pattern with the given name. If it does not exist, then create it and add it to the patterns.
     * In either case, update the destination and direction of the pattern.

     */
    public RoutePattern getPattern(String patternName, String destination, String direction) {
        int index = 0;
        for(RoutePattern next : routes)
        {
            index++;
            if(next.getName().equals(patternName))
            {
                routes.get(index).setDestination(destination);
                routes.get(index).setDirection(direction);
                next.setDestination(destination);
                next.setDirection(direction);
                return next;
            }
        }

        RoutePattern rp = new RoutePattern(patternName, destination, direction, this);
        addPattern(rp);
        return rp;
    }

    /**
     * Return the pattern with the given name. If it does not exist, then create it and add it to the patterns
     * with empty strings as the destination and direction for the pattern.
     */
    public RoutePattern getPattern(String patternName) {
        for(RoutePattern next : routes)
        {
            if(next.getName().equals(patternName))
                return next;
        }

        RoutePattern rp = new RoutePattern(patternName, "", "", this);
        addPattern(rp);
        return rp;
    }

    /**
     * Return all the patterns for this route as a list
     */
    public List<RoutePattern> getPatterns() {
        return Collections.unmodifiableList(routes);
    }
}

package ca.ubc.cs.cpsc210.translink.model;

import ca.ubc.cs.cpsc210.translink.model.exception.StopException;
import ca.ubc.cs.cpsc210.translink.util.LatLon;
import ca.ubc.cs.cpsc210.translink.util.SphericalGeometry;

import java.util.*;

/**
 * Manages all bus stops.
 *
 * Singleton pattern applied to ensure only a single instance of this class that
 * is globally accessible throughout application.
 */

public class StopManager implements Iterable<Stop> {
    public static final int RADIUS = 10000;
    private static StopManager instance;
    private Stop selected;
    public LatLon defaultLatLon = new LatLon(49.2613, -123.254);
    // Use this field to hold all of the stops.
    // Do not change this field or its type, as the iterator method depends on it
    private Map<Integer, Stop> stopMap;

    /**
     * Constructs stop manager with empty collection of stops and null as the selected stop
     */
    private StopManager() {
        selected = null;
        stopMap = new HashMap<>();
    }

    /**
     * Gets one and only instance of this class
     */
    public static StopManager getInstance() {
        // Do not modify the implementation of this method!
        if(instance == null) {
            instance = new StopManager();
        }

        return instance;
    }

    public Stop getSelected() {
        return selected;
    }

    /**
     * Get stop with given id, creating it if necessary. If it is necessary to create a new stop,
     * then provide it with an empty string as its name, and a default location somewhere in the
     * lower mainland as its location.
     *
     * In this case, the correct name and location of the stop will be provided later
     *
     * @param id  the id of this stop
     *
     * @return  stop with given id
     */
    public Stop getStopWithId(int id) {
        Stop s;
        if(stopMap.containsKey(id))
            return stopMap.get(id);
        else {
            s = new Stop(id, "", defaultLatLon);
            stopMap.put(id, s);
        }

        return getStopWithId(id);
    }

    /**
     * Get stop with given id, creating it if necessary, using the given name and latlon
     *
     * @param id  the id of this stop
     *
     * @return  stop with given id
     */
    public Stop getStopWithId(int id, String name, LatLon locn) {
        Stop s;
        if(stopMap.containsKey(id))
            return stopMap.get(id);
        else {
            s = new Stop(id, name, locn);
            stopMap.put(id, s);
        }

        return getStopWithId(id, name, locn);
    }

    /**
     * Set the stop selected by user
     *
     * @param selected   stop selected by user
     * @throws StopException when stop manager doesn't contain selected stop
     */
    public void setSelected(Stop selected) throws StopException {
        if(stopMap.containsKey(selected.getNumber()))
            this.selected = selected;
        else
            throw new StopException("No such stop: " + selected.getNumber() + " " + selected.getName());
    }

    /**
     * Clear selected stop (selected stop is null)
     */
    public void clearSelectedStop() {
        selected = null;
    }

    /**
     * Get number of stops managed
     *
     * @return  number of stops added to manager
     */
    public int getNumStops() {
        return stopMap.size();
    }

    /**
     * Remove all stops from stop manager
     */
    public void clearStops() {
        stopMap.clear();
    }

    /**
     * Find nearest stop to given point.  Returns null if no stop is closer than RADIUS metres.
     *
     * @param pt  point to which nearest stop is sought
     * @return    stop closest to pt but less than 10,000m away; null if no stop is within RADIUS metres of pt
     */
    public Stop findNearestTo(LatLon pt) {
        Stop st = null;
        double minDist = -1;
        Iterator<Stop> sIterator = iterator();
        while(sIterator.hasNext()){
            Stop s = sIterator.next();
            double distance = SphericalGeometry.distanceBetween(s.getLocn(), pt);
            if(distance < RADIUS){
                if(distance < minDist || st == null){
                    st = s;
                    minDist = distance;
                }
            }
        }
        return st;
    }

    @Override
    public Iterator<Stop> iterator() {
        // Do not modify the implementation of this method!
        return stopMap.values().iterator();
    }
}

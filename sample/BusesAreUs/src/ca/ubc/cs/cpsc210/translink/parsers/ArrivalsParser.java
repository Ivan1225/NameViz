package ca.ubc.cs.cpsc210.translink.parsers;

import ca.ubc.cs.cpsc210.translink.model.*;
import ca.ubc.cs.cpsc210.translink.parsers.exception.ArrivalsDataMissingException;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;



/**
 * A parser for the data returned by the Translink arrivals at a stop query
 */
public class ArrivalsParser {

    /**
     * Parse arrivals from JSON response produced by TransLink query.  All parsed arrivals are
     * added to the given stop assuming that corresponding JSON object has a RouteNo: and an
     * array of Schedules:
     * Each schedule must have an ExpectedCountdown, ScheduleStatus, and Destination.  If
     * any of the aforementioned elements is missing, the arrival is not added to the stop.
     *
     * @param stop             stop to which parsed arrivals are to be added
     * @param jsonResponse    the JSON response produced by Translink
     * @throws JSONException  when JSON response does not have expected format
     * @throws ArrivalsDataMissingException  when no arrivals are found in the reply
     */
    public static void parseArrivals(Stop stop, String jsonResponse) throws JSONException, ArrivalsDataMissingException
    {
        try {
            JSONArray array = new JSONArray(jsonResponse);
            for (int i = 0; i < array.length(); i++) {
                JSONObject route = array.getJSONObject(i);
                parseArrival(stop, route);
            }
        }
        catch (JSONException e) {
            throw new JSONException("Error in JSON format");
        }
    }

    private static void parseArrival(Stop stop, JSONObject route) throws JSONException, ArrivalsDataMissingException
    {
        String direction;
        String routeNo;
        String routeName;

        try
        {
            direction = route.getString("Direction");
            routeNo = route.getString("RouteNo");
            routeName = route.getString("RouteName");
        }
        catch (JSONException e)
        {
            throw new ArrivalsDataMissingException("RouteNo or Direction or RouteName is missing");
        }

        Route r = RouteManager.getInstance().getRouteWithNumber(routeNo, routeName);
        JSONArray arrivals = route.getJSONArray("Schedules");

        for (int j = 0; j < arrivals.length(); j++) {
            JSONObject arrival = arrivals.getJSONObject(j);
            Arrival a = parseArrivalParts(arrival, r, direction);
            if(a != null)
                stop.addArrival(a);
        }
        r.addStop(stop);
    }

    private static Arrival parseArrivalParts(JSONObject arrival, Route r, String direction) throws JSONException, ArrivalsDataMissingException
    {
        if(!arrival.has("Destination") || !arrival.has("ExpectedCountdown")
                || !arrival.has("ScheduleStatus") || !arrival.has("Pattern"))
            throw new ArrivalsDataMissingException("Destination or ExpectedCountdown");

        else
        {
            int minsToStop = arrival.getInt("ExpectedCountdown");
            String destination = arrival.getString("Destination");
            String scheduleStatus = arrival.getString("ScheduleStatus");
            String pattern = arrival.getString("Pattern");

            RoutePattern rp = new RoutePattern(pattern, destination, direction, r);
            r.addPattern(rp);
            Arrival a = new Arrival(minsToStop, destination, r);
            a.setStatus(scheduleStatus);
            return a;
        }
    }
}


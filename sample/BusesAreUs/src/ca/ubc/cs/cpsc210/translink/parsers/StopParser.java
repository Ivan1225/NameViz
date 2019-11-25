package ca.ubc.cs.cpsc210.translink.parsers;

import ca.ubc.cs.cpsc210.translink.model.*;
import ca.ubc.cs.cpsc210.translink.parsers.exception.StopDataMissingException;
import ca.ubc.cs.cpsc210.translink.providers.DataProvider;
import ca.ubc.cs.cpsc210.translink.providers.FileDataProvider;
import ca.ubc.cs.cpsc210.translink.util.LatLon;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;


/**
 * A parser for the data returned by Translink stops query
 */
public class StopParser {

    private String filename;

    public StopParser(String filename) {
        this.filename = filename;
    }
    /**
     * Parse stop data from the file and add all stops to stop manager.
     *
     */
    public void parse() throws IOException, StopDataMissingException, JSONException{
        DataProvider dataProvider = new FileDataProvider(filename);

        parseStops(dataProvider.dataSourceToString());
    }
    /**
     * Parse stop information from JSON response produced by Translink.
     * Stores all stops and routes found in the StopManager and RouteManager.
     *
     * @param  jsonResponse    string encoding JSON data to be parsed
     * @throws JSONException   when JSON data does not have expected format
     * @throws StopDataMissingException when
     * <ul>
     *  <li> JSON data is not an array </li>
     *  <li> JSON data is missing Name, StopNo, Routes or location (Latitude or Longitude) elements for any stop</li>
     * </ul>
     */

    private void parseStops(String jsonResponse) throws JSONException, StopDataMissingException {
        JSONArray array = new JSONArray(jsonResponse);

        for(int i = 0; i < array.length(); i++)
        {
            JSONObject stop = array.getJSONObject(i);
            parseStop(stop);
        }
    }

    private void parseStop(JSONObject stop) throws JSONException, StopDataMissingException
    {
        String stopName = stop.getString("Name");
        int stopNo = stop.getInt("StopNo");
        double lat = stop.getDouble("Latitude");
        double lon = stop.getDouble("Longitude");

        String routeNos = stop.getString("Routes");

        if (stopName == null || stopName.length() == 0)
            throw new StopDataMissingException("StopName missing");

        if(stopNo == 0)
            throw new StopDataMissingException("StopNo missing");

        if(lat == 0.0)
            throw new StopDataMissingException("Latitude missing");

        if(lon == 0.0)
            throw new StopDataMissingException("Longitude missing");

        if(routeNos == null)
            throw new StopDataMissingException("RouteNo missing");

        Stop s = StopManager.getInstance().getStopWithId(stopNo, stopName, new LatLon(lat, lon));

        if(routeNos.contains(","))
        {
            int index = routeNos.indexOf(",");
            s.addRoute(RouteManager.getInstance().getRouteWithNumber(routeNos.substring(0, index)));

            while(index+5 <= routeNos.length())
            {
                s.addRoute(RouteManager.getInstance().getRouteWithNumber(routeNos.substring(index + 2, index + 5)));
                index += 5;
            }
        }
        else
            s.addRoute(RouteManager.getInstance().getRouteWithNumber(routeNos));
    }
}

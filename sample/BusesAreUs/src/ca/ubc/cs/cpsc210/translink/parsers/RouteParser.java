package ca.ubc.cs.cpsc210.translink.parsers;

import ca.ubc.cs.cpsc210.translink.model.Route;
import ca.ubc.cs.cpsc210.translink.model.RouteManager;
import ca.ubc.cs.cpsc210.translink.model.RoutePattern;
import ca.ubc.cs.cpsc210.translink.parsers.exception.RouteDataMissingException;
import ca.ubc.cs.cpsc210.translink.providers.DataProvider;
import ca.ubc.cs.cpsc210.translink.providers.FileDataProvider;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

/**
 * Parse route information in JSON format.
 */
public class RouteParser {
    private String filename;

    public RouteParser(String filename) {
        this.filename = filename;
    }
    /**
     * Parse route data from the file and add all route to the route manager.
     *
     */
    public void parse() throws IOException, RouteDataMissingException, JSONException{
        DataProvider dataProvider = new FileDataProvider(filename);

        parseRoutes(dataProvider.dataSourceToString());
    }
    /**
     * Parse route information from JSON response produced by Translink.
     * Stores all routes and route patterns found in the RouteManager.
     *
     * @param  jsonResponse    string encoding JSON data to be parsed
     * @throws JSONException   when JSON data does not have expected format
     * @throws RouteDataMissingException when
     * <ul>
     *  <li> JSON data is not an array </li>
     *  <li> JSON data is missing Name, StopNo, Routes or location elements for any stop</li>
     * </ul>
     */

    private void parseRoutes(String jsonResponse) throws JSONException, RouteDataMissingException {
        JSONArray array = new JSONArray(jsonResponse);

        for (int i = 0; i < array.length(); i++)
        {
            JSONObject route = array.getJSONObject(i);
            parseRoute(route);
        }
    }

    private void parseRoute(JSONObject route) throws JSONException, RouteDataMissingException {
        if(!route.has("RouteNo") || !route.has("Name") || !route.has("Patterns"))
            throw new RouteDataMissingException("RouteNo or Name pr Patterns is missing");

        String routeNo = route.getString("RouteNo");
        String routeName = route.getString("Name");

        Route r = RouteManager.getInstance().getRouteWithNumber(routeNo, routeName);

        Object elements = route.get("Patterns");
        if (!(elements instanceof JSONArray))
            throw new RouteDataMissingException("Route Pattern is not a JSON Array");

        else {
            JSONArray patterns = (JSONArray) elements;

            for (int i = 0; i < patterns.length(); i++) {
                JSONObject pattern = patterns.getJSONObject(i);

                if(!pattern.has("Destination") || !pattern.has("Direction") || !pattern.has("PatternNo"))
                    throw new RouteDataMissingException("Destination or Direction or PatternNo is missing");

                String stopName = pattern.getString("Destination");
                String direction = pattern.getString("Direction");
                String patternNo = pattern.getString("PatternNo");

                RoutePattern rp = new RoutePattern(patternNo, stopName, direction, r);
                r.addPattern(rp);
            }
        }
    }
}

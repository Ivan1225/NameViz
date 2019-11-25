package ca.ubc.cs.cpsc210.translink.util;

/**
 * Compute relationships between points, lines, and rectangles represented by LatLon objects
 */
public class Geometry {
    /**
     * Return true if the point is inside of, or on the boundary of, the rectangle formed by northWest and southeast
     * @param northWest         the coordinate of the north west corner of the rectangle
     * @param southEast         the coordinate of the south east corner of the rectangle
     * @param point             the point in question
     * @return                  true if the point is on the boundary or inside the rectangle
     */
    public static boolean rectangleContainsPoint(LatLon northWest, LatLon southEast, LatLon point) {
        return between(southEast.getLatitude(), northWest.getLatitude(), point.getLatitude())
                && between(northWest.getLongitude(), southEast.getLongitude(), point.getLongitude());
    }

    /**
     * Return true if the rectangle intersects the line
     * @param northWest         the coordinate of the north west corner of the rectangle
     * @param southEast         the coordinate of the south east corner of the rectangle
     * @param src               one end of the line in question
     * @param dst               the other end of the line in question
     * @return                  true if any point on the line is on the boundary or inside the rectangle
     */
    public static boolean rectangleIntersectsLine(LatLon northWest, LatLon southEast, LatLon src, LatLon dst) {

        if(rectangleContainsPoint(northWest, southEast, src) || rectangleContainsPoint(northWest, southEast, dst))
            return true;

        else
            return linesIntersect(src.getLongitude(), src.getLatitude(), dst.getLongitude(), dst.getLatitude(),
                    northWest.getLongitude(), northWest.getLatitude(), southEast.getLongitude(), northWest.getLatitude())
                    || linesIntersect(src.getLongitude(), src.getLatitude(), dst.getLongitude(), dst.getLatitude(),
                    northWest.getLongitude(), southEast.getLatitude(), southEast.getLongitude(), southEast.getLatitude())
                    || linesIntersect(src.getLongitude(), src.getLatitude(), dst.getLongitude(), dst.getLatitude(),
                    northWest.getLongitude(), northWest.getLatitude(), northWest.getLongitude(), southEast.getLatitude())
                    || linesIntersect(src.getLongitude(), src.getLatitude(), dst.getLongitude(), dst.getLatitude(),
                    southEast.getLongitude(), northWest.getLatitude(), southEast.getLongitude(), southEast.getLatitude());
    }

    private static boolean linesIntersect(double x1, double y1, double x2, double y2, double x3, double y3, double x4, double y4)
    {
        //http://www.realtimerendering.com/resources/GraphicsGems/gemsii/xlines.c

        double a1, a2, b1, b2, c1, c2;
        double r1, r2, r3, r4;
        double denom;

        a1 = y2 - y1;
        b1 = x1 - x2;
        c1 = x2 * y1 - x1 * y2;

        r3 = a1 * x3 + b1 * y3 + c1;
        r4 = a1 * x4 + b1 * y4 + c1;

        if (r3 != 0 && r4 != 0 && sameSigns(r3, r4))
            return false;

        a2 = y4 - y3;
        b2 = x3 - x4;
        c2 = x4 * y3 - x3 * y4;

        r1 = a2 * x1 + b2 * y1 + c2;
        r2 = a2 * x2 + b2 * y2 + c2;

        if (r1 != 0 && r2 != 0 && sameSigns(r1, r2))
            return false;

        denom = a1 * b2 - a2 * b1;
        if (denom == 0)
            return true;

        return true;
    }

    private static boolean sameSigns(double a, double b)
    {
        return (a<0 && b<0) || (a>0 && b>0);
    }

    /**
     * A utility method that you might find helpful in implementing the two previous methods
     * Return true if x is >= lwb and <= upb
     * @param lwb      the lower boundary
     * @param upb      the upper boundary
     * @param x         the value in question
     * @return          true if x is >= lwb and <= upb
     */
    private static boolean between(double lwb, double upb, double x) {
        return lwb <= x && x <= upb;
    }
}

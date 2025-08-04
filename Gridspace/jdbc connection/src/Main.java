import java.sql.*;

public class Main {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/gridspace";
        String user = "root";
        String password = "Lucifer@1234";

        String query = "SELECT * FROM apartment_details";

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            Connection con = DriverManager.getConnection(url, user, password);
            Statement stmt = con.createStatement();
            ResultSet rs = stmt.executeQuery(query);

            System.out.printf("%-10s %-25s %-10s %-60s%n", "ROOM_NO", "APT_TITLE", "AREA", "APARTMENT_DESC");
            System.out.println("---------------------------------------------------------------------------------------------------------");

            while (rs.next()) {
                int roomNo = rs.getInt("ROOM_NO");
                String title = rs.getString("APT_TITLE");
                int area = rs.getInt("AREA");
                String desc = rs.getString("APARTMENT_DESC");

                System.out.printf("%-10d %-25s %-10d %-60s%n", roomNo, title, area, desc);
            }

            rs.close();
            stmt.close();
            con.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
